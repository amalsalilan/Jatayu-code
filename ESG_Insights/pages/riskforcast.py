import pandas as pd
import streamlit as st
import plotly.graph_objects as go
hide_st_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
"""

st.markdown(hide_st_style, unsafe_allow_html=True)

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

    # Customize the appearance of the gauge charts
    gauge_colors = ["#5ee432", "#f9c74f", "#ff0000"]  # Green, Yellow, Red
    gauge_titles = ["Standard Deviation", "Beta", "Value at Risk"]
    gauge_ranges = [[0, 5], [0, 5], [0, 5]]

    fig = go.Figure()
    for i, value in enumerate([float(Standard_Deviation), float(Beta), float(Value_at_Risk)]):
        fig.add_trace(go.Indicator(
            mode="gauge+number",
            value=value,
            domain={'x': [0, 1], 'y': [i * 0.3 + 0.1, (i + 1) * 0.3]},
            title={'text': gauge_titles[i]},
            gauge={
                'axis': {'range': gauge_ranges[i]},
                'bar': {'color': gauge_colors[i]},
                'steps': [
                    {'range': [0, gauge_ranges[i][1] * 0.3], 'color': '#e8edea'},
                    {'range': [gauge_ranges[i][1] * 0.3, gauge_ranges[i][1] * 0.7], 'color': '#b7e9a5'},
                    {'range': [gauge_ranges[i][1] * 0.7, gauge_ranges[i][1]], 'color': '#5ee432'}
                ],
                'threshold': {
                    'line': {'color': 'red', 'width': 4},
                    'thickness': 0.75,
                    'value': gauge_ranges[i][1] * 0.7
                }
            }
        ))

    # Update the figure layout to add spacing between charts and make titles visible
    fig.update_layout(
        height=800,  # Adjust the height to make the charts more visible
        margin=dict(l=50, r=50, t=50, b=50),  # Add margins around the charts
        grid=dict(rows=3, columns=1, pattern="independent"),  # Separate charts into individual rows
        showlegend=False,  # Hide the legend
        title_x=0.5,  # Center the title
        title_y=0.98,  # Adjust the vertical position of the title
        title_text="Risk Metrics",  # Add a common title for all charts
        title_font=dict(size=24)  # Customize the title font size
    )

    st.plotly_chart(fig, theme="streamlit", use_container_width=False)
else:
    st.error("Invalid Stock Symbol")
