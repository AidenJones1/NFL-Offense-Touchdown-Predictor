import pandas as pd

def ExpectedValue(offense_df: pd.DataFrame, defense_df: pd.DataFrame, league_df: pd.DataFrame, stat: str):
    """
    A formula use to calculate expected values
    Parameters:
        offense_df (DataFrame): The team's offense stats
        defense_df (DataFrame): The other team's defense stats
        league_df (DataFram): A collection of the entire leagues offensive stats
        stat (str): The specific stat to access
    Returns:
        float: The expected value for the offense's specified stat 
    """
    return ((offense_df[stat].iloc[0] / offense_df["Games Played"].iloc[0]) * (defense_df[stat].iloc[0] / defense_df["Games Played"].iloc[0])) / league_df[stat].mean()

def GetMetricPredictors(home_team: str, away_team: str, year: int):
    """
    Calculates all of the expected values for each predictor variables for both teams according to both teams offense vs the defense.
    Parameters:
        home_team (str): Home Team
        away_team (str): Away Team
        year (int): The year of the NFL Season
    Returns:
        DataFrame: A DataFrame representing a set of predicted stats for the two teams facing each other.
    """
    # Read offense/defense season stats and team stats csv files 
    league_stats = pd.read_csv(f"./Team Stats/{year} TeamStatsAll.csv") 
    offense_stats = pd.read_csv(f"./Season Stats/{year} OffenseSeasonStats.csv")
    defense_stats = pd.read_csv(f"./Season Stats/{year} DefenseSeasonStats.csv")

    # Get Offense and Defense season stats for both teams
    home_off = offense_stats.loc[offense_stats["Team Name"] == home_team]
    away_off = offense_stats.loc[offense_stats["Team Name"] == away_team]

    home_def = defense_stats.loc[defense_stats["Team Name"] == home_team]
    away_def = defense_stats.loc[defense_stats["Team Name"] == away_team]

    # Calculate expected values for total yards and total plays
    home_exp_plays = ExpectedValue(home_off, away_def, league_stats, "Total Plays")
    away_exp_plays = ExpectedValue(away_off, home_def, league_stats, "Total Plays")

    home_exp_yards_per_play = ExpectedValue(home_off, away_def, league_stats, "Total Yards") / home_exp_plays
    away_exp_yards_per_play = ExpectedValue(away_off, home_def, league_stats, "Total Yards") / away_exp_plays

    # Calculate expected values for passing yards per completion/attempt
    home_exp_passing_yards = ExpectedValue(home_off, away_def, league_stats, "Passing Yards")
    away_exp_passing_yards = ExpectedValue(away_off, home_def, league_stats, "Passing Yards")

    home_exp_yards_per_comp = home_exp_passing_yards / ExpectedValue(home_off, away_def, league_stats, "Pass Completions")
    away_exp_yards_per_comp = away_exp_passing_yards / ExpectedValue(away_off, home_def, league_stats, "Pass Completions")

    home_exp_yards_per_att = home_exp_passing_yards / ExpectedValue(home_off, away_def, league_stats, "Pass Attempts")
    away_exp_yards_per_att = away_exp_passing_yards / ExpectedValue(away_off, home_def, league_stats, "Pass Attempts")

    # Calculate expected values for yards per carry 
    home_exp_yards_per_rush =  ExpectedValue(home_off, away_def, league_stats, "Rushing Yards") / ExpectedValue(home_off, away_def, league_stats, "Rush Attempts")
    away_exp_yards_per_rush =  ExpectedValue(away_off, home_def, league_stats, "Rushing Yards") / ExpectedValue(away_off, home_def, league_stats, "Rush Attempts")

    # Calculate expected values for red zone efficiency
    home_exp_red_zone_eff =  ExpectedValue(home_off, away_def, league_stats, "Red Zone Score") / ExpectedValue(home_off, away_def, league_stats, "Red Zone Trips")
    away_exp_red_zone_eff =  ExpectedValue(away_off, home_def, league_stats, "Red Zone Score") / ExpectedValue(away_off, home_def, league_stats, "Red Zone Trips")

    # Calculate expected values for goal to go efficiency
    home_exp_gtg_eff =  ExpectedValue(home_off, away_def, league_stats, "Goal To Go Score") / ExpectedValue(home_off, away_def, league_stats, "Goal To Go Trips")
    away_exp_gtg_eff =  ExpectedValue(away_off, home_def, league_stats, "Goal To Go Score") / ExpectedValue(away_off, home_def, league_stats, "Goal To Go Trips")

    # Calculate expected values for first down
    home_exp_first_down =  ExpectedValue(home_off, away_def, league_stats, "1st Down")
    away_exp_first_down =  ExpectedValue(away_off, home_def, league_stats, "1st Down")

    # Calculate expected values for 3rd down efficiency
    home_exp_third_down_eff =  ExpectedValue(home_off, away_def, league_stats, "3rd Downs Converted") / ExpectedValue(home_off, away_def, league_stats, "3rd Down Attempts")
    away_exp_third_down_eff =  ExpectedValue(away_off, home_def, league_stats, "3rd Downs Converted") / ExpectedValue(away_off, home_def, league_stats, "3rd Down Attempts")

    # Calculate expected values for 4th down efficiency
    home_exp_fourth_down_eff =  ExpectedValue(home_off, away_def, league_stats, "4th Downs Converted") / ExpectedValue(home_off, away_def, league_stats, "4th Down Attempts")
    away_exp_fourth_down_eff =  ExpectedValue(away_off, home_def, league_stats, "4th Downs Converted") / ExpectedValue(away_off, home_def, league_stats, "4th Down Attempts")

    # Calculate expected values for turnover rate
    home_exp_turnover_rate =  ExpectedValue(home_off, away_def, league_stats, "Turnovers") / home_exp_plays
    away_exp_turnover_rate =  ExpectedValue(away_off, home_def, league_stats, "Turnovers") / away_exp_plays

    # Calculate expected values for turnover rate
    home_exp_sack_rate =  ExpectedValue(home_off, away_def, league_stats, "Sacks Allowed") / home_exp_plays
    away_exp_sack_rate =  ExpectedValue(away_off, home_def, league_stats, "Sacks Allowed") / away_exp_plays

    exp_predictors = pd.DataFrame({
        "Yards Per Play": [home_exp_yards_per_play, away_exp_yards_per_play],
        "Yards Per Completion": [home_exp_yards_per_comp, away_exp_yards_per_comp],
        "Yards Per Attempt": [home_exp_yards_per_att, away_exp_yards_per_att],
        "Yards Per Rush": [home_exp_yards_per_rush, away_exp_yards_per_rush],
        "Red Zone Efficiency":  [home_exp_red_zone_eff, away_exp_red_zone_eff],
        "Goal To Go Efficiency": [home_exp_gtg_eff, away_exp_gtg_eff],
        "Total First Downs": [home_exp_first_down, away_exp_first_down],
        "3rd Down Efficiency": [home_exp_third_down_eff, away_exp_third_down_eff],
        "4th Down Efficiency": [home_exp_fourth_down_eff, away_exp_fourth_down_eff],
        "Turnover Rate": [home_exp_turnover_rate, away_exp_turnover_rate],
        "Sack Rate": [home_exp_sack_rate, away_exp_sack_rate]})
    
    return exp_predictors