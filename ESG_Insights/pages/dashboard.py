import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image
import plotly.graph_objects as go
from streamlit_extras.switch_page_button import switch_page

hide_st_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
"""

st.markdown(hide_st_style, unsafe_allow_html=True)

df = pd.read_csv('pages/yfinance2.csv')

selected_company = st.session_state["my_input"]

st.header(selected_company)
info = df.loc[df['Name'] == selected_company, 'Description'].iloc[0]
st.subheader(info)

st.subheader('ESG Score')

esg_score = df.loc[df['Name'] == selected_company, 'Total ESG Score'].iloc[0]

fig = go.Figure(go.Indicator(
    mode="gauge+number",
    value=esg_score,
    domain={'x': [0, 1], 'y': [0, 1]},
    title={'text': "ESG Score"},
    gauge={'axis': {'range': [None, 50]}}
))

st.plotly_chart(fig, theme="streamlit", use_container_width=False)

companyEsgE = df.loc[df['Name'] == selected_company]['Environment Score'].iloc[0]
companyEsgS = df.loc[df['Name'] == selected_company]['Social Score'].iloc[0]
companyEsgG = df.loc[df['Name'] == selected_company]['Governance Score'].iloc[0]

gauge_colors = ["#5ee432", "#f9c74f", "#ff0000"]  # Green, Yellow, Red
gauge_titles = ["Environment Score", "Social Score", "Governance Score"]
gauge_ranges = [[0, 50], [0, 50], [0, 50]]

fig1 = go.Figure()

fig1.update_layout(
    height=1000,
    margin=dict(l=50, r=50, t=50, b=50),
    grid=dict(rows=3, columns=1, pattern="independent"),
    showlegend=False,
    title_x=0.5,
    title_y=0.98,
    title_text="",
    title_font=dict(size=34)
)

for i, value in enumerate([float(companyEsgE), float(companyEsgS), float(companyEsgG)]):
    fig1.add_trace(go.Indicator(
        mode="gauge+number",
        value=value,
        domain={'x': [0, 1], 'y': [i * 0.35 + 0.05, (i + 1) * 0.35 - 0.05]},
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

st.plotly_chart(fig1, theme="streamlit", use_container_width=False)

sector = df.loc[df['Name'] == selected_company]['Sector'].iloc[0]

df1 = pd.read_excel('pages/yfinance2.xlsx', usecols='A,C:H')
peers = df1.loc[df1['Sector'] == sector].head(5)

st.subheader('Peer Comparison')
st.dataframe(peers)
symbol = df.loc[df['Name'] == selected_company]['Symbols'].iloc[0]
if "symbol" not in st.session_state:
    st.session_state["symbol"] = ""

bar = st.button("Risk Analysis")

if bar:
    st.session_state["symbol"] = symbol
    switch_page('riskforcast')


