import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image
import plotly.graph_objects as go
from streamlit_extras.switch_page_button import switch_page
 
st.set_page_config(page_title='ESG Insights')
# st.header()

df = pd.read_csv('yfinance2.csv')
# st.dataframe(df)

# selected_company = st.selectbox('Select a company', df['Name'])
selected_company=st.session_state["my_input"]
st.header(selected_company)
info=df.loc[df['Name'] == selected_company, 'Description'].iloc[0]
st.subheader(info)

st.subheader('ESG Score')

esg_score=df.loc[df['Name'] == selected_company, 'Total ESG Score'].iloc[0]

fig = go.Figure(go.Indicator(
    mode = "gauge+number",
    value = esg_score,
    domain = {'x': [0, 1], 'y': [0, 1]},
    title = {'text': "ESG Score"},gauge={'axis':{'range':[None,50]},}))


st.plotly_chart(fig, theme="streamlit",use_container_width=False )

# st.write(df.loc[df['Name'] == selected_company])
companyEsgE = df.loc[df['Name'] == selected_company]['Environment Score'].iloc[0]
companyEsgS = df.loc[df['Name'] == selected_company]['Social Score'].iloc[0]
companyEsgG = df.loc[df['Name'] == selected_company]['Governance Score'].iloc[0]

with open("pages/style.css") as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

col1, col2, col3, = st.columns(3)

with col1:
    st.metric(label="Environment Score", value=companyEsgE, delta="")

with col2:
    st.metric(label="Social Score", value=companyEsgS, delta="")

with col3:
    st.metric(label="Governance Score", value=companyEsgG,delta="")

st.subheader('Controversy Score:')
controversyScore = df.loc[df['Name'] == selected_company]['Controversy Score'].iloc[0]
Controversy=df.loc[df['Name'] == selected_company]['Controversy Assessment'].iloc[0]

fig1 = go.Figure(go.Indicator(
    mode = "number+gauge",
    gauge = {'shape': "bullet"},
    value=controversyScore,
    domain = {'x': [0.1,1], 'y': [0.2, 0.9]},))
st.subheader(Controversy)

st.plotly_chart(fig1, theme="streamlit",use_container_width=False )

sector=df.loc[df['Name'] == selected_company]['Sector'].iloc[0]

df1=pd.read_excel('yfinance2.xlsx',usecols='A,C:H')
peers=df1.loc[df1['Sector']==sector]
peers=peers.head(5)
st.subheader('Peer Comparison')

symbol = df.loc[df['Name'] == selected_company]['Symbols'].iloc[0]
st.dataframe(peers)
if "symmbol" not in st.session_state:
    st.session_state["symbol"]=""
#
# my_input = st.text_input("Search Companies",st.session_state["my_input"])
bar = st.button("Risk Analysis")
if bar:
    st.session_state["symbol"] = symbol
    switch_page('Riskforcast')