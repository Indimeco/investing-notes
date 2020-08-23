# Investing Notes
Small jupyter notebook where I might run some silly experiments mostly around analysing stock information based on a given portfolio.

Right now, only one analytical path is available: reversionToMean

# Reversion To Mean
## Description
The goal of this path is to provide a minimal, rough insight into expected returns from the individual entries in a portfolio of stocks.

This is based on the assumption that stock prices, given a long enough timeline, have a tendency to regress towards the mean, plus or minus a small amount. [Read more](https://www.investopedia.com/terms/m/meanreversion.asp)

However, it has a bias towards recent stock history rather than complete history. The time specified, for example five years, uses the mean price of the first year as the base price and averages all of the remaining years, four years, to produce the given visuals. 

## Input
This tool reads from portfolio.json if it exists or portfolioSample.json if it does not
Both of these json inputs must follow the type definition
```
class PortfolioItem(TypedDict):
    ticker: str
    friendlyName: str
    amount: int
Portfolio = List[PortfolioItem]
```
for example
```json
[
	{ "ticker": "AMZN",    "friendlyName": "AMAZON",  "amount": 15000 },
	{ "ticker": "SPLK",    "friendlyName": "SPLUNK",  "amount": 15000 }
]
```

Additionally, most control variables exist in the first cell
e.g., the time period over which to include in calculations

## Processing and Collection
This tool leverages [yfinance](https://github.com/ranaroussi/yfinance) to pull stock information over the historical period given.
Alternative colleciton is available from the AlphaVantage API. Other APIs may be considered for inclusion later depending on availability.
