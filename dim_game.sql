CREATE TABLE dim_game (
    app_id INT PRIMARY KEY,
    name VARCHAR(255),
    release_date DATE,
    required_age INT,
    genres VARCHAR(255),
    categories VARCHAR(255),
    tags TEXT,
    about_the_game LONGTEXT,
    header_image TEXT,
    website TEXT,
    support_url TEXT,
    support_email VARCHAR(255),
    achievements TEXT,
    recommendations TEXT,
    notes TEXT
);


