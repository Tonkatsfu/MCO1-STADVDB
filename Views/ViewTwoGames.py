import streamlit as st
import Functions.gameFunctions as gameFunctions
import Functions.helperFunctions as hf

def fetch_unique_game_names():
    query = "SELECT DISTINCT name FROM dim_game ORDER BY name ASC"
    return [row[0] for row in hf.execute_query(query)]

def compare_two_games():
    st.sidebar.title("Choose Two Games")

    default = ['Select a game']
    game_names = default + fetch_unique_game_names()

    selected_game_one = st.sidebar.selectbox("Choose Game 1:", options=game_names, index=0)
    game_names_two = default + [game for game in game_names if game != selected_game_one]
    selected_game_two = st.sidebar.selectbox("Choose Game 2:", options=game_names_two, index=0)