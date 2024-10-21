import streamlit as st
import functions  # Import functions from functions.py
import warnings
import plotly.express as px  # Import Plotly Express here
from mysql.connector import Error  # Import Error class

<<<<<<< Updated upstream
warnings.filterwarnings('ignore')
=======
import sys

sys.path.append('Functions')
sys.path.append('Views')

#Helper functions
import Functions.helperFunctions as hf

#Different views
import Views.ViewByGames as viewGames
import Views.ViewTwoGames as compareGames
import Views.ViewByGenres as viewGenres
>>>>>>> Stashed changes

# Title
st.title(":pencil: Steam Games Report")

# Age category filter
age_categories = st.sidebar.multiselect(
    "Select Age Categories",
    options=["0-7 (Children)", "8-15 (Teens)", "16-21 (Young Adults)"]
)

age_filter = functions.get_age_category_filter(age_categories)

# Fetch genres for dropdown
genres = functions.fetch_genres()  # Fetch unique genres from the database
selected_genre = st.sidebar.selectbox("Select Genre", options=sorted(genres))  # Sort the genres for better readability

# Fetch publishers for dropdown
publishers = functions.fetch_publishers()  # Fetch unique publishers from the database

connection = None

try:
    # Create a database connection
    connection = functions.create_connection()
    
    if connection.is_connected():
        # Radio button for selecting game mode
        categories = ["Single-player", "Multi-player"]
        selected_category = st.sidebar.radio("Gamemode", options=categories)

        if selected_category:
            # Fetch highest peak CCU data
            top_n_ccu = st.slider(
                "Number of games to display by Highest Peak CCU:",
                min_value=5,
                max_value=20,
                value=5,  
                step=1    
            )
            highest_ccu, fig_ccu = functions.fetch_games_highest_peak_ccu(
                selected_category,
                top_n_ccu,
                age_filter
            )
            st.plotly_chart(fig_ccu)  

<<<<<<< Updated upstream
            # Fetch highest average playtime data based on user input
            top_n_playtime = st.slider(
                "Number of games to display by Highest Playtime:",
                min_value=5,
                max_value=20,
                value=5,  
                step=1    
            )
            highest_ave_playtime, fig_playtime = functions.fetch_games_highest_playtime(
                selected_category, 
                top_n_playtime,
                age_filter
            )
            # Display Playtime chart
            st.plotly_chart(fig_playtime)
=======
        selected_view = st.sidebar.selectbox("Choose a view:", options=view_options)

        view_actions = {
            "View by Games": viewGames.display_game_reports,
            "Compare two games": compareGames.compare_two_games,
            "View by Publisher": viewGenres.display_genre_reports
        }

        if selected_view in view_actions:
            view_actions[selected_view]()
>>>>>>> Stashed changes

            # Fetch total games by publisher
            if selected_genre:
                unique_publishers = list(set(publishers))  # Remove duplicates
                top_n_publishers = st.slider(
                    "Number of Unique Publishers to display:",
                    min_value=1,
                    max_value=20,  # Total number of unique publishers
                    value=5,  # Default value
                    step=1
                )
                total_games_by_publisher = functions.fetch_total_games_by_publisher(selected_genre, top_n_publishers, age_filter)

                if not total_games_by_publisher.empty:
                    # Display total game counts in a bar chart by publisher
                    fig_publisher = px.bar(total_games_by_publisher, x='Publisher', y='Total Games', title='Total Games by Publisher')
                    st.plotly_chart(fig_publisher)
                else:
                    st.write("No games found for the selected genre.")
except Error as e:
    st.error(f"Error while connecting to MySQL: {e}")
finally:
    # Ensure the connection is closed
    if connection is not None and connection.is_connected():  
        connection.close()
