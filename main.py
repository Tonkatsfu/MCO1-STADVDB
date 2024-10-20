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

connection = None

try:
    connection = functions.create_connection()
    if connection.is_connected():
        if included_genres:
            game_data, fig = functions.fetch_games_highest_peak_ccu_by_genre(
                included_genres, 
                excluded_genres, 
                5
            )

            if not game_data.empty:  # Check if the DataFrame is empty
                col1, col2 = st.columns([1, 3])  # Adjust the width ratios as needed

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
                    top_n
                )

                # Display the bar graph
                st.plotly_chart(fig)  # Display the figure
            else:
                st.write("No games found for the selected genres.")

except Error as e:
    st.error(f"Error while connecting to MySQL: {e}")

finally:
    if connection is not None and connection.is_connected():  
        connection.close()

