import streamlit as st
from streamlit_option_menu import option_menu

def sidebar_menu(): 

    #removing the streamlit brandingin the page
    hide_streamlit_style = """ <style> #MainMenu {visibility: hidden;} footer {visibility: hidden;} </style> """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    # 1. as sidebar menu
    with st.sidebar:
        
        selected = option_menu("Main Menu", ["Home", 'Sandbox'],
                                             icons=['house', 'gear',], menu_icon="list", default_index=0)
        
        if selected == "Home":
            return "home"
        
        if selected == "Sandbox":
            return "sandbox"
        
