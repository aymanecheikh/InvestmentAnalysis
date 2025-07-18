from datascience.services.consume import Consumption
from datascience.services.detrender.strat_implmnt import Detrending


class DetrendingFacade:
    
    def __init__(self):
        self.data = Consumption()
        self.detrend = Detrending()
    
    def detrend_data(self, data):
        return self.detrend.consume_detrending_strategy_implementations(
                self.data.consume_data(data)
                )
