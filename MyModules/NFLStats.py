# My Modules
from MyModules.RotowireWebDriver import GetDataFrameFromGameID
from MyModules.NFLTeams import abbreviation_to_fullname

# Third Party Modules
from warnings import filterwarnings
from os import path, makedirs
from math import floor
from time import sleep
from sys import exit
import pandas as pd
import csv

def GenerateTeamStatsCSV(year: int):
    """
    Generate a CSV file containing team stats for every game during the specified NFL Season.
    Parameters:
        year (int): The year of the NFL season
    """
    try:
        text_file = open(f"./Game IDs/{year} GameIDs.txt", "r")
        
    except FileNotFoundError:
        exit("GAME IDs TEXT FILE NOT FOUND: Perhaps try a different year or create a game ID text file containing game IDs from that year!")

    # Make "Team Stats" directory if it doesn't exist
    if not path.exists("./Team Stats"):
        makedirs("./Team Stats")
    
    # Open "Team Stats" csv file
    team_stats_csv = open(f"./Team Stats/{year} TeamStatsAll.csv", "w", newline="")
    csv_writer = csv.writer(team_stats_csv)

    # Write the header row to the CSV file
    csv_writer.writerow(["Team Name", "Vs", "Total Yards", "Total Plays", "Yards Per Play", "Time of Possession",
        "1st Down", "Passing 1st Down", "Rushing 1st Down", "1st Down From Penalties",
        "3rd Downs Converted", "3rd Down Attempts",
        "4th Downs Converted", "4th Down Attempts",
        "Red Zone Score", "Red Zone Trips", "Goal To Go Score", "Goal To Go Trips",
        "Passing Yards", "Pass Completions", "Pass Attempts", "Yards Per Pass", "Passing Touchdowns",
        "Sacks Allowed", "Sack Yards Lost",
        "Rushing Yards", "Rush Attempts", "Yards Per Rush", "Rushing Touchdowns",
        "Penalties Committed", "Penalty Yards",
        "Turnovers", "Fumbles Lost", "Interceptions Thrown",
        "Defense/Special Teams Touchdowns", "Interception For Touchdown",
        "Fumble Recovery For Touchdown", "Kickoff Return For Touchdown", "Punt Return For Touchdown",
        "Field Goals Made", "Field Goal Attempts", "Extra Points Made", "Extra Point Attempts", "Safeties", "Two Points Converted", "Two Points Attempted",
        "GameID"])
    
    print(f"Now scraping team stats data for the {year} NFL Season!")

    # Loop through all the game IDs in the text file
    lines = text_file.readlines()

    total_games = len(lines)
    games_processed = 0

    for line in lines:
        game_id = line.strip()
        print(f"Processing Game ID: {game_id}")

        team_stats_df = GetDataFrameFromGameID(game_id)

        # Split the DataFrame into away team and home team
        # Ignore negative stats
        away_team_stats = team_stats_df.iloc[:, 1].to_list()
        away_team_stats_list = SplitStats(away_team_stats)

        home_team_stats = team_stats_df.iloc[:, 2].to_list()
        home_team_stats_list = SplitStats(home_team_stats)

        # Write the data to the CSV file
        # Structure [Team Name, Vs] + [Stats] + [Game ID]
        csv_writer.writerow([team_stats_df.columns[1], team_stats_df.columns[2]] + away_team_stats_list + [game_id])
        csv_writer.writerow([team_stats_df.columns[2], team_stats_df.columns[1]] + home_team_stats_list + [game_id])

        games_processed += 1
        print(f"{games_processed} of {total_games} ({floor(games_processed/total_games * 100)}%) games processed!!!")

        sleep(8)

    team_stats_csv.close()

def GenerateSeasonStatsCSV(year: int):
    """
    Generate two CSV files containing Offensive & Defensive season stats for every team during the specified NFL Season.
    Parameters:
        year (int): The year of the NFL season
    """
    # Ignore division by 0 warnings
    filterwarnings("ignore", message="invalid value encountered in scalar divide")

    # Make "Season Stats" directory if it doesn't exist
    if not path.exists("./Season Stats"):
        makedirs("./Season Stats")

    # Read Team Stats CSV file
    team_stats_df = pd.read_csv(f"./Team Stats/{year} TeamStatsAll.csv")
    offense_stats_df = pd.DataFrame()
    defense_stats_df = pd.DataFrame()

    # Filter the team stats DataFrame to only extract stats for each team
    teams_list = list(abbreviation_to_fullname.keys())
    team_stats_df = team_stats_df.drop(columns=["GameID", "Time of Possession"])

    for team in teams_list:
        # Filter the DataFrame to only include the current team
        offense_df = team_stats_df[team_stats_df["Team Name"].isin([team])]
        defense_df = team_stats_df[team_stats_df["Vs"].isin([team])]

        # Sum the stats for the current team
        offense_df = offense_df.sum()
        defense_df = defense_df.sum()

        offense_df["Team Name"] = team
        defense_df["Team Name"] = team

        # Recalculate specific stats (e.g. Yards per play)
        offense_df = RecalculateStats(offense_df)
        defense_df = RecalculateStats(defense_df)

        offense_df["Games Played"] = team_stats_df[team_stats_df["Team Name"].isin([teams_list[0]])].index.size
        defense_df["Games Played"] = team_stats_df[team_stats_df["Vs"].isin([teams_list[0]])].index.size

        # Add the Team's stats to the season stats DataFrame
        offense_stats_df = pd.concat([offense_stats_df, offense_df], axis=1)
        defense_stats_df = pd.concat([defense_stats_df, defense_df], axis=1)
    
    offense_stats_df = offense_stats_df.transpose()
    defense_stats_df = defense_stats_df.transpose()

    offense_stats_df = offense_stats_df.drop(columns=["Vs"], errors=True)
    defense_stats_df = defense_stats_df.drop(columns=["Vs"], errors=True)

    # Generate CSV file
    offense_stats_df.to_csv(f"./Season Stats/{year} OffenseSeasonStats.csv", index=False)
    defense_stats_df.to_csv(f"./Season Stats/{year} DefenseSeasonStats.csv", index=False)

def GenerateStatsMetricsCSV(year: int):
    """
    Generate a CSV file containing stat metrics that will be use for the prediction model.
    Parameters:
        year (int): The year of the NFL season
    """
    # Make "Team Stats Metrics" directory if it doesn't exist
    if not path.exists("./Team Stats Metrics"):
        makedirs("./Team Stats Metrics")
    
    # Read team stats CSV file
    team_stats_df = pd.read_csv(f"./Team Stats/{year} TeamStatsAll.csv")

    # Create a new DataFrame for the metrics
    metrics_df = pd.DataFrame()

    metrics_df["Team Name"] = team_stats_df["Team Name"]
    metrics_df["Offensive Touchdowns"] = team_stats_df["Passing Touchdowns"] + team_stats_df["Rushing Touchdowns"]
    metrics_df["Yards Per Play"] = team_stats_df["Yards Per Play"]
    metrics_df["Yards Per Completion"] = round(team_stats_df["Passing Yards"] / team_stats_df["Pass Completions"], 3)
    metrics_df["Yards Per Attempt"] = team_stats_df["Yards Per Pass"]
    metrics_df["Yards Per Rush"] = round(team_stats_df["Rushing Yards"] / team_stats_df["Rush Attempts"], 3)
    metrics_df["Red Zone Efficiency"] = round(team_stats_df["Red Zone Score"] / team_stats_df["Red Zone Trips"], 3)
    metrics_df["Goal To Go Efficiency"] = round(team_stats_df["Goal To Go Score"] / team_stats_df["Goal To Go Trips"], 3)
    metrics_df["Total First Downs"] = team_stats_df["1st Down"]
    metrics_df["3rd Down Efficiency"] = round(team_stats_df["3rd Downs Converted"] / team_stats_df["3rd Down Attempts"], 3)
    metrics_df["4th Down Efficiency"] = round(team_stats_df["4th Downs Converted"] / team_stats_df["4th Down Attempts"], 3)
    metrics_df["Turnover Rate"] = round(team_stats_df["Turnovers"] / team_stats_df["Total Plays"], 3)
    metrics_df["Sack Rate"] = round(team_stats_df["Sacks Allowed"] / team_stats_df["Total Plays"], 3)

    # Replace NaN values with 0
    metrics_df.fillna(0, inplace=True)

    # Generate CSV file
    metrics_df.to_csv(f"./Team Stats Metrics/{year} TeamStatsMetrics.csv", index=False)

def ComparePredictionToActualScore(predicted_scores: pd.DataFrame, year: int):
    team_td_df = pd.read_csv(f"./Team Stats/{year} TeamStatsAll.csv")
    team_actual = pd.DataFrame({"Team" : team_td_df["Team Name"], "TDs Actual": team_td_df["Passing Touchdowns"] + team_td_df["Rushing Touchdowns"]})

    # Calculate score differences
    score_diff = predicted_scores["Predicted Offensive Touchdowns"] - team_actual["TDs Actual"]
    score_diffs_over = score_diff[score_diff > 0].count()
    score_diffs_under_or_exact = score_diff[score_diff <= 0].count()

    print()
    print(f"Overestimated: {score_diffs_over}")
    print(f"Underestimated/Exact: {score_diffs_under_or_exact}")
    print(f"Percentage: {round(score_diffs_under_or_exact / (score_diffs_under_or_exact + score_diffs_over) * 100)}%")

def RecalculateStats(df: pd.DataFrame):
    """
    Responisble for recalculating rational stats such as yards/pass after summing up the other stats.
    Parameters:
        df (DataFrame): A set of stats of a given team
    Returns:
        DataFrame: A DataFrame containing a more accurate representation of rational stats.
    """
    df["Yards Per Play"] = round(df["Total Yards"] / df["Total Plays"], 1)
    df["Yards Per Pass"] = round(df["Passing Yards"] / df["Pass Attempts"], 1)
    df["Yards Per Rush"] = round(df["Rushing Yards"] / df["Rush Attempts"], 1)

    return df

def SplitStats(list: list[str]):
    """
    Splits stats that are listed with multiple stats such as completions-attempts 
    into two separate stats, completions & attempts.
    Stats starting with "-" (Negative Stats for the NYG) will not be split.
    Parameters:
        list (list[str]]): list of stats for a given team on a given week and season
    Returns:
        list[str]: A list of stats broken up into their own individual stats
    """
    
    return [
        ('-' + word if element.startswith('-') and idx == 1 else word)
        for element in list
        for idx, word in enumerate(element.split('-'))
        if word]