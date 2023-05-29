import pandas as pd
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from PIL import Image
hide_st_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
"""

st.markdown(hide_st_style, unsafe_allow_html=True)

# Rest of your Streamlit app code goes here


# Define Streamlit app
# st.set_page_config(page_title="ESG Insights")
# st.title("ESG Insights")

# Load CSV file
# set_background_image()
df = pd.read_csv('pages/yfinance2.csv')
selected_company = st.selectbox('Select a company', df['Name'].unique())

# Define function to check if input value is in the CSV file
def check_input(input_value):
    return df['Name'].str.contains(input_value, case=False, regex=True).any()


# Create input field
if "selected_company" not in st.session_state:
    st.session_state["selected_company"]=""

submit=st.button("Search")
# Check input value and redirect to dashboard if value is found in CSV file
if submit:
    st.session_state["my_input"]=selected_company
    st.write("You Have entered",selected_company)
    switch_page('dashboard')

image = Image.open('pages/ratings.png')
st.header("ESG methadology")
st.subheader(" ESG Risk Ratings measure a company’s ,exposure to industry-specific material ESG risks and how well a company is managing those risks. ")
st.image(image)