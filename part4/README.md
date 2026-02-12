# # HBnB Project - Part 4: Simple Web Client

In this phase of the project, the focus is on building the front-end of the application using HTML5, CSS3, and JavaScript (ES6). The goal is to design and implement an interactive user interface that communicates with the back-end API developed in previous parts.

This web client allows users to:
* Log in
* Browse places
* View detailed place information
* Add reviews

All through a dynamic and responsive interface.

## Project Overview
The web client connects to the back-end API created in previous phases. It uses modern JavaScript (ES6) and the Fetch API to interact with REST endpoints and manage authentication using JWT tokens stored in cookies.


## Objectives

- Develop a user-friendly interface based on provided design specifications.
- Implement client-side functionality to communicate with the back-end API.
- Handle authentication and session management using JWT.
- Apply modern web development practices to build a dynamic web application.


## Project Structure?

```
part4/
├── base_files/
│   ├── add-place.html
│   ├── add_review.html
│   ├── index.html
│   ├── login.html
│   ├── place.html
│   ├── scripts.js
│   ├── signup.html
│   ├── styles.css
│   ├── images
├── instance
│   ├── app.db
│   ├── development.db
│   ├── hbnb.db
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

# Tasks Breakdown

General Tasks are:

1. Design
2. Login
3. List of Places
4. Place Details
5. Add Review


## Running the Application

1. Starting the Back-End (API) using:
Depending on the Python installation, we used one of the following:

   ```
   python run.py
   ```
or
   ```
   python3 run.py
   ```
It will start the Flask API server.

2. Starting the Front-End (Web Client):

  ```
  python3 -m http.server (Port-number)
  ```
or
  ```
  python -m http.server (port-number)

  ```
Placing available port number, and in our case we used ``` 5000 ``` and ``` 5500 ```.

3. Open the Application:

In the browser:
   ```
   http://localhost:(port-number)
   ```

## Task 1: Design

1. Complete the provided HTML and CSS files.
2. Create pages for:
   - Login
   - List of Places
   - Place Details
   - Add Review

## Task 2: Login

1. Implement login using the back-end API.
2. Store the returned JWT token in a cookie for session management.

## Task 3: List of Places

1. Display all places on the main page.
2. Fetch data from the API.
3. Implement client-side filtering by country.
4. Redirect unauthenticated users to the login page.

## Task 4: Place Details

1. Fetch and display detailed information for a selected place.
2. Allow authenticated users to access the add review form.

## Task 5: Add Review

1. Implement a review submission form.
2. Restrict access to authenticated users only.



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
