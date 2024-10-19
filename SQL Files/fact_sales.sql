CREATE TABLE fact_sales (
    sales_id INT PRIMARY KEY AUTO_INCREMENT,
    app_id INT,
    estimated_owners VARCHAR(255),
    peak_ccu INT,
    price DECIMAL(10, 2),
    positive_reviews INT,
    negative_reviews INT,
    score_rank INT,
    average_playtime_forever INT,
    average_playtime_two_weeks INT,
    median_playtime_forever INT,
    median_playtime_two_weeks INT,
    time_id INT,
    FOREIGN KEY (app_id) REFERENCES dim_game(app_id) ON DELETE CASCADE,
    FOREIGN KEY (time_id) REFERENCES dim_time(time_id) ON DELETE CASCADE
);