from datascience.services.consume import Consumption
from datascience.services.detrend_data.stats.runstats import RunStats
from datascience.services.detrend_data.implement.strat_implmnt import Detrending


class DetrendingFacade:
    def __init__(self):
        self.data = Consumption()
        self.detrend = Detrending()
        self.statistics = RunStats()

    def detrend_data(self, data):
        return self.detrend.consume_detrending_strategy_implementations(
            self.data.consume_data(data)
        )

    def run_stats(self, data):
        return [
            self.statistics.detrended_data_statistics(
                self.data.consume_data(data),
                detrended_data
                )
            for detrended_data in self.detrend_data(data)
        ]
