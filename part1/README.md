# HBnB Technical Documentation

## Introduction
what this project about

## High-Level Architecture
![PackageDiagram1](https://github.com/user-attachments/assets/54af4884-1032-42e9-9884-49f828d9797d)

**Overview**

This package diagram depicts the system's high-level architecture using a layered design. The architecture is divided into three main layers: Presentation Layer, Business Logic Layer, and Persistence Layer. Each layer has clearly defined responsibilities and communicates only with its adjacent layers, ensuring loose coupling and high cohesion.

### 1. PresentationLayer
**Description**

The Presentation Layer is responsible for handling all external interactions with the system. It serves as the entry point for client requests and the exit point for system responses.

**Components**

- API
    - Exposes endpoints to external clients.
    - Handles request routing, input validation, and response formatting.
- Services
    - Coordinates request processing.
    - Delegates business operations to the Business Logic Layer.

**Responsibilities**

- Accept and validate client requests.
- Invoke business operations via the HBnBFacade interface.
- Return appropriate responses to clients.

**Dependencies**

- Depends on the BusinessLogicLayer through the HBnBFacade interface.
- Does not directly access models or the database.
________________________________________

### 2. BusinessLogicLayer
**Description**

The Business Logic Layer encapsulates the system's core domain logic. It defines business rules, workflows, and domain behavior while acting as an intermediary between the Presentation and Persistence layers.

**Components**
- «Interface» HBnBFacade
    - Defines a unified interface for business operations.
    - Exposes use cases required by the Presentation Layer.
    - Hides internal implementation details.
- Models
    - Represent domain entities (e.g., User, Place, Review).
    - Contain domain attributes and behavior.

**Responsibilities**
- Enforce business rules and validations.
- Coordinate domain operations.
- Manage interactions with the Persistence Layer.
- Provide a stable API to the Presentation Layer.

**Dependencies**
- Used by the PresentationLayer.
- Depends on the PersistenceLayer for data storage and retrieval.
________________________________________

### 3. PersistenceLayer
**Description**

The Persistence Layer is responsible for managing data persistence and retrieval. It abstracts database access and storage mechanisms from the rest of the system.

**Components**
- DatabaseAccess
    - Executes CRUD operations.
    - Manages database connections and queries.

**Responsibilities**

- Store and retrieve domain data.
- Isolate database-specific logic from business rules.
- Ensure data integrity and consistency.

**Dependencies**
- Accessed only by the BusinessLogicLayer.
- Has no dependency on upper layers.


## Business Logic Layer
fff
## API Interaction Flow

This section describes how the system components interact for selected API calls. The sequence diagrams illustrate the flow of control and data exchanged between the User (client), Presentation Layer (API), Business Logic Layer (HBnBFacade), and Persistence Layer (Database).

### 1) User Registration

**Goal**: Create a new user account while ensuring valid input and preventing duplicate registrations (email uniqueness).

![SequenceDiagram4](https://github.com/user-attachments/assets/e3a8fdf2-d27b-4d10-8004-26bf109eb803)

**Actors / Components**

* User (Client): Sends registration details
* Presentation Layer (API): Receives request, validates fields, triggers the use case
* Business Logic Layer (HBnBFacade): Applies business rules (uniqueness, hashing, entity creation)
* Persistence Layer (Database): Checks existing users and stores the new user record

**Sequence Summary**

1. **User → API**: ```Register(id, first_name, last_name, password, email)```
2. **API**: Validates required fields and request format.
3. **API → HBnBFacade**: Forwards a valid registration request.
4. **HBnBFacade → Database**: Checks if the email already exists (```Query user by email```).
5. **Database → HBnBFacade**: Returns result (```Email exists? true/false```).
6. If email exists:
  * **HBnBFacade → API**: Returns registration failure (```email in use```)
  * **API → User**: Displays error/failure response
7. If email does not exist:
  * **HBnBFacade**: Hashes password and builds the user entity.
  * **HBnBFacade → Database**: Saves user record (```Save user``` with id, hashed password, created/updated timestamps, etc.).
  * **Database → HBnBFacade**: Confirms record creation (```User created```).
  * **HBnBFacade → API**: Returns success.
  * **API → User**: Displays success response.

**Data Flow Notes**

* The API layer should never store passwords directly; it only forwards them to business logic for hashing.
* The Business Logic Layer is responsible for enforcing:
  * uniqueness constraints (email)
  * password hashing
  * entity creation rules
* The Persistence Layer handles the actual write operation and returns storage results.




### 2) Place Creation
This section explains how a Place is created in the HBnB application.
It shows how the request flows through the system layers and how components interact. It shows:

* The interaction between the client and API
* The role of the facade in orchestrating business logic
* Validation and persistence responsibilities

** Actors **
* Client: A user or frontend application sending an HTTP request

** System Components **
* PlaceController (API Layer): Handles incoming HTTP requests
* HBnBFacade (Business Logic Layer): Coordinates application logic
* Place Entity: Represents the place being created
* PlaceRepository (Persistence Layer): Manages data storage

** Key Notes **

* Validation occurs in the Business Logic layer.
* The controller does not interact directly with the database.
* Persistence is handled exclusively by the repository.

** API Call: Create Place **
* Endpoint: POST /places
* Action: Create a new place listing
* Result: A new place is saved and returned to the clint

** Sequence Flow **
1. Client sends POST /places request with place data
2. PlaceController receives the request and forwards it to HBnBFacade
3. HBnBFacade validates the user and city
4. HBnBFacade creates a new Place entity
5. PlaceRepository saves the Place
6. HBnBFacade returns the created Place to PlaceController
7. PlaceController responds with HTTP 201 Created to the client

<<<<<<< HEAD
** Conclusion **
This sequence shows how a create-place request moves through the system.
It helps ensure correct interaction between the API, business logic, and persistence layers. 
=======
### 3) Review Submission
Lamyaa here

### 4) Fetching a List of Places
>>>>>>> df7a355e64b4337136b855e95272496a342aced8
