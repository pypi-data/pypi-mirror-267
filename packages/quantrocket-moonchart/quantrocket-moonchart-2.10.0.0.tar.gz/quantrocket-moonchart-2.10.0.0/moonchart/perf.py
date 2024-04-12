# Copyright 2017-2024 QuantRocket LLC - All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Union, TextIO
import numpy as np
import pandas as pd
from .exceptions import InsufficientData, MoonchartError
from .utils import (
    get_zscores,
    trim_outliers as trim_outliers_func,
    get_sharpe,
    get_rolling_sharpe,
    get_cagr,
    get_cum_returns,
    get_drawdowns,
    intraday_to_daily)

from quantrocket.moonshot import read_moonshot_csv
from quantrocket.blotter import read_pnl_csv

class DailyPerformance(object):
    """
    Class representing daily performance and derived statistics.

    Typically constructed using DailyPerformance.from_moonshot_csv.

    Parameters
    ----------
    returns : DataFrame, required
        a Dataframe of pct returns

    pnl : DataFrame, optional
        a DataFrame of pnl

    net_exposures : DataFrame, optional
        a Dataframe of net (hedged) exposure

    abs_exposures : DataFrame, optional
        a Dataframe of absolute exposure (ignoring hedging)

    total_holdings : DataFrame, optional
        a Dataframe of the number of holdings

    turnover : DataFrame, optional
        a DataFrame of turnover, that is, changes to positions

    commission_amounts : DataFrame, optional
        a DataFrame of commission amounts, in the base currency

    commissions : DataFrame, optional
        a DataFrame of commissions, as a proportion of capital

    slippages : DataFrame, optional
        a DataFrame of slippages, as a proportion of capital

    benchmark : Series, optional
        a Series of returns for a benchmark

    riskfree : float, optional
        the riskfree rate (default 0)

    compound : bool
         True for compound/geometric returns, False for arithmetic returns (default True)

    rolling_sharpe_window : int, optional
        compute rolling Sharpe over this many periods (default 200)

    trim_outliers: int or float, optional
        discard returns that are more than this many standard deviations from the mean
    """

    def __init__(
        self,
        returns: pd.DataFrame,
        pnl: pd.DataFrame = None,
        net_exposures: pd.DataFrame = None,
        abs_exposures: pd.DataFrame = None,
        total_holdings: pd.DataFrame = None,
        turnover: pd.DataFrame = None,
        commission_amounts: pd.DataFrame = None,
        commissions: pd.DataFrame = None,
        slippages: pd.DataFrame = None,
        benchmark: 'pd.Series[float]' = None,
        riskfree: float = 0,
        compound: bool = True,
        rolling_sharpe_window: int = 200,
        trim_outliers: float = None
        ):

        self.returns: pd.DataFrame = returns
        """a DataFrame of pct returns"""
        if len(self.returns.index) < 2:
            raise InsufficientData(
                "Moonchart needs at least 2 dates to analyze performance, "
                "but returns DataFrame has length {0}".format(len(self.returns.index)))
        self._trim_outliers = trim_outliers
        if trim_outliers:
            self.returns = trim_outliers_func(returns, z_score=trim_outliers)
        else:
            # warn the user if there are >10-sigma returns
            z_scores = get_zscores(returns)
            max_zscore = z_scores.abs().max()
            if isinstance(returns, pd.DataFrame):
                max_zscore = max_zscore.max()
            if max_zscore > 20:
                import warnings
                warnings.warn("Found returns which are {0} standard deviations from the "
                              "mean, consider removing them with the `trim_outliers` parameter".format(
                                  round(max_zscore)))
        self.pnl: pd.DataFrame = pnl
        """a DataFrame of pnl"""
        self.net_exposures: pd.DataFrame = net_exposures
        """a DataFrame of net (hedged) exposure"""
        self.abs_exposures: pd.DataFrame = abs_exposures
        """a DataFrame of absolute exposure (ignoring hedging)"""
        self.total_holdings: pd.DataFrame = total_holdings
        """a DataFrame of the number of holdings"""
        self.turnover: pd.DataFrame = turnover
        """a DataFrame of turnover, that is, changes to positions"""
        self.commission_amounts: pd.DataFrame = commission_amounts
        """a DataFrame of commission amounts, in the base currency"""
        self.commissions: pd.DataFrame = commissions
        """a DataFrame of commissions, as a proportion of capital"""
        self.slippages: pd.DataFrame = slippages
        """a DataFrame of slippages, as a proportion of capital"""
        self.riskfree: float = riskfree
        """the riskfree rate"""
        self.compound: bool = compound
        """True for compound/geometric returns, False for arithmetic returns"""
        self.rolling_sharpe_window: int = rolling_sharpe_window
        """compute rolling Sharpe over this many periods"""
        self._benchmark = benchmark
        self._benchmark_returns = None
        self._benchmark_cum_returns = None
        self._cum_returns = None
        self._cum_commissions = None
        self._cum_slippages = None
        self._cum_commission_amounts = None
        self._sharpe = None
        self._rolling_sharpe = None
        self._cagr = None
        self._drawdowns = None
        self._max_drawdown = None
        self._cum_pnl = None

    @classmethod
    def _from_moonshot_or_pnl(cls, results,
                              start_date=None,
                              end_date=None,
                              trim_outliers=None,
                              how_to_aggregate=None,
                              riskfree=0,
                              compound=True,
                              rolling_sharpe_window=200):
        """
        Creates a DailyPerformance instance from a moonshot backtest results
        DataFrame or a PNL DataFrame.
        """
        if "Time" in results.index.names:
            results = intraday_to_daily(results, how=how_to_aggregate)

        if start_date:
            results = results[results.index.get_level_values("Date") >= start_date]

        if end_date:
            results = results[results.index.get_level_values("Date") <= end_date]

        fields = results.index.get_level_values("Field").unique()
        kwargs = dict(
            trim_outliers=trim_outliers,
            riskfree=riskfree,
            compound=compound,
            rolling_sharpe_window=rolling_sharpe_window
        )
        kwargs["returns"] = results.loc["Return"]

        if "Pnl" in fields:
            kwargs["pnl"] = results.loc["Pnl"]
        if "NetExposure" in fields:
            kwargs["net_exposures"] = results.loc["NetExposure"]
        if "AbsExposure" in fields:
            kwargs["abs_exposures"] = results.loc["AbsExposure"]
        if "TotalHoldings" in fields:
            kwargs["total_holdings"] = results.loc["TotalHoldings"]
        if "Turnover" in fields:
            kwargs["turnover"] = results.loc["Turnover"]
        if "Commission" in fields:
            kwargs["commissions"] = results.loc["Commission"]
        if "CommissionAmount" in fields:
            kwargs["commission_amounts"] = results.loc["CommissionAmount"].astype(np.float64)
        if "Slippage" in fields:
            kwargs["slippages"] = results.loc["Slippage"]
        if "Benchmark" in fields:
            kwargs["benchmark"] = results.loc["Benchmark"]

        return cls(**kwargs)

    @classmethod
    def from_moonshot_csv(
        cls,
        filepath_or_buffer: Union[str, TextIO],
        start_date: str = None,
        end_date: str = None,
        trim_outliers: float = None,
        how_to_aggregate: dict[str, str] = None,
        riskfree: float = 0,
        compound: bool = True,
        rolling_sharpe_window: int = 200
        ) -> 'DailyPerformance':
        """
        Creates a DailyPerformance instance from a Moonshot backtest results CSV.

        Parameters
        ----------
        filepath_or_buffer : str or file-like object
            filepath or file-like object of the CSV

        start_date : str (YYYY-MM-DD), optional
            truncate at this start date (otherwise include entire date range)

        end_date : str (YYYY-MM-DD), optional
            truncate at this end date (otherwise include entire date range)

        trim_outliers: int or float, optional
            discard returns that are more than this many standard deviations from
            the mean. Useful for dealing with data anomalies that cause large
            spikes in plots.

        how_to_aggregate : dict, optional
            a dict of {fieldname: aggregation method} specifying how to aggregate
            fields from intraday to daily. See the docstring for
            `moonchart.utils.intraday_to_daily` for more details.

        riskfree : float, optional
            the riskfree rate (default 0)

        compound : bool
             True for compound/geometric returns, False for arithmetic returns (default True)

        rolling_sharpe_window : int, optional
            compute rolling Sharpe over this many periods (default 200)

        Returns
        -------
        DailyPerformance

        Examples
        --------
        Plot cumulative returns:

        >>> perf = DailyPerformance.from_moonshot_csv("backtest_results.csv")
        >>> perf.cum_returns.plot()
        """
        try:
            results = read_moonshot_csv(filepath_or_buffer)
        except ValueError as e:
            # "ValueError: 'Date' is not in list" might mean the user passed
            # a paramscan csv by mistake
            if "Date" not in repr(e):
                raise
            results = pd.read_csv(filepath_or_buffer)
            if "StrategyOrDate" in results.columns:
                raise MoonchartError("this looks like a parameter scan CSV, please use ParamscanTearsheet.from_csv")
            else:
                raise

        return cls._from_moonshot_or_pnl(
            results,
            start_date=start_date,
            end_date=end_date,
            trim_outliers=trim_outliers,
            how_to_aggregate=how_to_aggregate,
            riskfree=riskfree,
            compound=compound,
            rolling_sharpe_window=rolling_sharpe_window)

    @classmethod
    def from_pnl_csv(
        cls,
        filepath_or_buffer: Union[str, TextIO],
        start_date: str = None,
        end_date: str = None,
        trim_outliers: float = None,
        how_to_aggregate: dict[str, str] = None,
        riskfree: float = 0,
        compound: bool = True,
        rolling_sharpe_window: int = 200
        ) -> 'DailyPerformance':
        """
        Creates a DailyPerformance instance from a PNL CSV.

        Parameters
        ----------
        filepath_or_buffer : str or file-like object
            filepath or file-like object of the CSV

        start_date : str (YYYY-MM-DD), optional
            truncate at this start date (otherwise include entire date range)

        end_date : str (YYYY-MM-DD), optional
            truncate at this end date (otherwise include entire date range)

        trim_outliers: int or float, optional
            discard returns that are more than this many standard deviations from the mean

        how_to_aggregate : dict, optional
            a dict of {fieldname: aggregation method} specifying how to aggregate
            fields from intraday to daily. See the docstring for
            `moonchart.utils.intraday_to_daily` for more details.

        riskfree : float, optional
            the riskfree rate (default 0)

        compound : bool
             True for compound/geometric returns, False for arithmetic returns (default True)

        rolling_sharpe_window : int, optional
            compute rolling Sharpe over this many periods (default 200)

        Returns
        -------
        DailyPerformance

        Examples
        --------
        Plot cumulative returns:

        >>> perf = DailyPerformance.from_pnl_csv("pnl.csv")
        >>> perf.cum_returns.plot()
        """
        results = read_pnl_csv(filepath_or_buffer)

        return cls._from_moonshot_or_pnl(
            results,
            start_date=start_date,
            end_date=end_date,
            trim_outliers=trim_outliers,
            how_to_aggregate=how_to_aggregate,
            riskfree=riskfree,
            compound=compound,
            rolling_sharpe_window=rolling_sharpe_window)

    @property
    def cum_returns(self) -> pd.DataFrame:
        """a DataFrame of cumulative returns"""

        if self._cum_returns is None:
            self._cum_returns = get_cum_returns(self.returns, compound=self.compound)

        return self._cum_returns

    @property
    def cum_commissions(self) -> pd.DataFrame:
        """a DataFrame of cumulative commissions, as a proportion of capital"""

        if self._cum_commissions is None and self.commissions is not None:
            self._cum_commissions = get_cum_returns(self.commissions, compound=False)

        return self._cum_commissions

    @property
    def cum_commission_amounts(self) -> pd.DataFrame:
        """a DataFrame of cumulative commission amounts, in the base currency"""

        if self._cum_commission_amounts is None and self.commission_amounts is not None:
            self._cum_commission_amounts = self.commission_amounts.cumsum()

        return self._cum_commission_amounts

    @property
    def cum_slippages(self) -> pd.DataFrame:
        """a DataFrame of cumulative slippages, as a proportion of capital"""

        if self._cum_slippages is None and self.slippages is not None:
            self._cum_slippages = get_cum_returns(self.slippages, compound=False)

        return self._cum_slippages

    @property
    def cagr(self) -> 'pd.Series[float]':
        """a Series of CAGR values"""
        if self._cagr is None:
            self._cagr = get_cagr(self.cum_returns, compound=self.compound)

        return self._cagr

    @property
    def sharpe(self) -> 'pd.Series[float]':
        """a Series of Sharpe ratios"""
        if self._sharpe is None:
            self._sharpe = get_sharpe(self.returns, riskfree=self.riskfree)

        return self._sharpe

    @property
    def rolling_sharpe(self) -> pd.DataFrame:
        """a DataFrame of rolling Sharpe ratios"""
        if self._rolling_sharpe is None:
            self._rolling_sharpe = get_rolling_sharpe(
                self.returns,
                window=self.rolling_sharpe_window,
                riskfree=self.riskfree)

        return self._rolling_sharpe

    @property
    def drawdowns(self) -> pd.DataFrame:
        """a DataFrame of drawdowns"""
        if self._drawdowns is None:
            self._drawdowns = get_drawdowns(self.cum_returns)

        return self._drawdowns

    @property
    def max_drawdown(self) -> float:
        """the maximum drawdown"""
        return self.drawdowns.min()

    @property
    def cum_pnl(self) -> pd.DataFrame:
        """a DataFrame of cumulative PNL"""
        if self._cum_pnl is None and self.pnl is not None:
            self._cum_pnl = self.pnl.cumsum()

        return self._cum_pnl

    @property
    def benchmark_returns(self) -> 'pd.Series[float]':
        """
        Returns a Series of benchmark returns from the DataFrame of benchmark
        returns, if any. If more than one strategy/column has benchmark
        returns, uses the first.
        """
        if self._benchmark_returns is not None:
            return self._benchmark_returns

        if self._benchmark is None:
            return None

        have_benchmarks = (self._benchmark.fillna(0) != 0).any(axis=0)
        have_benchmarks = have_benchmarks[have_benchmarks]
        if have_benchmarks.empty:
            return None

        col = have_benchmarks.index[0]
        if len(have_benchmarks.index) > 1:
            import warnings
            warnings.warn("Multiple benchmarks found, only using first ({0})".format(col))

        self._benchmark_returns = self._benchmark[col]
        self._benchmark_returns.name = "benchmark"

        return self._benchmark_returns

    @property
    def benchmark_cum_returns(self) -> 'pd.Series[float]':
        """Cumulative benchmark returns"""

        if self._benchmark_cum_returns is None and self._benchmark_returns is not None:
            self._benchmark_cum_returns = get_cum_returns(self._benchmark_returns, compound=True)

        return self._benchmark_cum_returns

class AggregateDailyPerformance(DailyPerformance):
    """
    Class representing aggregate daily performance.

    Given a DailyPerformance instance containing multi-column (that is,
    multi-strategy or detailed single-strategy) DataFrames, this class
    represents the aggregate performance.

    Parameters
    ----------
    performance : DailyPerformance, required
        daily performance results to aggregate

    trim_outliers: int or float, optional
        discard returns that are more than this many standard deviations from the mean
        (copied from DailyPerformance if omitted)

    riskfree : float, optional
        the riskfree rate (copied from DailyPerformance if omitted)

    compound : bool
         True for compound/geometric returns, False for arithmetic returns (copied from
         DailyPerformance if omitted)

    rolling_sharpe_window : int, optional
        compute rolling Sharpe over this many periods (copied from DailyPerformance if
        omitted)

    Returns
    -------
    AggregatePerformance

    Examples
    --------
    Plot aggregate cumulative returns:

    >>> perf = DailyPerformance.from_moonshot_csv("backtest_results.csv")
    >>> agg_perf = AggregateDailyPerformance(perf)
    >>> agg_perf.cum_returns.plot()
    """

    def __init__(
        self,
        performance: DailyPerformance,
        riskfree: float = None,
        compound: bool = None,
        rolling_sharpe_window: int = None,
        trim_outliers: float = None
        ):

        if riskfree is None:
            riskfree = performance.riskfree
        if compound is None:
            compound = performance.compound
        if rolling_sharpe_window is None:
            rolling_sharpe_window = performance.rolling_sharpe_window
        if trim_outliers is None:
            trim_outliers = performance._trim_outliers

        super(AggregateDailyPerformance, self).__init__(
            performance.returns.sum(axis=1),
            riskfree=riskfree,
            compound=compound,
            rolling_sharpe_window=rolling_sharpe_window,
            benchmark=performance._benchmark,
            trim_outliers=trim_outliers
        )
        if performance.pnl is not None:
            self.pnl: 'pd.Series[float]' = performance.pnl.sum(axis=1)
            """a Series of aggregate PNL"""

        if performance.commission_amounts is not None:
            self.commission_amounts: 'pd.Series[float]' = performance.commission_amounts.sum(axis=1)
            """a Series of aggregate commission amounts, in the base currency"""

        if performance.commissions is not None:
            self.commissions: 'pd.Series[float]' = performance.commissions.sum(axis=1)
            """a Series of aggregate commissions, as a proportion of capital"""

        if performance.slippages is not None:
            self.slippages: 'pd.Series[float]' = performance.slippages.sum(axis=1)
            """a Series of aggregate slippages, as a proportion of capital"""

        if performance.net_exposures is not None:
            self.net_exposures: 'pd.Series[float]' = performance.net_exposures.sum(axis=1)
            """a Series of aggregate net exposures"""

        if performance.abs_exposures is not None:
            self.abs_exposures: 'pd.Series[float]' = performance.abs_exposures.sum(axis=1)
            """a Series of aggregate absolute exposures"""

        if performance.total_holdings is not None:
            self.total_holdings: 'pd.Series[float]' = performance.total_holdings.sum(axis=1)
            """a Series of aggregate total holdings"""

        if performance.turnover is not None:
            self.turnover: 'pd.Series[float]' = performance.turnover.sum(axis=1)
            """a Series of aggregate turnover"""
