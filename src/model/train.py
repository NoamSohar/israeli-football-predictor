import pandas as pd
from xgboost import XGBClassifier

class ModelTrainer:
    def __init__(self, dataset_path: str, feature_columns: list[str], model_params: dict):
        self.dataset_path = dataset_path
        self.feature_columns = feature_columns

        self.df = None
        self.model = None
        self.model_params = model_params

        self.x_train = None
        self.y_train = None

        self.x_val = None
        self.y_val = None

    def load_data(self):
        self.df = pd.read_csv(self.dataset_path)

        self.df["date"] = pd.to_datetime(self.df["date"])
        self.df = self.df.sort_values("date").reset_index(drop=True)


    def split_data(self, validation_days: int=30):
        x = self.df[self.feature_columns]
        y = self.df["result"]

        last_date = self.df["date"].max()
        split_date = last_date - pd.Timedelta(validation_days)

        train_df = self.df[self.df["date"] < split_date]
        val_df = self.df[self.df["date"] >= split_date]

        self.x_train = train_df[self.feature_columns]
        self.y_train = train_df["result"]

        self.x_val = val_df[self.feature_columns]
        self.y_val = val_df["result"]

    def train(self):
        self.model = XGBClassifier(**self.model_params)



    def evaluate(self):
        pass