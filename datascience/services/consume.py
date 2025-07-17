from pandas import DataFrame


def consume_data(data: list) -> DataFrame:
    consumed = DataFrame([dict(res) for res in data]).set_index("Datetime")
    print(consumed)
    return consumed
