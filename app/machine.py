from sklearn.ensemble import RandomForestClassifier
import datetime
from joblib import dump, load


class Machine:
    """
    Initiate the Learning Model, Fit the model to the given data
    and store the model attribute
    """
    def __init__(self, df):
        self.name = "Random Forest Classifier"
        target = df['Rarity']
        features = df.drop(columns=['Rarity'])
        self.model = RandomForestClassifier(max_depth=10,
                                            random_state=42,
                                            n_estimators=75)
        self.model.fit(features, target)
        self.timestamp = datetime.datetime.now()

    def __call__(self, feature_basis):
        """
        Return a prediction value and the confidence for that prediction
        value.
        :param feature_basis:
        :return:
        """
        prediction, *_ = self.model.predict(feature_basis)
        probability, *_ = self.model.predict_proba(feature_basis)
        return prediction, max(probability)

    def save(self, filepath):
        """
        Save the model to a filepath
        :param filepath:
        :return:
        """
        dump(self.model, "model.joblib")

    @staticmethod
    def open(filepath):
        """
        Loads the model from filepath
        :param filepath:
        :return:
        """
        load("model.joblib")

    def info(self):
        """
        Return a string of information about the model
        :return:
        """
        return f"Base Model: {self.name} <br> Timestamp: {self.timestamp}"
