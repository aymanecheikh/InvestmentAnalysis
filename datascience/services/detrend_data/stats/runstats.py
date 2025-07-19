from datascience.services.detrend_data.stats.statstrat import (
    ComparativeStatistic,
    PureStatistic,
)

class RunStats:
    def run_pure_stats(self, detrended_data):
        return {
            str(statistic()): statistic().test_detrend(detrended_data)
            for statistic in PureStatistic.__subclasses__()
        }

    def run_comparative_stats(self, raw_data, detrended_data):
        return {
            str(statistic()): statistic().test_detrend(raw_data, detrended_data)
            for statistic in ComparativeStatistic.__subclasses__()
        }

    def detrended_data_statistics(self, raw_data, detrended_data):
        return self.run_pure_stats(detrended_data) | self.run_comparative_stats(
            raw_data, detrended_data
        )
