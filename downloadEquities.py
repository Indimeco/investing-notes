import json
import yfinance as yf
import os.path
import pandas as pd
from config import PortfolioEquities


def getDataFileName(name: str) -> str:
    return f"data/{name}.json"


def convertDataFrameToJson(df: pd.DataFrame) -> any:
    return json.loads(df.to_json())


def writeJsonToFile(name: str, payload: any) -> None:
    filename = getDataFileName(name)
    with open(filename, "w") as outfile:
        json.dump(payload, outfile)

    print(f"{filename} saved!")


def getYFDataFrame(ticker: str, years: int) -> pd.DataFrame:
    dataframe = yf.download(
        ticker,
        period=str(years) + "y",
        prepost=True,
        interval="1d",  # none of the larger intervals seem to be consistent
        actions=True,
    )

    return dataframe


def downloadEquities(equities: PortfolioEquities, years: int, partial=True) -> None:
    for stock in equities:
        ticker = stock["ticker"]
        if not os.path.isfile(getDataFileName(ticker)) or not partial:
            print(f"Retreiving {ticker} information...")
            writeJsonToFile(
                ticker, convertDataFrameToJson(getYFDataFrame(ticker, years))
            )
        else:
            print(f"{ticker} already exists. Skipping download")