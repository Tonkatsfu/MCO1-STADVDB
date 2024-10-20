# MySQL connection setup
import mysql.connector
import pandas as pd
import plotly.express as px
from mysql.connector import Error

def create_connection():
    return mysql.connector.connect(
        host="localhost",   
        port=3306,                    
        user="root",             
        password="123456",     
        database="mco1"     
    )

def fetch_games_highest_peak_ccu_by_genre(included_genres, excluded_genres, top_n):
    include_query = " OR ".join([f"g.genres LIKE '%{genre}%'" for genre in included_genres])
    exclude_query = " AND ".join([f"g.genres NOT LIKE '%{genre}%'" for genre in excluded_genres])

    query = f"""
    SELECT 
        g.name, 
        MAX(f.`Peak CCU`) AS highest_peak_ccu
    FROM 
        dim_game g
    JOIN 
        fact_sales f ON g.`AppID` = f.`AppID`
    WHERE 
        ({include_query})
    """

    if exclude_query:
        query += f" AND ({exclude_query})"

    query += """
    GROUP BY 
        g.name
    ORDER BY 
        highest_peak_ccu DESC;
    """

    #Execute query
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()

    # Change to something else (maybe bar graph)
    # Convert the result to a DataFrame for display in Streamlit
    df = pd.DataFrame(result, columns=['Game Name', 'Highest Peak CCU'])

    # Return only top N records based on peak CCU
    top_games = df.nlargest(top_n, 'Highest Peak CCU')

    # Create a bar graph for the top N games
    fig = px.bar(top_games, x='Game Name', y='Highest Peak CCU', title=f'Top {top_n} Games by Highest Peak CCU')

    # Return the DataFrame and figure
    return top_games, fig