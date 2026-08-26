import pandas as pd
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score

class ModelTrainer:
    def __init__(self, dataset_path: str, feature_columns: list[str]):
        self.dataset_path = dataset_path
        self.feature_columns = feature_columns

        self.df = None
        self.model = None

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

    def train(self, model_params: dict):
        self.model = XGBClassifier(**model_params)

        self.model.fit(
            self.x_train,
            self.y_train,
            eval_set = [(self.x_val, self.y_val)],
            verbose = True
        )

    def evaluate(self):
        predictions = self.model.predict(self.x_val)

        accuracy = accuracy_score(
            self.y_val,
            predictions
        )

        return accuracy