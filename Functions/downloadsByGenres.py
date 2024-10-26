import mysql.connector
import pandas as pd
import helperFunctions as hf

import time

def fetch_publishers():
    query = "SELECT `Publishers` FROM `dim_publisher`"
    conn = hf.create_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    return [row[0] for row in result]

def fetch_genres():
    query = "SELECT DISTINCT `Genres` FROM `dim_game`"
    conn = hf.create_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    
    unique_genres = set()
    for row in result:
        for genre in row[0].split(','):
            unique_genres.add(genre.strip())
    
    return list(unique_genres)

def fetch_total_games_by_publisher(selected_genre, top_n_publishers, roll_up=False):
    start_time = time.time()  # Start the timer
    # Create index if it doesn't exist
    create_index_query = """
    CREATE INDEX IF NOT EXISTS idx_appid ON dim_game (AppID);
    """
    hf.execute_query(create_index_query)  # Ensure index is created

    query = f"""
    SELECT 
        p.Publishers AS Publisher, 
        COUNT(g.AppID) AS `Total Games`
    FROM 
        dim_game g
    JOIN 
        fact_sales f ON g.AppID = f.AppID
    JOIN 
        dim_publisher p ON f.AppID = p.AppID
    """

    if selected_genre:
        query += f" WHERE g.Genres = '{selected_genre}'"

    if roll_up:
        query += f"""
        GROUP BY 
            p.Publishers
        ORDER BY 
            `Total Games` DESC
        """
    else:
        query += f"""
        GROUP BY 
            p.Publishers, g.Genres
        ORDER BY 
            `Total Games` DESC
        """

    query += f" LIMIT {top_n_publishers};"

    conn = hf.create_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()

    df = pd.DataFrame(result, columns=['Publisher', 'Total Games'])

    end_time = time.time()  # End the timer
    runtime = end_time - start_time  # Calculate the runtime
    print(f"Runtime: {runtime:.4f} seconds")  # Print the runtime
    return df

def fetch_total_recommendations_by_publisher(selected_genre, top_n_publishers):
    query = f"""
    SELECT 
        p.`Publishers` AS `Publisher`, 
        SUM(g.`Recommendations`) AS `Total Recommendations`
    FROM 
        dim_game g
    JOIN 
        dim_publisher p ON g.`AppID` = p.`AppID`
    WHERE 
        g.`Genres` = '{selected_genre}'
    GROUP BY 
        p.`Publishers`
    ORDER BY 
        `Total Recommendations` DESC
    LIMIT {top_n_publishers};
    """

    conn = hf.create_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()

    df = pd.DataFrame(result, columns=['Publisher', 'Total Recommendations'])
    return df
