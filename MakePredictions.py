# My Modules
from MyModules.NFLStatsMetricsPredictor import GetMetricPredictors
from MyModules.NFLStats import ComparePredictionToActualScore
import MyModules.NFLPredictionModel as pm

# Third Party Modules
from os import path, makedirs
from sys import argv, exit
import pandas as pd

# Error handler
try:
    if (not str.isnumeric(argv[1]) or not str.isnumeric(argv[2])):
        exit("INVALID COMMAND ARGUMENT: First (year that the model if fitted after) and second (year to grab season stats from) argument MUST be a numerical value!")

except IndexError:
    exit("NO ARGUMENTS FOUND: Please enter a two years as arguments!")

model_after_seeaon = argv[1]
season_stats_year = argv[2]

# Get Prediction Model
prediction_model = pm.NFLPredictionModel(model_after_seeaon, False)
model = prediction_model.FitModel()

# Make Prediction(s)
pred_results = pd.DataFrame({"Team": [], "Predicted Offensive Touchdowns" : []})

txt_file = open(f"./Matchups/{season_stats_year} Matchups.txt")

# Read matchups line by line
lines = txt_file.readlines()
for i in range(len(lines)):
    teams = lines[i].strip().split(",")

    # Generate expected values for the predictor variables
    predictors = GetMetricPredictors(teams[1], teams[0], season_stats_year)

    # Get the results from the prediction
    res = prediction_model.MakePrediction(teams[1], teams[0], predictors)

    # Add the results to the overall results
    pred_results = pd.concat([pred_results, res])

# Convert touchdown value to int
pred_results = pred_results.reset_index(drop=True)
pred_results["Predicted Offensive Touchdowns"] = pred_results["Predicted Offensive Touchdowns"].astype(int)

# Print results from the model
print(pred_results)

# Make "Predictions" directory if it doesn't exist
if not path.exists("./Predictions"):
    makedirs("./Predictions")

# Saves results from the model to a CSV file
pred_results.to_csv("./Predictions/Predictions.csv", index = False)

#except FileNotFoundError:
    #pass
    #exit("MATCHUPS TEXT FILE NOT FOUND: Make sure the matchups text file is located in Matchups directory!")

# Compare Predicted Touchdowns to Actual Touchdowns Scored
if (len(argv) > 3 and argv[3].lower() == "compare"):
    ComparePredictionToActualScore(pred_results, season_stats_year)

## Comparisons

# TEST ONE
# Model After: 2023
# Sample: Every 2023 NFL game
# Successful Predictions: 73% 

# TEST TWO
# Model After: 2024
# Sample: Every 2024 NFL game
# Successful Predictions: 84%

# TEST THREE
# Model After: 2023
# Sample: Every 2024 NFL game
# Successful Predictions: 71%
