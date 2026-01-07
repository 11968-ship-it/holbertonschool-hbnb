# holbertonschool-hbnb

## Project Overview
This project is part of the HBnB application and focuses on setting up the initial project structure and core architecture. The goal is to create a clean, modular Flask application with a clear separation of concerns, preparing the codebase for future development.


The application is organized into three main layers:

- **Presentation Layer**: RESTful API endpoints built with Flask and Flask-RESTx.
- **Business Logic Layer**: Core models and services that define application behavior.
- **Persistence Layer**: An in-memory repository used for object storage and validation (to be replaced by a database in later stages).

At this stage, the application runs successfully but does not yet expose functional API endpoints.

---

## Project Structure

```
hbnb/
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── v1/
│   │       ├── __init__.py
│   │       ├── users.py
│   │       ├── places.py
│   │       ├── reviews.py
│   │       ├── amenities.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── place.py
│   │   ├── review.py
│   │   ├── amenity.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── facade.py
│   ├── persistence/
│   |   ├── __init__.py
│   |   ├── repository.py
|   ├── tests/
|   |   ├── test_models.py
├── run.py
├── config.py
├── requirements.txt
├── README.md

```


### Directory Purpose

- **api/**: Defines REST API endpoints (users, places, reviews, amenities).
- **models/**: Contains core entity classes.
- **services/**: Implements the Facade pattern to coordinate interactions between layers.
- **persistence/**: Provides an in-memory repository implementing a common storage interface.
- **run.py**: Starts the Flask application.
- **config.py**: Holds environment-specific configuration.
- **requirements.txt**: Lists required Python packages.

---

## Installation

1. Clone the repository:
   
   ```bash
   git clone <repository-url>
   cd holbertonschool-hbnb
   
2. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

## Running the Application

Start the Flask development server:

```
python run.py
```
The application will run in debug mode.
No API routes are fully implemented yet, but the server should start without errors.


## Future Development

* Implement full business logic in models and services
* Add functional API endpoints
* Replace the in-memory repository with a database-backed persistence layer
* Add authentication and authorization
* Improve validation and error handling

## Subtasks
This project is developed incrementally and is divided into the following subtasks:

1. Core Business Logic Classes
Define and manage the core models (User, Place, Review, Amenity) and their behaviors.

2. User Endpoints
Implement API endpoints to manage users and integrate them with the business logic layer.

3. Amenity Endpoints
Create endpoints to handle amenities and associate them with places.

4. Place Endpoints
Implement endpoints for managing places, including relationships with owners, amenities, and reviews.

5. Review Endpoints
Implement full CRUD operations for reviews, ensuring proper integration with users and places via the Facade pattern.

6. Testing and Validation
Add unit tests and validate input data to ensure application correctness and stability.


# Core Business Logic Classes

# User Endpoints

# Amenity Endpoints

This project is developed incrementally and is divided into the following subtasks:

1. **Core Business Logic Classes**  
   Define and manage the core models (User, Place, Review, Amenity) and their behaviors.

2. **User Endpoints**  
   Implement API endpoints to manage users and integrate them with the business logic layer.

3. **Amenity Endpoints**  
   Implement RESTful API endpoints to manage amenities:
   - **POST**: Create a new amenity
   - **GET**: Retrieve a list of all amenities or a single amenity by ID
   - **PUT**: Update an existing amenity
   - **DELETE** is **not implemented** at this stage  
   Endpoints integrate with the Business Logic layer via the **Facade pattern**.


4. **Place Endpoints**  
   Implement endpoints for managing places, including relationships with owners, amenities, and reviews.

5. **Review Endpoints**  
   Implement full CRUD operations for reviews, ensuring proper integration with users and places via the Facade pattern.

6. **Testing and Validation**  
   Add unit tests and validate input data to ensure application correctness and stability.


# Place Endpoints

# Review Endpoints
The Review Endpoints task focuses on implementing RESTful API endpoints to manage reviews within the HBnB application.

## Key objectives:

* Implement POST, GET, PUT, and DELETE endpoints for reviews
  code exaplme to Register a New Review:
  
     ```
      POST /api/v1/reviews/
     Content-Type: application/json
     {
  "text": "Great place to stay!",
  "rating": 5,
  "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "place_id": "1fa85f64-5717-4562-b3fc-2c963f66afa6"
     }
     ```
and the expected response should be something like this:

     ```
     {
     "id": "2fa85f64-5717-4562-b3fc-2c963f66afa6",
     "text": "Great place to stay!",
     "rating": 5,
     "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
     "place_id": "1fa85f64-5717-4562-b3fc-2c963f66afa6"
     }
     ```
     
Possible Status codes:

* 201 Created -> review is successfully created
* 400 Bad Request -> input data is invalid


* Ensure reviews are correctly linked to both a user and a place
* Validate review attributes such as text and rating (1–5)
* Integrate the API layer with the Business Logic layer using the Facade pattern
* Support retrieving all reviews for a specific place
* Make reviews the only entity supporting deletion at this stage

This task ensures that review management is fully functional and properly integrated into the overall application architecture.

# Testing and Validation





