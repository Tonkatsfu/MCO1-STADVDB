import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px  
from mysql.connector import Error
import warnings
import os
import functions 

warnings.filterwarnings('ignore')

# Title
st.title(":pencil: Steam Games Report")

age_categories = st.sidebar.multiselect(
    "Select Age Categories",
    options=["0-7 (Children)", "8-15 (Teens)", "16-21 (Young Adults)"]
)

age_filter = functions.get_age_category_filter(age_categories)

connection = None

try:
    # Create a database connection
    connection = functions.create_connection()
    
    if connection.is_connected():
        # Radio button for selecting game mode
        categories = ["Single-player", "Multi-player"]
        selected_category = st.sidebar.radio("Gamemode", options=categories)

        if selected_category:
            functions.display_game_data(
                functions.fetch_games_highest_peak_ccu,
                selected_category,
                "Highest Peak CCU",
                5,
                age_filter
            )

            # Fetch and display Highest Average Playtime
            functions.display_game_data(
                functions.fetch_games_highest_playtime,
                selected_category,
                "Highest Average and Median Playtime of All Time",
                5,
                age_filter
            )

except Error as e:
    st.error(f"Error while connecting to MySQL: {e}")
finally:
    # Ensure the connection is closed
    if connection is not None and connection.is_connected():  
        connection.close()

