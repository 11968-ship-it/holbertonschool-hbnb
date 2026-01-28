-- ====================
-- HBnB Schema (SQLite)
-- ====================
-- Drop existing tables if they exist (for clean setup)
DROP TABLE IF EXISTS Place_Amenity;
DROP TABLE IF EXISTS Review;
DROP TABLE IF EXISTS Place;
DROP TABLE IF EXISTS Amenity;
DROP TABLE IF EXISTS User;

PRAGMA foreign_keys = ON;

-- ---------- User --------------
CREATE TABLE IF NOT EXISTS "User" (
    id         CHAR(36) PRIMARY KEY,
    first_name VARCHAR(255),
    last_name  VARCHAR(255),
    email      VARCHAR(255) UNIQUE NOT NULL,
    password   VARCHAR(255) NOT NULL,
    is_admin   BOOLEAN NOT NULL DEFAULT 0
);

INSERT INTO "User" (id, first_name, last_name, email, password, is_admin)
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2b$12$KIXw7eKuoD1lVggh7X1sPOn2rOqNQtvFzOn8ZsT6r8gMf2eZcx42C', -- bcrypt hash
    TRUE
);


-- ---------- Place --------------
CREATE TABLE IF NOT EXISTS Place (
    id CHAR(36) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    owner_id CHAR(36) NOT NULL,

    -- Foreign key 
    FOREIGN KEY (owner_id) REFERENCES User(id) ON DELETE CASCADE
);
-- ---------- Review --------------
CREATE TABLE IF NOT EXISTS Review (
    id CHAR(36) PRIMARY KEY,
    text TEXT NOT NULL,
    rating INT CHECK (rating >= 1 AND rating <= 5),
    user_id CHAR(36) NOT NULL,
    place_id CHAR(36) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES "User"(id) ON DELETE CASCADE,
    FOREIGN KEY (place_id) REFERENCES "Place"(id) ON DELETE CASCADE,
    UNIQUE (user_id, place_id) -- ensures one review per user per place
);

-- ---------- Amenity --------------
CREATE TABLE IF NOT EXISTS Amenity (
    id CHAR(36) PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL
);

INSERT INTO "Amenity" (id, name) VALUES
('f1b2c3d4-1111-4e2a-aaaa-1234567890ab', 'WiFi'),
('f1b2c3d4-2222-4e2a-bbbb-1234567890ac', 'Swimming Pool'),
('f1b2c3d4-3333-4e2a-cccc-1234567890ad', 'Air Conditioning');

-- ---- Place_Amenity (Many-to-Many) ----------
CREATE TABLE IF NOT EXISTS Place_Amenity (
    place_id   CHAR(36) NOT NULL,
    amenity_id CHAR(36) NOT NULL,

    PRIMARY KEY (place_id, amenity_id),

    FOREIGN KEY (place_id) REFERENCES "Place"(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (amenity_id) REFERENCES "Amenity"(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
    );
