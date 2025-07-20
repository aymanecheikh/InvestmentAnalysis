from abc import ABC, abstractmethod
from typing import Any


class TemplatePredictionWorkflow(ABC):
    def run_workflow(self):
        self.consume_data()
        self.preprocess_data()
        self.explore_data()
        self.engineer_features()
        self.select_models()
        self.train_models()

    @abstractmethod
    def consume_data(self) -> Any:
        ...

    @abstractmethod
    def preprocess_data(self) -> Any:
        ...

    @abstractmethod
    def explore_data(self) -> Any:
        ...

    @abstractmethod
    def engineer_features(self) -> Any:
        ...

    @abstractmethod
    def select_models(self) -> Any:
        ...

    @abstractmethod
    def train_models(self) -> Any:
        ...
