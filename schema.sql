CREATE TABLE Users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    admin BOOLEAN
);

CREATE TABLE Recipes (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES Users,
    name TEXT,
    description TEXT,
    time INT,
    privacy BOOLEAN
);

CREATE TABLE Ingredients (
    id SERIAL PRIMARY KEY,
    recipe_id INT REFERENCES Recipes,
    name TEXT,
    quantity TEXT,
    essential BOOLEAN
);

CREATE TABLE Instructions (
    id SERIAL PRIMARY KEY,
    recipe_id INT REFERENCES Recipes,
    instruction TEXT
);

CREATE TABLE Reviews (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES Users,
    recipe_id INT REFERENCES Recipes,
    review TEXT,
    grade INT
);