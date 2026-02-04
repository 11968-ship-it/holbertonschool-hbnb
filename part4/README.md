# HBnB Project – Part 3: Enhanced Backend with Authentication & Database Integration

## Project Overview
Part 3 of the HBnB Project focuses on transforming the backend from a prototype into a secure, persistent, and production-ready system. This phase introduces JWT-based authentication, role-based authorization, and database integration using SQLAlchemy with SQLite for development and MySQL for production.

By the end of this part, the backend supports authenticated users, enforces permissions, persists data reliably, and is structured to scale in real-world environments.


## Objectives

### Authentication & Authorization
- Implement JWT authentication using Flask-JWT-Extended
- Secure protected endpoints
- Enforce role-based access control (RBAC) using the is_admin attribute

### Database Integration
- Replace in-memory storage with SQLite for development
- Prepare the application for MySQL in production
- Use SQLAlchemy ORM for database interactions

### CRUD Operations
- Refactor all CRUD operations to use persistent database storage
- Ensure consistent and reliable data handling

### Database Design & Visualization
- Design relational schemas for all entities
- Visualize entity relationships using Mermaid.js ER diagrams

### Data Validation & Consistency
- Enforce constraints and validation rules at the model level
- Maintain data integrity across relationships

---

## Project Structure

```
part3/
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── v1/
│   │       ├── __init__.py
│   │       ├── users.py
│   │       ├── places.py
│   │       ├── auth.py
│   │       ├── reviews.py
│   │       ├── amenities.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── place.py
│   │   ├── review.py
│   │   ├── place_amenity.py
│   │   ├── amenity.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── facade.py
│   ├── persistence/
│   |   ├── __init__.py
│   |   ├── repositories/
│   │       ├── amenity_repository.py
│   │       ├── place_repository.py
│   │       ├── review_repository.py
│   │       ├── user_repository.py
│   |   ├── repository.py
│   ├── sql/
│   |   ├──schema.sql
│   |   ├── seed.sql
│   |   ├── generate_admin_hash.py
|   ├── tests/
|   |   ├── test_models.py
├── run.py
├── config.py
├── requirements.txt
└── README.md
```

### Directory Purpose

- **api/**: Defines REST API endpoints (users, places, reviews, amenities).
- **models/**: Contains core entity classes.
- **services/**: Implements the Facade pattern to coordinate interactions between layers.
- **persistence/**: Provides an in-memory repository implementing a common storage interface.
- **persistence/repositories/**: Entity-specific repository implementations.
- **app/sql/**: Raw SQL utilities including schema, seed data, and admin password hash generator.
- **app/tests/**: Unit tests for models and core logic.
- **run.py**: Starts the Flask application.
- **config.py**: Holds environment-specific configuration.
- **requirements.txt**: Lists required Python packages.
---

## Authentication & Authorization
### Password Management
- User passwords are securely hashed using bcrypt
- Plain-text passwords are never stored

### JWT Authentication
- Token-based authentication using Flask-JWT-Extended
- Access tokens required for protected routes

### Role-Based Access Control
- is_admin flag determines administrative privileges
- Admin-only endpoints are strictly enforced

## Database Integration
### Development
- SQLite is used for lightweight, local development
- Database managed through SQLAlchemy

### Production
- Configured to switch seamlessly to MySQL
- Environment-based configuration ensures flexibility

### ORM Mapping
- Entities mapped using SQLAlchemy:
      - User
      - Place
      - Review
      - Amenity
- Relationships are properly defined with foreign keys and constraints.

## Installation

### Clone the repository:
   
   ```bash
   git clone <repository-url>
   cd holbertonschool-hbnb
   ```

### Install dependencies:

   ```
   pip install -r requirements.txt
   ```

### To initialize the database and create the table, run:

   ```
   flask shell
   >>> from app import db
   >>> db.create_all()
   ```

### Loading Schema and Seed Data

1. Open the SQLite database:
   ```
   sqlite3 hbnb.db
   ```

2. Load the schema
   ```
   .read schema.sql
   ```

3. Load the seed (initial) data:
   ```
   .read seed.sql
   ```

**These steps will:**

- Create all required tables and relationships
- Insert initial test or development data
- Allow immediate interaction with the database without running migrations

4. Exit the SQLite prompt when finished:
   ```
   .exit
   ```

## Running the Application

Start the Flask development server:

   ```
   python3 run.py
   ```

## API Tests (cURL)
- Environment variables used
      - ```ADMIN_TOKEN```: JWT for admin user
      - ```USER_TOKEN```: JWT for normal user (place owner)
      - ```USER2_TOKEN```: JWT for another normal user
      - ```PLACE_ID```: Place created by USER_TOKEN
      - ```AMENITY_ID```: Amenity created by admin
      - ```REVIEW_ID```: Review created by USER2_TOKEN

| Resource  | Endpoint | Method | Who | Expected | Actual | Result | Notes / Error |
|---|---|---:|---|---|---|---|---|
| Users | `/api/v1/users/` | POST | Admin | 201 | 201 | ✅ | Admin can create users |
| Users | `/api/v1/users/` | POST | User | 403 | 403 | ✅ | `Admin privileges required` |
| Places | `/api/v1/places/` | POST | User | 201 | 201 | ✅ | User can create place (owner_id = user) |
| Places | `/api/v1/places/<place_id>` | PUT | Owner | 200 | 200 | ✅ | Must send required fields if validation requires them |
| Places | `/api/v1/places/<place_id>` | PUT | Admin | 200 | 200 | ✅ | Admin bypass ownership |
| Places | `/api/v1/places/<place_id>` | DELETE | Admin | 200 | 200 | ✅ | Admin bypass ownership works |
| Amenities | `/api/v1/amenities/` | POST | User | 403 | 403 | ✅ | `Admin privileges required` |
| Amenities | `/api/v1/amenities/` | POST | Admin | 201 | 201 | ✅ | Amenity created |
| Amenities | `/api/v1/amenities/<amenity_id>` | PUT | Admin | 200 | 200 | ✅ | Amenity updated |
| Amenities | `/api/v1/amenities/<amenity_id>` | DELETE | Admin | 200 | 200 | ✅ | Amenity deleted |
| Reviews | `/api/v1/reviews/` | POST | Owner | 400 | 400 | ✅ | `You cannot review your own place.` |
| Reviews | `/api/v1/reviews/` | POST | User2 | 201 | 201 | ✅ | Review created successfully |
| Reviews | `/api/v1/reviews/` | POST | Same user2 again | 400 | 400 | ✅ | `You already reviewed this place.` (enforce unique user+place) |
| Reviews | `/api/v1/reviews/<review_id>` | PUT | Other user | 403 | 403 | ✅ | `Unauthorized action` |
| Reviews | `/api/v1/reviews/<review_id>` | PUT | Admin | 200 | 200 | ✅ | Admin bypass ownership |
| Reviews | `/api/v1/reviews/<review_id>` | DELETE | Admin | 200 | 200 | ✅ | Admin bypass ownership |

### Creating admin test on thr 29/1/2025

<img width="1044" height="478" alt="image" src="https://github.com/user-attachments/assets/a643b493-7ae7-4a29-b7ba-cd55ffb5c135" />

2. <img width="1060" height="879" alt="image" src="https://github.com/user-attachments/assets/7954e6f2-de45-4761-9871-42ae4eddc12c" />

Login as Admin to Get JWT Token

```bash
curl -X POST "http://127.0.0.1:5000/api/v1/auth/login" \
     -H "Content-Type: application/json" \
     -d '{
       "email": "admin@example.com",
       "password": "admin123"
     }'
```
Test Creating an Amenity (Admin Only)
Replace <admin_token> with the actual token you received:

```bash
curl -X POST "http://127.0.0.1:5000/api/v1/amenities/" \
     -H "Authorization: Bearer <admin_token>" \
     -H "Content-Type: application/json" \
     -d '{"name": "Swimming Pool"}'
```
 Get All Amenities (Verify Creation)

 ```bash
curl -X GET "http://127.0.0.1:5000/api/v1/amenities/"
```
Update an Amenity (Admin Only)
```bash
curl -X PUT "http://127.0.0.1:5000/api/v1/amenities/<amenity_id>" \
     -H "Authorization: Bearer <admin_token>" \
     -H "Content-Type: application/json" \
     -d '{"name": "Updated Swimming Pool"}'
```
Test Non-Admin User (Optional - to verify access control)
```bash
# Register regular user
curl -X POST "http://127.0.0.1:5000/api/v1/users/" \
     -H "Content-Type: application/json" \
     -d '{
       "email": "user@example.com",
       "password": "user123",
       "first_name": "Regular",
       "last_name": "User"
     }'

# Login as regular user
curl -X POST "http://127.0.0.1:5000/api/v1/auth/login" \
     -H "Content-Type: application/json" \
     -d '{
       "email": "user@example.com",
       "password": "user123"
     }'

# Try to create amenity with regular user token (should fail)
curl -X POST "http://127.0.0.1:5000/api/v1/amenities/" \
     -H "Authorization: Bearer <regular_user_token>" \
     -H "Content-Type: application/json" \
     -d '{"name": "Gym"}'

```

## Database Schema

### ER Diagram

> The following ER diagram was generated using Mermaid.js and reflects the SQLAlchemy models used in the application.
<img width="1167" height="875" alt="Screenshot (587)" src="https://github.com/user-attachments/assets/96e55801-558f-48d3-822e-8b4a7b159f7c" />

This ER diagram represents the relational structure of the HBnB backend.  
It defines users, places, reviews, amenities, and their relationships while enforcing data integrity through foreign keys and constraints.

- A **User** can own multiple **Places** and write multiple **Reviews**.
- A **Place** belongs to one **User** (owner) and can receive multiple **Reviews**.
- A **Review** links a **User** to a **Place**, with a uniqueness constraint ensuring one review per user per place.
- **Amenities** are linked to **Places** through a many-to-many relationship using the `Place_Amenity` join table.
- Administrative privileges are handled via the `is_admin` flag on the `User` entity.

This schema ensures normalized data storage, clear ownership rules, and consistent relationships across all core entities.

erDiagram

    USER {
        char(36) id PK
        varchar first_name
        varchar last_name
        varchar email "UNIQUE, NOT NULL"
        varchar password "NOT NULL"
        boolean is_admin "DEFAULT false"
    }

    PLACE {
        char(36) id PK
        varchar title "NOT NULL"
        text description
        decimal price "NOT NULL"
        float latitude "NOT NULL"
        float longitude "NOT NULL"
        char(36) owner_id FK
    }

    REVIEW {
        char(36) id PK
        text text "NOT NULL"
        int rating "CHECK 1..5"
        char(36) user_id FK
        char(36) place_id FK
        %% also: UNIQUE(user_id, place_id)
    }

    AMENITY {
        char(36) id PK
        varchar name "UNIQUE, NOT NULL"
    }

    PLACE_AMENITY {
        char(36) place_id PK, FK
        char(36) amenity_id PK, FK
    }

    %% Relationships
    USER  ||--o{ PLACE  : owns
    USER  ||--o{ REVIEW : writes
    PLACE ||--o{ REVIEW : receives

    PLACE   ||--o{ PLACE_AMENITY : has
    AMENITY ||--o{ PLACE_AMENITY : included_in

# Conclusion

Part 3 elevates the HBnB backend into a secure, scalable, and production-ready system. With authentication, authorization, and database persistence in place, the application is now aligned with industry-standard backend practices and ready for further expansion.

# Authors
- Lamyaa Mohammed Alghaihab 11955@holbertonstudents.com 💻✍️
- Thekira A. Ahmed 11968@holbertonstudents.com 💻✍️
- Yara K. Alrasheed 11982@holbertonstudents.com 💻✍️
