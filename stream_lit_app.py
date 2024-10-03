# Import python packages
import streamlit as st
import requests
import pandas 
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
    """
    Choose the fruits you want in your custom Smoothie! \n
    """
)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

pd_df=my_dataframe.to_pandas()
st.dataframe(pd_df)
st.stop()

name_on_order = st.text_input("Name on Smoothie")
st.write("The name on smoothie is", name_on_order)

ingredients_list = st.multiselect('Choose up to 5 ingredients:',
                                  my_dataframe,
                                 max_selections = 5)
if ingredients_list:

    
    ingredients_string = ''
    for fruits_chosen in ingredients_list:
        ingredients_string+=fruits_chosen + ' '
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
        st.subheader(fruits_chosen+' Nutri Info')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruits_chosen)
        fv = st.dataframe(data=fruityvice_response.json(),use_container_width=True)
    
    st.write(ingredients_string)
     
    my_insert_stmt = """INSERT INTO smoothies.public.orders (ingredients, name_on_order)
                    VALUES ('""" + ingredients_string + """', '""" + name_on_order + """')"""

    
    #st.write(my_insert_stmt)
    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!'+name_on_order, icon="✅")

























