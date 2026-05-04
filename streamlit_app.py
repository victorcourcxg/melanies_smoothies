# Import python packages
import streamlit as st
from snowflake.snowpark.functions import (col)
import requests

# Write directly to the app
st.title(f"Order app :cup_with_straw:")

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"))

name_on_order = st.text_input("Name on Smoothie:")

ingredients_list = st.multiselect("Choose up to 5 ingredients", my_dataframe, max_selections=5)

if ingredients_list:
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        st.subheader(fruit_chosen + " Nutrition Infos")
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit_chosen)
        sf_df = st.dataframe(smoothiefroot_response.json(), use_container_width=True)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
                    values ('""" + ingredients_string + """','""" + name_on_order + """')"""
    submit = st.button("Submit order")
    
    if submit:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
