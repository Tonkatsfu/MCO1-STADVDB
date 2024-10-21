import streamlit as st
import Functions.CompareTwoGames as tg

def compare_two_games():
    st.sidebar.title("Choose Two Games")

    default = ['Select a game']
    game_names = default + tg.fetch_unique_game_names()

    game_one = st.sidebar.selectbox("Choose Game 1:", options=game_names, index=0)
    game_names_two = default + [game for game in game_names if game != game_one]
    game_two = st.sidebar.selectbox("Choose Game 2:", options=game_names_two, index=0)

    if game_one != 'Select a game' and game_two != 'Select a game':
        

        #bar graph that compares two games positive and negative reviews
        fig = tg.compare_reviews(game_one, game_two)
        st.plotly_chart(fig) 

        fig = tg.compare_ccu(game_one, game_two)
        st.plotly_chart(fig) 
