# # HBnB Project - Part 4: Simple Web Client
<img width="2454" height="1036" alt="logo" src="https://github.com/user-attachments/assets/d6175ea6-3b88-4986-9123-10996ef5635f" />

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

## Technologies Used
- **Front-End**
      - HTML5
      - CSS3
      - JavaScript (ES6)
      - Fetch API

- **Back-End (from previous parts)**
      - Flask
      - REST API
      - JWT Authentication

## Project Structure

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

#### **Front-End**
- **base_files/**
Contains all client-side files including HTML pages, CSS styling, JavaScript logic, and static assets (images). This directory represents the web client interface.

#### **Back-end**
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

1. Implement login using the back-end API:
   ```POST /api/v1/auth/login```
3. Store the returned JWT token in a cookie for session management.

## Task 3: List of Places

1. Display all places on the main page.
2. Fetch data from the API:
   ```GET /api/v1/places/```
4. Implement client-side filtering by country.
5. Redirect unauthenticated users to the login page.

## Task 4: Place Details

1. Fetch and display detailed information for a selected place:
   ```GET /api/v1/places/<place_id>```
3. Allow authenticated users to access the add review form.

## Task 5: Add Review

1. Implement a review submission form.
2. Sent review data using:
   ```POST /api/v1/reviews/```
4. Restrict access to authenticated users only.

## Authentication Flow
1. User logs in.
2. API returns JWT token.
3. Token is stored in browser cookie.
4. Protected pages verify token existence.
5. Requests include Authorization header:
   ```Authorization: Bearer <token>```

## Handling CORS
During development, the client and API run on different ports, causing CORS errors.

To resolve this, CORS support was added to the Flask API:
```py
from flask_cors import CORS
CORS(app)
```

This allows the web client to communicate with the API securely.

# Conclusion

Part 4 completes the HBnB project by integrating a fully functional front-end web client with the existing back-end API. Using HTML5, CSS3, and JavaScript (ES6), the application now provides a dynamic and interactive user experience without page reloads.

Through this phase, we successfully:

- Implemented JWT-based authentication on the client side
- Managed user sessions using cookies
- Connected the interface to RESTful API endpoints using the Fetch API
- Applied client-side validation and filtering
- Resolved CORS issues for cross-origin communication

This phase demonstrates a full-stack integration where the frontend and backend work together securely and efficiently. The HBnB application is now a complete web platform that follows modern development practices and industry standards.

# Authors
- Lamyaa Mohammed Alghaihab 11955@holbertonstudents.com 💻✍️
- Thekira A. Ahmed 11968@holbertonstudents.com 💻✍️
- Yara K. Alrasheed 11982@holbertonstudents.com 💻✍️
