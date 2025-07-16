from pandas import DataFrame

def consume_data(data: list) -> DataFrame:
    return DataFrame([dict(res) for res in data]).set_index("Datetime")
