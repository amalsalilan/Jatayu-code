import streamlit as st
from streamlit_extras.switch_page_button import switch_page

# Set page configuration
st.set_page_config(page_title="Login Page", initial_sidebar_state="collapsed")
hide_st_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
"""

st.markdown(hide_st_style, unsafe_allow_html=True)


# Create a session state object
session_state = st.session_state

# Define username and password
valid_username = "admin"
valid_password = "password"

# Check if user is logged in
if "is_logged_in" not in session_state:
    session_state.is_logged_in = False

# Show login page if not logged in
if not session_state.is_logged_in:
    st.title("Login Page")

    # Get username and password input
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if username and password:
        Login = st.button("Login")
        # Perform login validation
        if username == valid_username and password == valid_password:
            session_state.is_logged_in = True
            st.success("Logged in successfully!")

        else:
            st.error("Invalid username or password")
    else:
        st.warning("Please enter username and password")

# Show homepage if logged in
if session_state.is_logged_in:

    switch_page('homepage')
