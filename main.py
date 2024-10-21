#Libraries used
import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px  
from mysql.connector import Error

import sys

sys.path.append('Functions')
sys.path.append('Views')

#Helper functions
import Functions.helperFunctions as hf

#Different views
import Views.ViewByGames as viewGames
import Views.ViewTwoGames as compareGames

# Title
st.title(":pencil: Steam Games Report")

try:
    # Create a database connection
    connection = hf.create_connection()
    if connection.is_connected():

        #Different view options
        st.sidebar.title("Select View")
        view_options = [
            "View by Games",
            "View by Publisher",
            "View by Developer",
            "View by Release Year",
            "View by Ratings",
            "Compare two games"
        ]

    selected_view = st.sidebar.selectbox("Choose a view:", options=view_options)
    
    if selected_view == "View by Games":
        viewGames.display_game_reports() #View by games
    elif selected_view == "Compare two games":
        compareGames.compare_two_games()

except Error as e:
    st.error(f"Error while connecting to MySQL: {e}")
finally:
    # Ensure the connection is closed
    if connection is not None and connection.is_connected():  
        connection.close()

