from pandas import DataFrame


class Consumption:
    def consume_data(self, data: list):
        consumed = DataFrame([dict(res) for res in data])
        return consumed
