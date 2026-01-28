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
    TRUE
);

-- ====================
-- Seed: Initial Amenities
-- ====================

INSERT INTO "Amenity" (id, name) VALUES
('f1b2c3d4-1111-4e2a-aaaa-1234567890ab', 'WiFi'),
('f1b2c3d4-2222-4e2a-bbbb-1234567890ac', 'Swimming Pool'),
('f1b2c3d4-3333-4e2a-cccc-1234567890ad', 'Air Conditioning');
