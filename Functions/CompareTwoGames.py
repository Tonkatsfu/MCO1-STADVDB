import mysql.connector
import pandas as pd
import streamlit as st
import plotly.graph_objects as go

import helperFunctions as hf

def fetch_unique_game_names():
    query = "SELECT DISTINCT name FROM dim_game ORDER BY name ASC"
    return [row[0] for row in hf.execute_query(query)]

def fetch_game_reviews(game_name):
    query = f"""
    SELECT 
        `Positive`, `Negative`
    FROM 
        fact_sales
    WHERE 
        `AppID` = (
            SELECT 
                `AppID`
            FROM 
                dim_game 
            WHERE 
                `Name` = '{game_name}'
        )
    """
    result = hf.execute_query(query)

    if result and len(result) > 0:
        positive_reviews, negative_reviews = result[0]  
        return positive_reviews, negative_reviews
    else:
        return 0, 0

def fetch_game_ccu(game_name):
    query = f"""
    SELECT 
        `Peak CCU`
    FROM 
        fact_sales
    WHERE 
        `AppID` = (
            SELECT 
                `AppID` 
            FROM 
                dim_game 
            WHERE 
                `Name` = '{game_name}'
        )
    """
    result = hf.execute_query(query)

    if result and len(result) > 0:
        return result[0][0]  
    else:
        return 0
    
def fetch_game_price(game_name):
    query = f"""
    SELECT 
        `Price`
    FROM
        fact_sales
    WHERE
        `AppID` = (
        SELECT
            `AppID`
        FROM
            dim_game
        WHERE
            `Name` = '{game_name}'
        )
    """
    result = hf.execute_query(query)

    if result and len(result) > 0:
        return result[0][0] 
    else:
        return 0

def compare_reviews(game_one, game_two):

    pos_reviews_one, neg_reviews_one = fetch_game_reviews(game_one)
    pos_reviews_two, neg_reviews_two = fetch_game_reviews(game_two)

    data = {
        'Reviews': ['Positive', 'Negative'],
        game_one: [pos_reviews_one, neg_reviews_one],
        game_two: [pos_reviews_two, neg_reviews_two]
    }

    df = pd.DataFrame(data)
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=df['Reviews'],
        y=df[game_one],
        name=game_one,
        marker_color='#1f77b4' 
    ))

    fig.add_trace(go.Bar(
        x=df['Reviews'],
        y=df[game_two],
        name=game_two,
        marker_color='#ff7f0e'  
    ))

    fig.update_layout(
        title='Comparison of Positive vs Negative Reviews',
        xaxis_title='Review Type',
        yaxis_title='Number of Reviews',
        barmode='group',  
        legend_title='Games'
    )

    return fig

def compare_ccu(game_one, game_two):
    ccu_one = fetch_game_ccu(game_one)
    ccu_two = fetch_game_ccu(game_two)

    data = {
        'Games': [game_one, game_two],
        'Peak CCU': [ccu_one, ccu_two]
    }

    df = pd.DataFrame(data)
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=df['Games'],
        y=df['Peak CCU'],
        marker_color=['#1f77b4', '#ff7f0e'], 
    ))

    fig.update_layout(
        title='Comparison of Peak Concurrent Users (CCU)',
        xaxis_title='Games',
        yaxis_title='Peak CCU',
        barmode='group', 
    )

    return fig

def compare_price(game_one, game_two):
    price_one = fetch_game_price(game_one)
    price_two = fetch_game_price(game_two)

    data = {
        'Games': [game_one, game_two],
        'Game Price': [price_one, price_two]
    }

    df = pd.DataFrame(data)
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=df['Games'],
        y=df['Game Price'],
        marker_color=['#1f77b4', '#ff7f0e'], 
    ))

    fig.update_layout(
        title='Comparison of Game Prices',
        xaxis_title='Games',
        yaxis_title='Game Price',
        barmode='group', 
    )

    return fig
