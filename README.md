# Investing Notes
Small jupyter notebook where I might run some silly experiments mostly around analysing stock information based on a given portfolio.

Right now, only one analytical path is available: reversionToMean

# Reversion To Mean
## Description
The goal of this path is to provide a minimal, rough insight into expected returns from the individual entries in a portfolio of stocks.

This is based on the assumption that stock prices, given a long enough timeline, have a tendency to regress towards the mean, plus or minus a small amount. [Read more](https://www.investopedia.com/terms/m/meanreversion.asp)

## Input
This tool reads from the `portfolioFilePath` if it exists or `./portfolioSample.json` if it does not
See the [Portfolio Sample](./portfolioSample.json) for example inputs 
Control variables exist in the first cell to be customized 

## Processing and Collection
This tool leverages [yfinance](https://github.com/ranaroussi/yfinance) to pull stock information over the historical period given.
Alternative colleciton is available from the AlphaVantage API. Other APIs may be considered for inclusion later depending on availability.
