# # Update from given tags
# tags = ["Action", "Adventure", "Strategy", "RPG", "Sports", "Simulation", "Indie"]


# included_tags = st.sidebar.multiselect("Select Tags to Include", tags)
# temp_tags = [tag for tag in tags if tag not in included_tags]
# excluded_tags = st.sidebar.multiselect("Select Tags to Exclude", temp_tags)

import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px  
from mysql.connector import Error
import warnings
import os
import functions #functions


warnings.filterwarnings('ignore')

# Title
st.title(":pencil: Steam Games Report")
genres = ["Single-player", "Multi-player", "Full controller support"]

# Sidebar input for included genres
included_genres = st.sidebar.multiselect("Select Genres to Include", genres)
temp_genres = [genre for genre in genres if genre not in included_genres]
excluded_genres = st.sidebar.multiselect("Select Genres to Exclude", temp_genres)

age_categories = st.sidebar.multiselect(
    "Select Age Categories",
    options=["0-7 (Children)", "8-15 (Teens)", "16-21 (Young Adults)"]
)

age_filter = functions.get_age_category_filter(age_categories)

connection = None

try:
    connection = functions.create_connection()
    if connection.is_connected():
        if included_genres:

            #Data checks
            game_data, fig = functions.fetch_games_highest_peak_ccu_by_genre(
                included_genres, 
                excluded_genres, 
                5,
                age_filter
            )

            if not game_data.empty: 
                col1, col2 = st.columns([1, 3])  

                with col1:
                    top_n = st.slider(
                        "Select number of top games to display:",
                        min_value=5,
                        max_value=50,
                        value=5,  
                        step=1    
                    )

                # Fetch the data for the selected number of top games
                game_data, fig = functions.fetch_games_highest_peak_ccu_by_genre(
                    included_genres, 
                    excluded_genres, 
                    top_n,
                    age_filter
                )

                st.plotly_chart(fig)  
            else:
                st.write("No games found.")

except Error as e:
    st.error(f"Error while connecting to MySQL: {e}")

finally:
    if connection is not None and connection.is_connected():  
        connection.close()

