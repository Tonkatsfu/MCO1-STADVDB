CREATE TABLE dim_game (
    app_id INT PRIMARY KEY,
    name TEXT,
    release_date DATE,
    required_age INT,
    genres TEXT,
    categories TEXT,
    tags TEXT,
    about_the_game LONGTEXT,
    header_image TEXT,
    website TEXT,
    support_url TEXT,
    support_email TEXT,
    achievements TEXT,
    recommendations TEXT,
    notes TEXT
);

SELECT * FROM dim_game;
