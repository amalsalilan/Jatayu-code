import pandas as pd
import streamlit as st
import plotly.graph_objects as go

df = pd.read_csv('pages/risk_forecast.csv', encoding='unicode_escape')
Stock = st.session_state["symbol"]
st.header(Stock)
st.subheader("""To calculate the risk metrics in the provided code, the following inputs are used:
    1. Stock Symbol:
        ◦ The user is prompted to enter the stock symbol for which they want to calculate the risk metrics.
        ◦ The stock symbol is used to retrieve the historical price data and other information for the specified stock.
    2. Historical Price Data:
        ◦ The yf.download function from the yfinance library is used to retrieve the historical price data for the specified stock.
        ◦ The start and end parameters are set to define the time period for which the data is retrieved (from January 1, 2022, to January 1, 2023).""")
st.subheader("""Based on the stock symbol and historical price data, the following risk metrics are calculated:
    1. Standard Deviation:
        ◦ The standard deviation of the stock's returns is calculated using the "Close" price data.
        ◦ The returns are calculated as the percentage change in the closing prices over time.
    2. Beta:
        ◦ The beta value is obtained from the info dictionary of the yf.Ticker(stock_symbol) object.
        ◦ Beta measures the sensitivity of the stock's price movements compared to the overall market.
        ◦ If the "beta" key is not available in the info dictionary, it is assigned as "N/A" to handle cases where beta information is not provided for a stock.
    3. Value at Risk (VaR):
        ◦ VaR is calculated as the quantile of the stock's return distribution.
        ◦ The quantile is determined by subtracting the confidence level (0.95) from 1 and finding the corresponding percentile of the returns.
        ◦ This quantile represents the potential loss that is not expected to be exceeded with 95% confidence.
   These inputs and calculations allow for the assessment of risk associated with the specified stock symbol based on historical price data and statistical measures.""")
if not df.empty and df['Symbols'].eq(Stock).any():
    Standard_Deviation = df.loc[df['Symbols'] == Stock, 'Standard Deviation'].iloc[0]
    Beta = df.loc[df['Symbols'] == Stock, 'Beta'].iloc[0]
    Value_at_Risk = df.loc[df['Symbols'] == Stock, 'Value at Risk'].iloc[0]

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=float(Standard_Deviation),
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Standard_Deviation"},gauge={'axis':{'range':[None,5]},}))

    st.plotly_chart(fig, theme="streamlit", use_container_width=False)

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=float(Beta),
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Beta"},gauge={'axis':{'range':[None,5]},}))

    st.plotly_chart(fig, theme="streamlit", use_container_width=False)

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=float(Value_at_Risk),
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Value_at_Risk"},gauge={'axis':{'range':[None,5]},}))

    st.plotly_chart(fig, theme="streamlit", use_container_width=False)
else:
    st.error("Invalid Stock Symbol")