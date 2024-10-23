import streamlit as st
import Functions.downloadsByGenres as gf
import plotly.express as px 
import pandas as pd

def display_genre_reports():
    st.sidebar.title("Select a Genre")

    genres = gf.fetch_genres()  
    default = ['Select a genre'] 
    genre_list = default + sorted(genres) 

    selected_genre = st.sidebar.selectbox("Choose Genre:", options=genre_list, index=0)

    if selected_genre != 'Select a genre': 
        st.write(f"Selected Genre: {selected_genre}")

        top_n_publishers = st.slider(
            "Number of Unique Publishers to display by Total Games:",
            min_value=1,
            max_value=20, 
            value=5,
            step=1
        )

        total_games_by_publisher = gf.fetch_total_games_by_publisher(selected_genre, top_n_publishers)

        if not total_games_by_publisher.empty:
            st.write(f"Total games for genre: {selected_genre}")
            fig_publisher = px.bar(total_games_by_publisher, x='Publisher', y='Total Games', title='Total Games by Publisher')
            st.plotly_chart(fig_publisher)
        else:
            st.write(f"No games found for the selected genre: {selected_genre}")

        top_n_publishers_recommendations = st.slider(
            "Number of Recommendations per Publishers:",
            min_value=1,
            max_value=20, 
            value=5,
            step=1
        )

        total_recommendations_by_publisher = gf.fetch_total_recommendations_by_publisher(selected_genre, top_n_publishers_recommendations)

        if not total_recommendations_by_publisher.empty:
            fig_recommendations = px.bar(total_recommendations_by_publisher, x='Publisher', y='Total Recommendations', title='Total Recommendations by Publisher')
            st.plotly_chart(fig_recommendations)
        else:
            st.write(f"No recommendations found for the selected genre: {selected_genre}")

