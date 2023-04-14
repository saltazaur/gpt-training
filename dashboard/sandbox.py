import streamlit as st
import openai
import json
import pandas as pd
from db import get_database_schema, extract_schema_str, execute_query, get_cols_from_query, test_query, format_database_schema

def run_app():

    default_schema = """### MySQL tables, with their properties:
# customers (customerNumber, customerName, contactLastName, contactFirstName, phone, addressLine1, addressLine2, city, state, postalCode, country, salesRepEmployeeNumber, creditLimit,)
# employees (employeeNumber, lastName, firstName, extension, email, officeCode, reportsTo, jobTitle,)
# offices (officeCode, city, phone, addressLine1, addressLine2, state, country, postalCode, territory,)
# orderdetails (orderNumber, productCode, quantityOrdered, priceEach, orderLineNumber,)
# orders (orderNumber, orderDate, requiredDate, shippedDate, status, comments, customerNumber,)
# payments (customerNumber, checkNumber, paymentDate, amount,)
# productlines (productLine, textDescription, htmlDescription, image,)
# products (productCode, productName, productLine, productScale, productVendor, productDescription, quantityInStock, buyPrice, MSRP,)"""

    connect_db = st.button('Get schema')

    if connect_db:

        #Try connect to local database if not we have hardcoded string
        try:
            database_schema_string = format_database_schema()

        except Exception as e:
            st.warning(f'Could not connect to database, reason: {e}')

            database_schema_string = default_schema
    else:
        database_schema_string = default_schema

    st.markdown("<p style='text-align:Left ;font-family:Graphik;font-weight: bold;color:hsl(0, 100%, 0%); font-size:30px;'>Natural Language to SQL engine based on GPT-3 DEMO</p>",unsafe_allow_html=True)
    
    st.write("")
    st.write("")

    form_1  = st.form(key="something_unique")
    left, right = form_1.columns([4, 1])

    with left:
        database_structure = st.text_area("database structure: ",value=database_schema_string, height=410)
    start_phrase = database_structure+"/n/n"+ form_1.text_area("please write your request here: ",value="A query to get the product names and codes that were ordered before date 20220402", height=50)
    start_phrase = start_phrase + "\nSELECT"

    with right:
        st.write("   Tuning:")
        st.write("___")

        #model = st.number_input("Model", min_value=2, max_value=3, value=3)
        model = st.selectbox('Model',('gpt-3.5-turbo','text-davinci-003', 'text-embedding-ada-002'))
        temperature = st.number_input("Temperature", min_value=.0, max_value=1., value=.7, step=.01)
        max_tokens = st.number_input("Max_tokens", min_value=50, value=250)
    
    get_query = form_1.form_submit_button("Get query")

    if get_query:
        with st.spinner("Generating query..."):
            query_ = openai.Completion.create(
                            model=model,  # The name of the GPT-3 language model to use
                            prompt=start_phrase,  # The initial text prompt to generate text from
                            temperature=temperature,  # Controls the randomness and creativity of the generated text
                            max_tokens=max_tokens,  # The maximum length of the generated text in terms of tokens (words or symbols)
                            )
            query_ = "SELECT " + query_["choices"]["text"]
            with open('temp/last_query.txt','w') as f:
                f.write(query_)
            
            # Save result to session state, to display it again upon query execution
            st.session_state.last_generated_query = query_
            code_raw = st.code(f"{query_}")

    run_btn = st.button(label='Run query to database')
    if run_btn:
        query_ = st.session_state.last_generated_query
        code_raw = st.code(f"{query_}")

        #Try to show results from database
        try:
            rez = execute_query(query_)
            col_l = get_cols_from_query(query_)
            try:
                df = pd.DataFrame(columns=col_l, data=rez)
                st.dataframe(df)
            except Exception as e:
                st.warning(f'Could not show result as dataframe, reason: {e}')
                st.write(rez)

        except Exception as e:
            st.warning(f'Could not fetch results from database, reason: {e}')
