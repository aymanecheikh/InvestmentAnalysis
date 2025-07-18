from datascience.services.detrender.strat_design import DetrendingStrategy


class Detrending:
    def consume_detrending_strategy_implementations(self, data):
        return [
            strategy().detrend(data) for strategy in DetrendingStrategy.__subclasses__()
        ]
