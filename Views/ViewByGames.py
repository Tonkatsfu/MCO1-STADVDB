import streamlit as st
import Functions.gameFunctions as gf

def display_game_reports():
    # Radio button for selecting game mode
    categories = ["Single-player", "Multi-player"]
    selected_category = st.sidebar.radio("Gamemode", options=categories)

    age_categories = st.sidebar.multiselect(
        "Select Age Categories",
        options=["0-7 (Children)", "8-15 (Teens)", "16-21 (Young Adults)"]
    )

    age_filter = gf.get_age_category_filter(age_categories)

    if selected_category:
        # Display Highest Peak CCU
        gf.display_game_data(
            gf.fetch_games_highest_peak_ccu,
            selected_category,
            "Highest Peak CCU",
            5,
            age_filter
        )

        # Display Highest Average Playtime
        gf.display_game_data(
            gf.fetch_games_highest_playtime,
            selected_category,
            "Highest Average and Median Playtime of All Time",
            5,
            age_filter
        )

        gf.display_game_datas(
            gf.fetch_games_required_age,
            selected_category,
            age_filter
        )