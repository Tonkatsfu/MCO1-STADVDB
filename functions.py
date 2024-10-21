import mysql.connector
import pandas as pd
import plotly.express as px
from mysql.connector import Error

# MySQL connection setup
def create_connection():
    return mysql.connector.connect(
        host="localhost",   
        port=3306,                    
        user="root",             
        password="kian0204",     
        database="databasewarehouse"     
    )

def get_age_category_filter(age_filter):
    age_conditions = []
    
    if "0-7 (Children)" in age_filter:
        age_conditions.append("`Required Age` BETWEEN 0 AND 7")
    if "8-15 (Teens)" in age_filter:
        age_conditions.append("`Required Age` BETWEEN 8 AND 15")
    if "16-21 (Young Adults)" in age_filter:
        age_conditions.append("`Required Age` BETWEEN 16 AND 21")

    return " OR ".join(age_conditions)

def fetch_publishers():
    query = "SELECT `Publishers` FROM `dim_publisher`"
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    return [row[0] for row in result]

def fetch_genres():
    query = "SELECT DISTINCT `Genres` FROM `dim_game`"
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    
    # Split genres and create a set for unique genres
    unique_genres = set()
    for row in result:
        # Split by comma and strip whitespace
        for genre in row[0].split(','):
            unique_genres.add(genre.strip())
    
    return list(unique_genres)

def fetch_games_highest_peak_ccu(selected_category, top_n, age_fil):
    query = f"""
    SELECT 
        g.name, 
        MAX(f.`Peak CCU`) AS highest_peak_ccu
    FROM 
        dim_game g
    JOIN 
        fact_sales f ON g.`AppID` = f.`AppID`
    WHERE 
        FIND_IN_SET('{selected_category}', g.`Categories`) > 0
    """

    if age_fil:
        query += f" AND ({age_fil})"

    query += """
    GROUP BY 
        g.name
    ORDER BY 
        highest_peak_ccu DESC;
    """

    # Execute query
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()

    df = pd.DataFrame(result, columns=['Game Name', 'Highest Peak CCU'])
    df['Highest Peak CCU'] = pd.to_numeric(df['Highest Peak CCU'], errors='coerce')
    highest_ccu = df.nlargest(top_n, 'Highest Peak CCU')
    fig = px.bar(highest_ccu, x='Game Name', y='Highest Peak CCU', title=f'Top {top_n} Games by Highest Peak CCU')
    return highest_ccu, fig

def fetch_games_highest_playtime(selected_category, top_n, age_fil):
    query = f"""
    SELECT 
        g.name, 
        AVG(f.`Average playtime forever`) AS average_playtime, 
        AVG(f.`Median playtime forever`) AS median_playtime
    FROM 
        dim_game g
    JOIN 
        fact_sales f ON g.`AppID` = f.`AppID`
    WHERE 
        FIND_IN_SET('{selected_category}', g.`Categories`) > 0
    """

    if age_fil:
        query += f" AND ({age_fil})"

    query += """
    GROUP BY 
        g.name
    ORDER BY 
        average_playtime DESC;
    """

    # Execute query
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()

    df = pd.DataFrame(result, columns=['Game Name', 'Average Playtime', 'Median Playtime'])
    df['Average Playtime'] = pd.to_numeric(df['Average Playtime'], errors='coerce')
    df['Median Playtime'] = pd.to_numeric(df['Median Playtime'], errors='coerce')
    df = df.dropna(subset=['Average Playtime', 'Median Playtime'])
    highest_ave_playtime = df.nlargest(top_n, 'Average Playtime')

    long_df = highest_ave_playtime.melt(id_vars='Game Name', 
                                         value_vars=['Average Playtime', 'Median Playtime'],
                                         var_name='Playtime Type', 
                                         value_name='Playtime')

    fig = px.bar(
        long_df, 
        x='Game Name', 
        y='Playtime', 
        color='Playtime Type',
        title=f'Top {top_n} Games by Average and Median Playtime',
        barmode='group'
    )

    return highest_ave_playtime, fig

def fetch_total_games_by_publisher(selected_genre, top_n_publishers, age_filter, roll_up=False):
    # Base query
    query = f"""
    SELECT 
        p.`Publishers` AS `Publisher`, 
        COUNT(g.`AppID`) AS `Total Games`
    FROM 
        dim_game g
    JOIN 
        fact_sales f ON g.`AppID` = f.`AppID`
    JOIN 
        dim_publisher p ON f.`AppID` = p.`AppID`
    """

    # Apply slicing based on genre
    if selected_genre:
        query += f" WHERE g.Genres = '{selected_genre}'"

    # Include age filter if provided
    if age_filter:
        query += f" AND ({age_filter})"

    # Optionally roll up if requested
    if roll_up:
        query += f"""
        GROUP BY 
            p.`Publishers`
        ORDER BY 
            `Total Games` DESC
        """
    else:
        query += f"""
        GROUP BY 
            p.`Publishers`, g.Genres
        ORDER BY 
            `Total Games` DESC
        """

    query += f" LIMIT {top_n_publishers};"

    # Execute the query
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()

    # Return as DataFrame
    df = pd.DataFrame(result, columns=['Publisher', 'Total Games'])
    return df

