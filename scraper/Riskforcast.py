import csv
import yfinance as yf
import numpy as np
import pandas as pd
import sklearn.linear_model
import os

# Read the CSV file with a column of company symbols
with open("updated_dataset.csv", "r") as file:
    reader = csv.reader(file)
    next(reader)  # Skip the header row
    company_symbols = [row[1] for row in reader]

# Define threshold values for each metric category
std_dev_thresholds = {
    "low": 0.0,
    "medium": 0.5,
    "high": 1.0
}

beta_thresholds = {
    "low": 0.5,
    "medium": 1.0,
    "high": 1.5
}

var_thresholds = {
    "low": -0.02,
    "medium": -0.05,
    "high": -0.1
}

# Loop through each company symbol
for company_symbol in company_symbols:
    print(company_symbol)
    # Retrieve the stock symbol for the specified company
    stock_info = yf.Ticker(company_symbol).info
    stock_symbol = stock_info["symbol"]

    # Download historical price data for the specified stock symbol
    stock_data = yf.download(stock_symbol, start="2018-01-01", end="2022-12-31")

    # Calculate daily returns based on the closing prices
    stock_data["Return"] = stock_data["Close"].pct_change()

    # Remove missing or NaN values from the datasets
    market_returns = market_data["Close"].pct_change().dropna().values.reshape(-1, 1)
    stock_returns = stock_data["Return"].dropna().values.reshape(-1, 1)

    # Check if the lengths of the datasets are consistent
    if len(market_returns) != len(stock_returns):
        print("Inconsistent number of samples. Adjusting the datasets.")

        # Remove excess samples from the longer dataset
        min_length = min(len(market_returns), len(stock_returns))
        market_returns = market_returns[:min_length]
        stock_returns = stock_returns[:min_length]

    # Perform linear regression with the adjusted datasets
    regression_model = LinearRegression().fit(market_returns, stock_returns)
    beta = regression_model.coef_[0][0]

    # Perform VaR analysis
    confidence_level = 0.95
    returns_sorted = np.sort(stock_data["Return"].dropna().values)
    var = returns_sorted[int((1 - confidence_level) * len(returns_sorted))]

    # Get P/E Ratio and Debt-to-Equity Ratio
    pe_ratio = stock_info.get("trailingPE", "N/A")
    debt_to_equity = stock_info.get("debtToEquity", "N/A")

    # Assign labels based on threshold values
    std_dev_label = max(std_dev_thresholds, key=lambda x: std_dev_thresholds[x] <= std_dev_label)
    beta_label = max(beta_thresholds, key=lambda x: beta_thresholds[x] <= beta)
    var_label = max(var_thresholds, key=lambda x: var_thresholds[x] <= var)

       # Save risk forecast data to a CSV file
    filename = "risk_forecast.csv"
    file_exists = os.path.isfile(filename)
    with open(filename, "a") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Company Name", "Stock Symbol", "Standard Deviation", "Beta", "Value at Risk", "P/E Ratio", "Debt-to-Equity Ratio",
                         "Standard Deviation Label", "Beta Label", "Value at Risk Label"])
        writer.writerow([stock_info["longName"], stock_symbol, std_dev_label, beta, var, pe_ratio, debt_to_equity, std_dev_label, beta_label, var_label])

    # Print the risk forecast analysis
    print("Risk Forecast for", stock_info["longName"])
    print("Stock Symbol:", stock_symbol)
    print("Standard Deviation:", std_dev_label)
    print("Beta:", beta)
    print("Value at Risk (VaR) at", confidence_level, "confidence level:", var)
    print("P/E Ratio:", pe_ratio)
    print("Debt-to-Equity Ratio:", debt_to_equity)
    print("Standard Deviation Label:", std_dev_label)
    print("Beta Label:", beta_label)
    print("Value at Risk Label:", var_label)
    print()  # Add a new line between companies