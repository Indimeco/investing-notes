from typing_extensions import TypedDict
from typing import List


class EquityItem(TypedDict):
    ticker: str
    name: str
    amount: int


class OtherItem(TypedDict):
    name: str
    amount: int
    fromDate: any
    toDate: any
    changePerAnnum: float


PortfolioEquities = List[EquityItem]
PortfolioOthers = List[OtherItem]


class Portfolio(TypedDict):
    equities: PortfolioEquities
    other: PortfolioOthers


class PortfolioInfo(TypedDict):
    name: str
    fromDate: any
    toDate: any
    changePerAnnum: float