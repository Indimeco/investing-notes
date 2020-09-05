import pandas as pd
import numpy as np
import datetime
import functools
from config import Portfolio, PortfolioInfo, EquityItem
from downloadEquities import getDataFileName


def parsePortfolio(
    portfolio: Portfolio,
    useDataOverYears: int,
    endDate: datetime,
) -> PortfolioInfo:
    portfolioEquities = portfolio["equities"]
    portfolioOther = portfolio["other"]

    portfolioEquityMeans = []
    for entry in portfolioEquities:
        portfolioEquityMeans.append(
            parseStockDataFrame(
                pd.read_json(getDataFileName(entry["ticker"])),
                entry,
                getPortfolioWeight(portfolio, entry["name"]),
                useDataOverYears,
                endDate,
            )
        )

    portfolioOtherMapped = []
    for entry in portfolioOther:
        portfolioOtherMapped.append(
            {
                **entry,
                "weight": getPortfolioWeight(portfolio, entry["name"]),
                "sharePriceChangePerAnnum": entry["changePerAnnum"],
                "estimatedDividendsPerAnnum": 0,
                "estimatedDividendBonusToChange": 0,
            }
        )

    portfolioDf = pd.concat(
        [pd.DataFrame(portfolioEquityMeans), pd.DataFrame(portfolioOtherMapped)]
    )
    portfolioDf["weightedReturnPerAnnum"] = (
        portfolioDf["weight"] * portfolioDf["changePerAnnum"]
    )
    return portfolioDf


def getPortfolioWeight(portfolio: Portfolio, name: str) -> float:
    allItems = []

    # flatten portfolio
    for key, value in portfolio.items():
        allItems.extend(value)

    portfolioSum = functools.reduce(lambda acc, curr: acc + curr["amount"], allItems, 0)
    itemVal = 0
    for item in allItems:
        if item["name"] == name:
            itemVal = item["amount"]

    return itemVal / portfolioSum


def percentOfDifference(x):
    current = x.iloc[-1]
    previous = x.iloc[0]
    print(f"previous: {previous} ::: current {current}")

    return current - previous


def parseStockDataFrame(
    df: pd.DataFrame,
    portfolioEntry: EquityItem,
    weight: float,
    useDataOverYears: int,
    endDate: datetime,
) -> PortfolioInfo:
    # initialise fundamental dates
    minDate = df.index[0]
    maxDate = endDate - datetime.timedelta(weeks=useDataOverYears * 52)
    fromDate = maxDate if maxDate >= minDate else minDate

    relevantDf = df[df.index > fromDate.isoformat()]

    closes = relevantDf["Adj Close"]
    differences = []
    # this is pretty inefficient for pandas, I'm aware
    # but I don't know how else we can get a rolling difference
    for i, day in enumerate(closes):
        previous = closes[i - 1]
        current = closes[i]
        if i == 0:
            differences.append(0)
        elif not pd.isna(previous) and not pd.isna(current):
            diff = (current - previous) / previous
            differences.append(diff)
        else:
            raise Exception("NAN in data")

    sharePriceChangePerAnnum = (
        np.mean(differences) * 253
    )  # about ~253 working days in a year

    # add dividends to profit
    dividendProfits = relevantDf["Dividends"].sum()
    assumedShares = portfolioEntry["amount"] / relevantDf["Adj Close"].mean()
    dividendProfitPerAnnum = (dividendProfits * assumedShares) / useDataOverYears
    dividendReturnPerAnnum = dividendProfitPerAnnum / portfolioEntry["amount"]

    totalChangePerAnnum = sharePriceChangePerAnnum + dividendReturnPerAnnum

    return {
        "name": portfolioEntry["name"],
        "weight": weight,
        "fromDate": fromDate,
        "toDate": endDate,
        "amount": portfolioEntry["amount"],
        "sharePriceChangePerAnnum": sharePriceChangePerAnnum,
        "estimatedDividendsPerAnnum": dividendProfitPerAnnum,
        "estimatedDividendBonusToChange": dividendReturnPerAnnum,
        "changePerAnnum": totalChangePerAnnum,
    }
