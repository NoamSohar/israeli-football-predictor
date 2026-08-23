import pandas as pd

class ModelTrainer:
    def __init__(self, dataset_path: str, feature_columns: list[str]):
        self.dataset_path = dataset_path
        self.feature_columns = feature_columns

        self.df = None
        self.model = None

        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None


    def load_data(self):
        self.df = pd.read_csv(self.dataset_path)

        self.df["date"] = pd.to_datetime(self.df["date"])
        self.df = self.df.sort_values("date").reset_index(drop=True)


    def split_data(self, train_ratio: float = 0.8):
        x = self.df[self.feature_columns]
        y = self.df["result"]

        split_index = int(len(self.df) * train_ratio)

        self.X_train = x.iloc[:split_index]
        self.X_test = x.iloc[split_index:]

        self.y_train = y.iloc[:split_index]
        self.y_test = y.iloc[split_index:]


    def train(self):
        pass


    def evaluate(self):
        pass