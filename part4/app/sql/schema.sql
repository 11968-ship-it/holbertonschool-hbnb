-- ====================
-- HBnB Schema (SQLite)
-- ====================
-- Drop existing tables if they exist (for clean setup)
DROP TABLE IF EXISTS PlaceImage;
DROP TABLE IF EXISTS Place_Amenity;
DROP TABLE IF EXISTS Review;
DROP TABLE IF EXISTS Place;
DROP TABLE IF EXISTS Amenity;
DROP TABLE IF EXISTS "User";

PRAGMA foreign_keys = ON;

-- ---------- User --------------
CREATE TABLE IF NOT EXISTS "User" (
    id         CHAR(36) PRIMARY KEY,
    first_name VARCHAR(255),
    last_name  VARCHAR(255),
    email      VARCHAR(255) UNIQUE NOT NULL,
    password   VARCHAR(255) NOT NULL,
    is_admin   BOOLEAN NOT NULL DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
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
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    -- Foreign key 
    FOREIGN KEY (owner_id) REFERENCES "User"(id) ON DELETE CASCADE
);
-- ---------- Place Image --------------
CREATE TABLE IF NOT EXISTS PlaceImage (
    id CHAR(36) PRIMARY KEY,
    place_id CHAR(36) NOT NULL,
    image_url VARCHAR(500) NOT NULL,
    display_order INTEGER DEFAULT 0,
    is_primary BOOLEAN DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign key: When place is deleted, delete all its images
    FOREIGN KEY (place_id) REFERENCES Place(id) ON DELETE CASCADE,
    
    -- Ensure display order is unique per place
    UNIQUE(place_id, display_order)
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_place_images_place_id ON PlaceImage(place_id);
CREATE INDEX IF NOT EXISTS idx_place_images_primary ON PlaceImage(is_primary) WHERE is_primary = 1;
-- ---------- Review --------------
CREATE TABLE IF NOT EXISTS Review (
    id CHAR(36) PRIMARY KEY,
    text TEXT NOT NULL,
    rating INT CHECK (rating >= 1 AND rating <= 5),
    user_id CHAR(36) NOT NULL,
    place_id CHAR(36) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES "User"(id) ON DELETE CASCADE,
    FOREIGN KEY (place_id) REFERENCES Place(id) ON DELETE CASCADE,
    UNIQUE (user_id, place_id) -- ensures one review per user per place
);

-- ---------- Amenity --------------
CREATE TABLE IF NOT EXISTS Amenity (
    id CHAR(36) PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);


-- ---- Place_Amenity (Many-to-Many) ----------
CREATE TABLE IF NOT EXISTS Place_Amenity (
    place_id   CHAR(36) NOT NULL,
    amenity_id CHAR(36) NOT NULL,

    PRIMARY KEY (place_id, amenity_id),

    FOREIGN KEY (place_id) REFERENCES Place(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (amenity_id) REFERENCES Amenity(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
    );
