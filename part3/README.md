# holbertonschool-hbnb

## Project Overview
This project is part of the HBnB application and focuses on setting up the initial project structure and core architecture. The goal is to create a clean, modular Flask application with a clear separation of concerns, preparing the codebase for future development.


The application is organized into three main layers:

- **Presentation Layer**: RESTful API endpoints built with Flask and Flask-RESTx.
- **Business Logic Layer**: Core models and services that define application behavior.
- **Persistence Layer**: An in-memory repository used for object storage and validation (to be replaced by a database in later stages).


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

The application will run in debug mode.
No API routes are fully implemented yet, but the server should start without errors.

4. Install the ```flask-bcrypt``` plugin:

   ```
   pip install flask-bcrypt
   ```
   
5. Install ```flask-jwt-extended``` Library:

   ```
   pip install flask-jwt-extended
   ```

6. To initialize the database and create the table, run:

   ```
   flask shell
   >>> from app import db
   >>> db.create_all()
   ```
## Running the Application

Start the Flask development server:

   ```
   python3 run.py
   ```

# Core Business Logic Classes

# User Endpoints

1. **Create user:**

```bash
curl -X POST "http://127.0.0.1:5000/api/v1/users/" \
     -H "Content-Type: application/json" \
     -d '{
       "first_name": "John",
       "last_name": "Doe",
       "email": "john.doe@example.com",
       "password": "my_secure_password"
     }'
```
2. **Login:**

```bash
curl -X POST "http://127.0.0.1:5000/api/v1/auth/login" \
     -H "Content-Type: application/json" \
     -d '{
       "email": "john.doe@example.com",
       "password": "my_secure_password"
     }'
```

3. Create a New User as an Admin:

```
curl -X POST "http://127.0.0.1:5000/api/v1/users/"
     -d '{"email": "newuser@example.com", "first_name": "Admin", "last_name": "User"}'
     -H "Authorization: Bearer <admin_token>"
     -H "Content-Type: application/json"
```


4. Modify as an Admin:

```
curl -X PUT "http://127.0.0.1:5000/api/v1/users/<user_id>"
     -d '{"<first_name>": "mary"}'
     -H "Authorization: Bearer <admin_token>"
     -H "Content-Type: application/json"
```

At this point the ```User``` can't change the email or pawssord!


3. **Access a Protected Endpoint**

```bash
curl -X GET "http://127.0.0.1:5000/api/v1/auth/protected" -H "Authorization: Bearer your_generated_jwt_token"
```

# Place Endpoints

**1. Create place:**

```bash
curl -X POST "http://127.0.0.1:5000/api/v1/places/" \
  -H "Authorization: Bearer < your_token>" -H "Content-Type: application/json" \
  -d '{
    "title": "User A Luxury Villa",
    "description": "Amazing villa by the town",
    "price": 400.0,
    "latitude": 34.0540,
    "longitude": -118.2457,
    "amenities": []
  }'
```

**2. Update Place:**

```bash
curl -X PUT "http://127.0.0.1:5000/api/v1/places/4fbefac0-906e-453e-a160-a63d8110b341" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc2OTAwNzA0NCwianRpIjoiYmRkY2E5NjMtNzFmYi00NTY3LWE1MWYtY2YwZmE1Mzc3YTM5IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImM4ZTg4MzI2LTMzMTQtNGYwOC1iZmIxLTcwNDVkNWM3ZWYzZCIsIm5iZiI6MTc2OTAwNzA0NCwiY3NyZiI6IjZjNGM5ZTllLTkzMzYtNDcyMi04MzBkLWQwZThiYzkzMDU1YyIsImV4cCI6MTc2OTAwNzk0NCwiaXNfYWRtaW4iOmZhbHNlfQ.XAkHIApGy7PjAju7H_DQBd_PZ8cHcNCRnOqMNdmfD9k" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated Luxury Villa",
    "description": "Amazing villa by the beach",
    "price": 300.0,
    "latitude": 34.0522,
    "longitude": -118.2437,
    "amenities": []
  }'
```




## Table

The test for each as follow?

| left | Center | Right |
|:-----|:------:|------:|
| A    |    B   |   C   |

## Task: Implement Administrator Access Endpoints
Create Admin 
```bash
curl -X POST "http://127.0.0.1:5000/api/v1/auth/register-admin" \
     -H "Content-Type: application/json" \
     -d '{
       "email": "admin@example.com",
       "password": "admin123",
       "first_name": "Admin",
       "last_name": "User"
     }'

```
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

## Task: Map the User Entity to SQLAlchemy Model

## Task: Map the Place, Review, and Amenity Entities

### Test CRUL for place
1. Start your Flask app:
   ``` bash
   python3 run.py
   ```
2.  Create a place:
   ``` bash
curl -X POST "http://127.0.0.1:5000/api/v1/places/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Beach House",
    "description": "Beautiful oceanfront property",
    "price": 150.0,
    "latitude": 34.0522,
    "longitude": -118.2437
  }'
```
Expected Response:
``` bash
{
    "id": "fb3a127a-2a54-4052-87cf-371f1832b356",
    "title": "Beach House",
    "description": "Beautiful oceanfront property",
    "price": 150.0,
    "latitude": 34.0522,
    "longitude": -118.2437,
    "created_at": "2026-01-27T13:44:17.114732",
    "updated_at": "2026-01-27T13:44:17.114913"
}

```
3.  Get all places:
   ``` bash
curl -X GET "http://127.0.0.1:5000/api/v1/places/"
```
Expected Response:
```bash
[
    {
        "id": "fb3a127a-2a54-4052-87cf-371f1832b356",
        "title": "Beach House",
        "description": "Beautiful oceanfront property",
        "price": 150.0,
        "latitude": 34.0522,
        "longitude": -118.2437,
        "created_at": "2026-01-27T13:44:17.114732",
        "updated_at": "2026-01-27T13:44:17.114913"
    }
]

```

4.  Get place by ID (use ID from step 2):
   ``` bash
curl -X GET "http://127.0.0.1:5000/api/v1/places/<place_id>"
```
Expected Response:
```bash
{
    "id": "fb3a127a-2a54-4052-87cf-371f1832b356",
    "title": "Beach House",
    "description": "Beautiful oceanfront property",
    "price": 150.0,
    "latitude": 34.0522,
    "longitude": -118.2437,
    "created_at": "2026-01-27T13:44:17.114732",
    "updated_at": "2026-01-27T13:44:17.114913"
}

```
5.  Update place:
   ```bash
curl -X PUT "http://127.0.0.1:5000/api/v1/places/<place_id>" \
  -H "Content-Type: application/json" \
  -d '{
    "price": 175.0,
    "description": "Newly renovated!"
  }'
```
Expected Response:
```bash
{
    "id": "fb3a127a-2a54-4052-87cf-371f1832b356",
    "title": "Beach House",
    "description": "Newly renovated!",
    "price": 175.0,
    "latitude": 34.0522,
    "longitude": -118.2437,
    "updated_at": "2026-01-27T13:51:10.370791"
}

```

6.  Delete place:
   ```bash
curl -X DELETE "http://127.0.0.1:5000/api/v1/places/<place_id>"
```
Expected Response:
```bash
{
    "message": "Place deleted successfully"
}
```

7. Create a review:
```bash
curl -X POST http://127.0.0.1:5000/api/v1/reviews/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{"text":"This is a test review","rating":5}'
```

Expected Response:
```bash
{
    "id": "REVIEW_ID",
    "text": "This is a test review",
    "rating": 5,
    "created_at": "2026-01-27T14:13:10.838734",
    "updated_at": "2026-01-27T14:13:10.838736"
}
```

8. Retrieve all reviews:
```bash
curl -X GET http://127.0.0.1:5000/api/v1/reviews/
```

9. Retrieve review by review id:
```bash
curl -X GET http://127.0.0.1:5000/api/v1/reviews/REVIEW_ID
```

10. Update a review:
```bash
curl -X PUT http://127.0.0.1:5000/api/v1/reviews/REVIEW_ID \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{"text":"Updated review text"}'
```
Expected Response:
```bash
{
    "message": "Review updated successfully"
}
```

11. Delete a review:
```bash
curl -X DELETE http://127.0.0.1:5000/api/v1/reviews/REVIEW_ID \
  -H "Authorization: Bearer <TOKEN>"
```

Expected Response:
```bash
{
    "message": "Review deleted successfully"
}
```

12. Create Amenity
```bash
curl -X POST http://127.0.0.1:5000/api/v1/amenities/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -d '{"name":"WiFi"}'
```

Expected Response:
```bash
{
    "id": "d2693824-4505-4b5b-bd06-7ebde11352ea",
    "name": "WiFi"
}
```

13. Get All Amenities:
```bash
curl -X GET http://127.0.0.1:5000/api/v1/amenities/
```

14. Get Amenity by ID:
```bash
curl -X GET http://127.0.0.1:5000/api/v1/amenities/AMENITY_ID
```

15. Update Amenity:
```bash
curl -X PUT http://127.0.0.1:5000/api/v1/amenities/AMENITY_ID \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -d '{"name":"Air Conditioning"}'
```

Expected Response:
```bash
{ "message": "Amenity updated successfully" }
```

16. Delete Amenity:
```bash
curl -X DELETE http://127.0.0.1:5000/api/v1/amenities/AMENITY_ID \
  -H "Authorization: Bearer $ADMIN_TOKEN"
```

Expected Response:
```bash
{ "message": "Amenity deleted successfully" }
```
