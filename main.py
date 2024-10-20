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
categories = ["Single-player", "Multi-player", "Full controller support"]

# Sidebar input for included categories
included_categories = st.sidebar.multiselect("Select Categories to Include", categories)
temp_categories = [category for category in categories if category not in included_categories]
excluded_categories = st.sidebar.multiselect("Select Categories to Exclude", temp_categories)

age_categories = st.sidebar.multiselect(
    "Select Age Categories",
    options=["0-7 (Children)", "8-15 (Teens)", "16-21 (Young Adults)"]
)

age_filter = functions.get_age_category_filter(age_categories)

connection = None

try:
    connection = functions.create_connection()
    if connection.is_connected():
        if included_categories:

            #Data checks
            game_data, fig = functions.fetch_games_highest_peak_ccu(
                included_categories, 
                excluded_categories, 
                5,
                age_filter
            )

            if not game_data.empty: 

                top_n_ccu = st.slider(
                    "Number of games to display by Highest Peak CCU:",
                    min_value=5,
                    max_value=20,
                    value=5,  
                    step=1    
                )

                highest_ccu, fig = functions.fetch_games_highest_peak_ccu(
                    included_categories, 
                    excluded_categories, 
                    top_n_ccu,
                    age_filter
                    )

                st.plotly_chart(fig)  

                top_n_playtime = st.slider(
                    "Number of games to display by Highest Playtime",
                    min_value=5,
                    max_value=20,
                    value=5,  
                    step=1    
                )

                highest_ave_playtime, fig = functions.fetch_games_highest_playtime(
                    included_categories,
                    excluded_categories,
                    top_n_playtime,
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

