# NFL Offense Touchdown Predictor
#### A set of programs that utilize a Poisson Regression model to predict how many offensive touchdowns Team A will score against Team B and vice versa.

### About
Generates stats scraped from rotowire.com that will be used to predict how many offensive touchdowns a team will score

### Installing Necessary Modules
Make sure you have the necessary modules installed to run the program. You can do that by typing `pip install -r requirements.txt`

### How It Works
This project consists of two main Python files:
-GenerateStats.py
-MakePrediction.py
Several imported modules:
-./MyModules/NFLPredictionModel.py
- ./MyModules/NFLStats.py
- ./MyModules/NFLStatsMetricsPredictor.py
- ./MyModules/NFLTeams.py
- ./MyModules/RotowireWebDriver.py
And several miscellaneous files:
- ./Game IDs/* GameIDs.txt
- ./Matchups/* Matchups.txt
- ./Predictions/Predictions.csv
- ./Season Stats/* DefenseSeasonStats.csv
- ./Season Stats/* OffenseSeasonStats.csv
- ./Team Stats/* TeamStatsAll.csv
- ./Team Stats Metrics/* TeamStatsMetrics.csv

### How To Use
- To use the program, you must ensure that you have a list of rotowire.com game IDs (most preferably within the same season) in a text file. This text file MUST be in the 'Game ID' directory with the name formatted as '* GameIDs' where * is the year of the NFL season.
- You then generate the necessary stats files that will be used in the prediction model using the following command: `python.exe ./GenerateStats.py {year}`
- Before making predictions, there MUST be a text file named '* Matchups.txt' in the 'Matchups' directory. The matchups don't necessarily need to follow the actual schedule of the season.
- You then make the prediction by using the following command: `python.exe ./MakePredictions.py {year the model is based on} {year that the stats will be pulled from} compare`
- 'compare' argument (optional) enables the program to compare the predicted touchdown score to the team's actual touchdown score and displays and saves the results (should be used if you have the actual statistics)

#### GameIDs.txt Format
Each line in the file represents a unique game ID and MUST contain only that game ID

#### Matchups.txt Format
Each line represents a game between Team A and Team B and MUST be written out in their abbreviated name (refer to NFLTeams.py to get a list of each team's abbreviations). Each line should look like this: "TeamA,TeamB"

#### GenerateStats.py
Responsible for generating a collection of team stats from every game, a collection of every team's seasonal stats, and a collection of stat metrics that will be used in the prediction model.

#### MakePredictions.py
Responsible for predicting each game listed in the matchups text file.

#### ./MyModules/NFLPredictionModel.py
Responsible for the training and testing of the prediction model. The model utilizes Poisson Regression and K-Fold Cross-Validation.

#### ./MyModules/NFLStats.py
Responsible for creating the CSV files for team stats, season stats, and stat metrics.

#### ./MyModules/NFLStatsMetricsPredictor.py
Responsible for calculating expected values for each predictor metric.

#### ./MyModules/RotowireWebDriver.py
Responsible for accessing the rotowire.com web page for each game and parsing out the stats
