# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write("Choose the fruits you want in your customer Smoothie!")

name_on_order = st.text_input('Name on Smoothie')
st.write("The name on your Smoothie will be:", name_on_order)

# Get active Snowflake session
cnx = st.connection("snowflake")
session = cnx.session()

# Get fruit options
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

# Multiselect for ingredients
ingredients_list = st.multiselect('Choose up to 5 ingredients:', my_dataframe)


ingredients_list = ['apple', 'banana', 'cherry']  # Example ingredients list

ingredients_string = ""
for fruit_chosen in ingredients_list:
    ingredients_string += fruit_chosen + ' '
    st.subheader(f"{fruit_chosen} Nutrition Information")
    
    try:
        # Correct the typo here: smoothiefroot_response
        smoothiefroot_response = requests.get(f"https://my.smoothiefroot.com/api/fruit/{fruit_chosen}")
        
        # Check if the request was successful
        if smoothiefroot_response.status_code == 200:
            # Display the nutritional info in a table format (JSON data)
            st_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
        else:
            st.error(f"Failed to retrieve data for {fruit_chosen}. Status code: {smoothiefroot_response.status_code}")
        
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred while fetching data for {fruit_chosen}: {e}")
        
st.write("Selected Ingredients:", ingredients_string)

if ingredients_list:
    ingredients_string = ' '

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        st.subheader(fruit_chosen + ' Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit_chosen)
        st_df = st.dataframe(data=smoothiefroot_reponse.json(), use_container_width=True)

    st.write("Selected Ingredients:", ingredients_string)

    # Construct the SQL INSERT statement
    my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders (ingredients, name_on_order, order_filled, order_ts)
        VALUES ('{ingredients_string}', '{name_on_order}', FALSE, CURRENT_TIMESTAMP)
    """

    st.write("Final SQL Query: ", my_insert_stmt)  # Debugging step

    # Button to submit order
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")

if session is None:
    st.error("❌ Snowflake session is not active. Check connection settings.")

import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
