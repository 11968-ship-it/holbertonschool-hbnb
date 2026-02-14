# holbertonschool-hbnb

<img width="2454" height="1036" alt="logo" src="https://github.com/user-attachments/assets/9a7abc2b-d2e5-4437-a34b-1f6b803e1f76" />

## Project Description

holbertonschool-hbnb is a full-stack web application inspired by Airbnb.
The project is divided into four progressive parts, each building on the previous one to implement a complete web platform using a layered architecture.

The goal of the project is to apply concepts in:
* Object-Oriented Programming (OOP)
* RESTful API design
* Repository & Service (Facade) patterns
* SQL database design
* Frontend & Backend integration
* Authentication & authorization
* MVC-inspired architecture

## Architecture Overview
The project follows a layered architecture:
```
Presentation Layer (HTML/CSS/JS)
        ↓
API Layer (Flask Routes)
        ↓
Service Layer (Facade)
        ↓
Persistence Layer (Repositories)
        ↓
Database (SQLite)
```

## Project Structure
```
holbertonschool-hbnb/
├── base_files/              # Frontend (HTML, CSS, JS, images)
│   ├── add-place.html
│   ├── add_review.html
│   ├── index.html
│   ├── login.html
│   ├── place.html
│   ├── signup.html
│   ├── scripts.js
│   ├── styles.css
│   ├── images/
│
├── instance/                # SQLite databases
│   ├── app.db
│   ├── development.db
│   ├── hbnb.db
│
├── app/
│   ├── api/                 # REST API (v1)
│   │   ├── users.py
│   │   ├── places.py
│   │   ├── auth.py
│   │   ├── reviews.py
│   │   ├── amenities.py
│   │
│   ├── models/              # ORM Models
│   │   ├── user.py
│   │   ├── place.py
│   │   ├── review.py
│   │   ├── amenity.py
│   │   ├── place_amenity.py
│   │
│   ├── services/            # Business logic layer
│   │   ├── facade.py
│   │
│   ├── persistence/         # Data access layer
│   │   ├── repositories/
│   │   │   ├── user_repository.py
│   │   │   ├── place_repository.py
│   │   │   ├── review_repository.py
│   │   │   ├── amenity_repository.py
│   │   ├── repository.py
│   │
│   ├── sql/                 # Database schema & seed
│   │   ├── schema.sql
│   │   ├── seed.sql
│   │   ├── generate_admin_hash.py
│   │
│   ├── tests/
│   │   ├── test_models.py
│
├── run.py
├── config.py
├── requirements.txt
└── README.md
```

## Project Parts
🔹 **Part 1 – Core Models**
* Implemented core business models:
  * User
  * Place
  * Review
  * Amenity
* Implemented relationships between entities
* Applied OOP principles
* Unit testing for models

🔹 **Part 2 – Persistence Layer**
* Implemented Repository pattern
* Abstracted database operations
* Created base repository class
* Connected models to SQLite database
* Introduced schema.sql and seed.sql

🔹 **Part 3 – Service Layer & API**
* Implemented Facade pattern
* Built RESTful API (v1)
* Created endpoints:
  * Users
  * Places
  * Reviews
  * Amenities
  * Authentication
* Structured clean separation between layers

🔹 **Part 4 – Frontend Integration**
* Developed static frontend in base_files/
* Connected frontend to API using JavaScript (scripts.js)
* Implemented:
  * Login & Signup
  * Add Place
  * Add Review
  * View Place details
* Integrated authentication with API

## Tech Stack
### Backend
* Python 3
* Flask
* SQLAlchemy
* SQLite
* REST API

### Frontend
* HTML5
* CSS3
* JavaScript
* Dev Tools
* Git & GitHub

## Installation

1. Clone the repository:
```
git clone https://github.com/<USERNAME>/holbertonschool-hbnb.git
cd holbertonschool-hbnb
```

2. Install dependencies:
```
pip install -r requirements.txt
```

3. Initialize Database
```
sqlite3 instance/hbnb.db < app/sql/schema.sql
sqlite3 instance/hbnb.db < app/sql/seed.sql
```

4. Run the Application
```
python run.py
```

## Authentication
Authentication is handled via:
* Login endpoint (```/api/v1/auth```)
* Hashed passwords
* Admin hash generator (```generate_admin_hash.py```)

## Learning Outcomes
* Design scalable backend architecture
* Implement Repository & Facade patterns
* Build and consume REST APIs
* Integrate frontend with backend
* Manage relational databases
* Apply clean code principles

## Authors

* Lamyaa Mohammed Alghaihab 11955@holbertonstudents.com 💻✍️
* Thekira A. Ahmed 11968@holbertonstudents.com 💻✍️
* Yara K. Alrasheed 11982@holbertonstudents.com 💻✍️

**Holberton School**
