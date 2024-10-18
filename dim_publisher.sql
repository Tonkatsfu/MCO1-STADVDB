CREATE TABLE dim_publisher (
    publisher_id INT PRIMARY KEY AUTO_INCREMENT,
    publisher_name VARCHAR(255),
    app_id INT,
    FOREIGN KEY (app_id) REFERENCES dim_game(app_id) ON DELETE CASCADE
);