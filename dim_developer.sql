CREATE TABLE dim_developer (
    developer_id INT PRIMARY KEY AUTO_INCREMENT,
    developer_name VARCHAR(255),
    app_id INT,
    FOREIGN KEY (app_id) REFERENCES dim_game(app_id) ON DELETE CASCADE
);