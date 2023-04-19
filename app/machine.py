from pandas import DataFrame
from sklearn.ensemble import GradientBoostingClassifier
import datetime
import joblib


class Machine:

    def __init__(self, df):
        """Initializes model and stores attributes"""
        self.name = "Gradient Classifier"
        target = df["Rarity"]
        features = df.drop(columns=["Rarity"])
        self.model = GradientBoostingClassifier()
        self.model.fit(features, target)
        self.timestamp = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S %p")

    def __call__(self, feature_basis: DataFrame):
        """Takes DataFrame of feature data and returns prediction and probability of the prediction"""
        prediction, *_ = self.model.predict(feature_basis)
        confidence, *_ = self.model.predict_proba(feature_basis)
        return prediction, max(confidence)

    def save(self, filepath):
        """Saves the model to specific filepath"""
        joblib.dump(self.model, "model.joblib")

    @staticmethod
    def open(filepath):
        """Loads a saved model from filepath"""
        joblib.load("model.joblib")

    def info(self):
        """Returns name of the base model and timestamp of model's initialization"""
        return f"Base Model: {self.name} <br> Timestamp: {self.timestamp}"
