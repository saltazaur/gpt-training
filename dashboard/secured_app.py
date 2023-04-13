# streamlit_app.py

import streamlit as st

def check_password():

    st.set_page_config(page_title="ACN-GPT ",
                   page_icon='images/favicon_accenture.png',
                   layout="wide",
                   initial_sidebar_state="expanded"
                   )

    #removing the streamlit brandingin the page
    hide_streamlit_style = """ <style> #MainMenu {visibility: hidden;} footer {visibility: hidden;} </style> """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    print("Authentication")

    col1, _, col2= st.columns([1, 1, 1])
    col1.image('images/accenture_logo.png', width=250)
    col2.image('images/openai_logo.png', width=250)
    

    def password_entered():

        """Checks whether a password entered by the user is correct."""
        """Returns `True` if the user had a correct password."""
        
        if (
            st.session_state["username"] in st.secrets["passwords"]
            and st.session_state["password"] == st.secrets["passwords"][st.session_state["username"]]
        ):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store username + password
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False


    if "password_correct" not in st.session_state:
        # First run, show inputs for username + password.
        left_margin, workspace, right_margin = st.columns([1,1,1])
        workspace.text_input("Username", on_change=password_entered, key="username")
        workspace.text_input("Password", type="password", on_change=password_entered, key="password" )
        return False
    
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        left_margin, workspace, right_margin = st.columns([1,1,1])
        workspace.text_input("Username", on_change=password_entered, key="username")
        workspace.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
    
        return False
    else:
        # Password correct.
        return True



