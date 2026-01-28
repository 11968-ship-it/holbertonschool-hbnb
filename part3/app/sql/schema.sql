-- ====================
-- HBnB Schema (SQLite)
-- ====================
PRAGMA foreign_keys = ON;

-- ---------- User --------------
CREATE TABLE IF NOT EXISTS users (
    id         CHAR(36) PRIMARY KEY,
    first_name VARCHAR(255),
    last_name  VARCHAR(255),
    email      VARCHAR(255) UNIQUE NOT NULL,
    password   VARCHAR(255) NOT NULL,
    is_admin   BOOLEAN NOT NULL DEFAULT 0
);


-- ---------- Place --------------


-- ---------- Review --------------


-- ---------- Amenity --------------
