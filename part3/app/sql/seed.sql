-- ====================
-- HBnB Seed Data
-- ====================

PRAGMA foreign_keys = ON;

-- ====================
-- Seed: Admin User
-- ====================
INSERT INTO User (
    id,
    email,
    first_name,
    last_name,
    password,
    is_admin
) VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'admin@hbnb.io',
    'Admin',
    'HBnB',
    '$2b$12$OBOKagu1u1QSSGzvvBeeoeRaAW4H/nLIIyrZehUnZauE1Dgx/Mnte',
    1
);

-- ====================
-- Seed: Initial Amenities
-- ====================
