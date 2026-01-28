-- ====================
-- HBnB Schema (SQLite)
-- ====================
PRAGMA foreign_keys = ON;

-- ---------- User --------------
CREATE TABLE IF NOT EXISTS Users (
    id         CHAR(36) PRIMARY KEY,
    first_name VARCHAR(255),
    last_name  VARCHAR(255),
    email      VARCHAR(255) UNIQUE NOT NULL,
    password   VARCHAR(255) NOT NULL,
    is_admin   BOOLEAN NOT NULL DEFAULT 0
);


-- ---------- Place --------------
CREATE TABLE Place (
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


-- ---------- Amenity --------------
