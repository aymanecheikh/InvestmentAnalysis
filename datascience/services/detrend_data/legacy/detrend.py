"""
To be deprecated & refactored
"""

import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import (
    InterpolationWarning,
    ValueWarning,
    adfuller,
    kpss,
    acf,
    pacf,
)
from statsmodels.stats.diagnostic import acorr_ljungbox
import warnings

from datascience.services.consume import Consumption
from datascience.services.detrender.strat_design import DetrendingStrategy


warnings.simplefilter("ignore", InterpolationWarning)
warnings.simplefilter("ignore", ValueWarning)

data = Consumption()


class Autocorrelation:
    def __init__(self, detrended_data):
        self.acf_values = acf(detrended_data, nlags=30)[1:]
        self.pacf_values = pacf(detrended_data, nlags=30)[1:]

        # Revisit design
        self.acf_maac = np.mean(np.abs(self.acf_values))
        self.ma_pacf = np.mean(np.abs(self.pacf_values))
        self.max_acf = np.max(np.abs(self.acf_values))
        self.max_pacf = np.max(np.abs(self.pacf_values))

        self.ljungbox_min_pvalue = acorr_ljungbox(
            detrended_data, lags=[10, 20, 30], return_df=True
        )["lb_pvalue"].min()

    def _normalize_inverse(self, x, max_acceptable=0.05):
        return min(x / max_acceptable, 1.0)

    """For ljungbox_min_pvalue"""

    def _normalize_pvalue(self, p, threshold=0.05):
        return 1.0 - min(p / threshold, 1.0)

    def get_autocorrelation_score(self):
        return (
            self._normalize_inverse(self.acf_maac) * 0.2
            + self._normalize_inverse(self.ma_pacf) * 0.2
            + self._normalize_inverse(self.max_acf) * 0.2
            + self._normalize_inverse(self.max_pacf) * 0.2
            + self._normalize_pvalue(self.ljungbox_min_pvalue) * 0.2
        )


def add_score(score: int) -> int:
    score += 1
    return score


def detrend_strat_scoring(strat_eval_df, condition):
    qualifiers = strat_eval_df.loc[condition, "Strategy"]
    strat_eval_df.Score = strat_eval_df.apply(
        lambda row: (
            add_score(row.Score) if row.Strategy in qualifiers.values else row.Score
        ),
        axis=1,
    )
    return strat_eval_df


def evaluate_detrending_strategies(data):
    raw_data = data.consume_data(data)
    evaluation = []

    for strategy in DetrendingStrategy.__subclasses__():
        detrended_data = strategy().detrend(raw_data).dropna()

        strategy_evaluation = {
            "Strategy": str(strategy()),
            "ADF": f"{adfuller(detrended_data)[1]:.4f}",
            "KPSS": f"{kpss(detrended_data)[1]:.4f}",
            "Mean": f"{detrended_data.mean()}",
            "Variance Reduction": f"{raw_data.Close.var() - detrended_data.var()}",
            "Autocorrelation": Autocorrelation(
                detrended_data
            ).get_autocorrelation_score(),
        }

        evaluation.append(strategy_evaluation)

    strat_eval_df = pd.DataFrame(evaluation)
    strat_eval_df["Score"] = 0

    conditions = [
        strat_eval_df.ADF == strat_eval_df.ADF.min(),
        strat_eval_df.KPSS == strat_eval_df.KPSS.min(),
        strat_eval_df.Mean == strat_eval_df.Mean.min(),
        strat_eval_df["Variance Reduction"]
        == strat_eval_df["Variance Reduction"].max(),
        strat_eval_df.Autocorrelation < 0.5,
    ]

    for condition in conditions:
        detrend_strat_scoring(strat_eval_df, condition)

    print(strat_eval_df)

    winners = strat_eval_df.loc[
        strat_eval_df.Score == strat_eval_df.Score.max(), "Strategy"
    ].values

    if len(winners) == 1:
        return winners[0]
    else:
        print("More than one winner")
        return winners


"""
    print("Skewness: TBC")
    print("Kurtosis: TBC")
    print("FFT: TBC")
    print("Rolling mean stability: TBC")
    print("std stability: TBC")
"""
