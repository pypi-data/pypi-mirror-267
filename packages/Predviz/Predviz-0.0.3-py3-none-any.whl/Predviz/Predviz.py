# Libraries
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


class Predviz(object):
    """Forecast Visualizer.

    Parameters
    ----------
    data: A Pandas DataFrame that contains the actual values.
    data_pred: A Pandas DataFrame that contains the forecasted values of a time-series forecasting model.
    """

    def __init__(self, data=None, data_pred=None):
        """Initialization."""
        self.data = data
        self.data_pred = data_pred
        self.validate_input()
        self.visualizes()

    def validate_input(self):
        """Validates the inputs to Predviz."""
        # Input 'data'
        if self.data is None:
            raise ValueError("Input 'data' must not None!")

        # Input 'data_pred'
        if self.data_pred is None:
            raise ValueError("Input 'data_pred' must not None!")

        # Both inputs
        if int(self.data.shape[0]) != int(self.data_pred.shape[0]):
            raise ValueError(
                "Make sure the data counts in both 'data' and 'data_pred' is the same!"
            )
        elif not (
            isinstance(self.data, pd.DataFrame)
            and isinstance(self.data_pred, pd.DataFrame)
            and "Date" in self.data
            and "Date" in self.data_pred
        ):
            raise ValueError(
                "Both 'data' and 'data_pred' must be a DataFrame and a column named 'Date' that contains time series data must exist in both of them!"
            )
        elif not ("y" in self.data and "y_pred" in self.data_pred):
            raise ValueError(
                "The input 'data' must contain 'y' named column (contains Actual Values) and 'data_pred' must contain 'y_pred' named column (contains Predicted Values)!"
            )
        elif self.data["y"].isnull().any() or self.data_pred["y_pred"].isnull().any():
            raise ValueError("Found NaN values in 'data' or 'data_pred'!")
        elif pd.Series(self.data["Date"] != self.data_pred["Date"]).all():
            raise ValueError(
                "Found different time(s) between the 'Date' column inside the 'data' and 'data_pred' inputs!"
            )

        self.data["Date"] = pd.to_datetime(self.data["Date"])
        self.data_pred["Date"] = pd.to_datetime(self.data_pred["Date"])
        self.data["y"] = self.data["y"].astype(float)
        self.data_pred["y"] = self.data_pred["y_pred"].astype(float)

    def visualizer(self):
        plt.plot(self.data["Date"], self.data["y"], label="Actual Values")
        plt.plot(self.data_pred["Date"], self.data_pred["y_pred"], label="Forecasted Values")
        plt.suptitle("Comparison Visualization", x=0.51, fontsize=16)
        plt.title("Actual Values VS Forecasted Values", fontsize=12)
        plt.xlabel("Date")
        plt.ylabel("Values")
        plt.legend(loc="upper right")
        plt.show()
