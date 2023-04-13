import streamlit as st
import secured_app 
import sb                       # refers to sidebar
import home
import sandbox


# Authentication check
if not secured_app.check_password():
    st.stop()
# User authenticated, we can proceed

# Load sidebar and pick page to render
side_bar =  sb.sidebar_menu()

if side_bar == "home":
    home.run_app()
elif side_bar == "sandbox":
    sandbox.run_app()

else:
    st.warning('not implemented yet')
