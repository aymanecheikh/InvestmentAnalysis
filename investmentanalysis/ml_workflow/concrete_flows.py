from .abstract_template import TemplatePredictionWorkflow


class ClosePredictionWorkflow(TemplatePredictionWorkflow):
    def consume_data(self):
        return "Fetching closing data"  # We are here

    def preprocess_data(self):
        return "Preprocessing data"

    def explore_data(self):
        return "Exploring data & generating insights"

    def engineer_features(self):
        return "Feature engineering data"

    def select_models(self):
        return "Selecting appropriate model(s)"

    def train_models(self):
        return "Training model"


class VolumePredictionWorkflow(TemplatePredictionWorkflow):
    def consume_data(self):
        return "Consuming Volume data from yf"  # We are here

    def preprocess_data(self):
        return "Preprocessing volume data"

    def explore_data(self):
        return "Exploring data & generating insights"

    def engineer_features(self):
        return "Feature engineering data"

    def select_models(self):
        return "Selecting appropriate model(s)"

    def train_models(self):
        return "Training model"
