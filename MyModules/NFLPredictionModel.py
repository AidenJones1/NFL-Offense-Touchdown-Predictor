from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import KFold
import statsmodels.api as sm
import pandas as pd
import numpy as np
from sys import exit

class NFLPredictionModel:
    def __init__(self, year: int, print_training_results: bool):
        """
        Create an instance of the NFL Prediction Model using every game from the specified NFL season as the training set.
        Parameters:
            year (int): The year of the NFL Season
            print_training_results (bool): Determine whether or not to go through the training process and print the results
        """
        self.model_family = sm.families.Poisson()

        # Error Handling
        try:
            df = pd.read_csv(f"./Team Stats Metrics/{year} TeamStatsMetrics.csv")
        except FileNotFoundError:
            exit("TEAM STATS METRICS CSV FILE NOT FOUND: Perhaps try generating the csv file using 'GenerateStats.py'")
        
        # Load the data set
        self._X = df[["Yards Per Completion", "Yards Per Attempt", "Yards Per Rush", "Yards Per Play",
            "Red Zone Efficiency", "Goal To Go Efficiency", "Total First Downs", "3rd Down Efficiency", "4th Down Efficiency",
            "Turnover Rate", "Sack Rate"]]
        self._y = df["Offensive Touchdowns"]
        self._X = sm.add_constant(self._X)

        # Train Model
        if (print_training_results):
            self.TrainModel()

    def TrainModel(self):
        """
        Utilizes KFold Cross-Validation for the training process and print the results along with how many scores were over overestimated/underestimated/exact.
        """
        # Setup KFold cross-validation
        kf = KFold(n_splits=5, shuffle=True, random_state=42)
        mae_scores = []
        mse_scores = []
        score_diffs_over = []
        score_diffs_under_or_exact = []

        # Perform cross-validation
        for train_index, test_index in kf.split(self._X):
            X_train, X_test = self._X.iloc[train_index], self._X.iloc[test_index]
            y_train, y_test = self._y.iloc[train_index], self._y.iloc[test_index]

            # Fit the model
            model_train = sm.GLM(y_train, X_train, family=self.model_family).fit()

            # Make predictions
            y_pred = model_train.predict(X_test)

            # Calculate MAE
            mae = mean_absolute_error(y_test, y_pred)
            mae_scores.append(mae)

            # Calculate MSE
            mse = mean_squared_error(y_test, y_pred)
            mse_scores.append(mse)

            # Calculate score differences
            score_diff = np.floor(y_pred) - y_test
            score_diffs_over.append(score_diff[score_diff > 0].count())
            score_diffs_under_or_exact.append(score_diff[score_diff <= 0].count())

        # Print the Summary and Tests
        print(model_train.summary())

        residual_deviance = model_train.deviance
        degrees_of_freedom = model_train.df_resid
        dispersion_ratio = residual_deviance / degrees_of_freedom

        print(f"Dispersion Ratio: {dispersion_ratio:.4f}")
        if dispersion_ratio > 1:
            print("Overdispersion detected!!!")
        else:
            print("No overdispersion detected!!!")

        print("\nTESTING SCORES:")
        print(f"Average MSE: {np.mean(mse_scores):.4f}")
        print(f"Average MAE: {np.mean(mae_scores):.4f}")

        print(f"Average Number of Times the Model Overpredicted (per test): {np.mean(score_diffs_over):.4f}")
        print(f"Average Number of Times the Model Underestimated or Was Exact (per test): {np.mean(score_diffs_under_or_exact):.4f}")
    
    def FitModel(self):
        # Fit Model
        self.model = sm.GLM(self._y, self._X, family=self.model_family).fit()

    def MakePrediction(self, team_A: str, team_B: str, X_new: pd.DataFrame):
        """
        Makes a prediction based on a set of predictor variables in X_new.
        Parameters:
            team_A (str): First Team
            team_B (str): Second Team
            X_new (DataFrame): A set of predictor variables that will be used in the model
        Returns:
            DataFrame: A DataFrame representing the predicted offensive touchdowns for the offense team against the defense
        """
        X_new = sm.add_constant(X_new, has_constant="add")
        
        preds = pd.DataFrame({"Team" : [team_A, team_B]})
        preds["Predicted Offensive Touchdowns"] = np.floor(self.model.predict(X_new))
        preds["Vs"] = [team_B, team_A]
        
        return preds