# HBnB Technical Documentation

## Introduction
HBnB is a web application where users can list, find, and book places to stay. Hosts can create and manage property listings, while guests can search for accommodations by location, price, and other features.

This document explains how HBnB works, including the system structure, the business logic, and how key API calls are handled. It serves as a guide for building the application and understanding how its parts interact.

## High-Level Architecture

This package diagram depicts the system's high-level architecture using a layered design. The architecture is divided into three main layers: Presentation Layer, Business Logic Layer, and Persistence Layer. Each layer has clearly defined responsibilities and communicates only with its adjacent layers, ensuring loose coupling and high cohesion.

![PackageDiagram](https://github.com/user-attachments/assets/3c9da85e-c1c4-4b98-9d95-3f88f650362a)

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

**Conclusion**

This high-level architecture demonstrates how the system is structured around a clear separation of concerns. By organizing functionality into Presentation, Business Logic, and Persistence layers with well-defined responsibilities and controlled dependencies, the design promotes modularity, maintainability, and scalability, while keeping business rules and data access cleanly isolated from external interactions.

## Business Logic Layer

1. **Purpose of the diagram**

This diagram is like a map for our HBnB app. It shows the main parts we need, like users and places, and how they connect before we start writing the code.

![class](https://github.com/user-attachments/assets/c1458e4f-7db9-4a5e-beb5-cbe4dd02a337)

3. **Main Classes**
* **Users:** The people using the app (can be regular users or admins).
* **Place:** The listings that people can book.
* **Review:** Where users leave a rating and a comment about a place.
* **Amenity:** Extra features for a place, like WiFi or a pool.

3. **Design Decisions**
* **IDs:** We use UUID4 for IDs to make sure they are unique and safe.
* **Dates:** Each part has a "created" and "updated" date so we can track when things change.
* **Methods:** We added simple actions like create and delete to each class to keep the logic organized.

4. **How it fits in the app**
 
The Business Logic Layer is the middle part of the app. It takes information from the user, checks if it follows the rules, and then sends it to be saved in the database.

## API Interaction Flow

This section describes how the system components interact for selected API calls. The sequence diagrams illustrate the flow of control and data exchanged between the User (client), Presentation Layer (API), Business Logic Layer (HBnBFacade), and Persistence Layer (Database).

### 1) User Registration

**Goal**: Create a new user account while ensuring valid input and preventing duplicate registrations (email uniqueness).

![UserRegistration](https://github.com/user-attachments/assets/10074dde-97dd-4709-8d73-3ca01e45d9a9)

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

**Conclusion**

This sequence shows how a user registration request moves through the system.
It ensures proper validation, enforces business rules like email uniqueness and password security, and clearly defines the interaction between the API, business logic, and persistence layers.

### 2) Place Creation
This section explains how a Place is created in the HBnB application. When a user wants to create a new place, the API receives the request, the business logic checks and processes the data, and the information is saved in the database

<img width="1128" height="646" alt="image" src="https://github.com/user-attachments/assets/c202a7ba-da32-45ea-a6cc-2f5bd9b73272" />

This illustrates how a Place Creation request flows through the system layers and how the components interact:

**Flow Overview:**

* Client → API: User sends a request to create a new place.
* API → Business Logic (Facade): The facade coordinates validation and creation logic.
* Business Logic → Persistence: The Place data is saved in the database.

**Actors**
* Client: A user or frontend application sending an HTTP request

**System Components**
* PlaceController (API Layer): Handles incoming HTTP requests
* HBnBFacade (Business Logic Layer):Coordinates application logic and validation.
* Place Entity: Represents the place being created
* PlaceRepository (Persistence Layer): Manages data storage

**Explanatory Notes**

1. User Interaction

* The user sends a POST /places request with the place data (name, description, price, location, etc.).
* This starts the process through the system layers.

2. API Layer

* Checks that the user is logged in.
* Sends the data to the business logic layer.
* Returns success or error messages to the user.

3. Business Logic Layer

* Checks if the user has permission to create a place.
* Validates the place data to make sure it’s correct.
* Prepares the place to be saved in the database.

The diagram clearly shows how information flows from the client to the database and back.

**API Call: Create Place**
* Endpoint: POST /places
* Action: Create a new place listing
* Result: A new place is saved and returned to the clint

**Sequence Flow**
1. Client sends POST /places request with place data
2. PlaceController receives the request and forwards it to HBnBFacade
3. HBnBFacade validates the user and city
4. HBnBFacade creates a new Place entity
5. PlaceRepository saves the Place
6. HBnBFacade returns the created Place to PlaceController
7. PlaceController responds with HTTP 201 Created to the client

**Conclusion**
This sequence shows how a create-place request moves through the system. It ensures correct interaction between the API, business logic, and persistence layers. 

### 3) Review Submission
**Purpose of the Diagram:**

The following diagram shows exactly what happens when a user wants to write a review for a place. It helps us see how the information travels from the user's click all the way to being saved in our system. I created this to make sure the process is clear and follows a logical order.

 ![Review Submission](https://github.com/user-attachments/assets/7cff1db1-dda3-4479-915b-42bf40f7f6dc)

**Key Parts of the System:**
* **User:** This is the person using the app who sends the review details (like the rating and comment).
* **API:** This is the "front door" of our server. It receives the user's request first.
* **BusinessLogic:** I think of this as the "brain" of the app. It checks the rules and makes sure everything is correct.
* **Database:** This is our storage. It's where the review is kept forever if everything is right.

**My Design Decisions (Why I did it this way):**
* **Checking the data first:** I decided to let `the BusinessLogic` check if the review is valid before talking to the `Database`. This is better because we don't want to save empty or broken reviews.
* **The "Alt" Box:** I used this box to show two paths. If the data is right, we save it. If the data is missing something (like the rating), we show an error message. This makes the app more "friendly" for the user.
* **Waiting for Confirmation:** The `Database` sends a "Confirm Save" message back. I did this to make sure we only tell the user "Success" after we are 100% sure the data is actually saved.

**How it fits the Architecture:**

This design follows the "Layered" style we are learning. By keeping the `API`, `Logic`, and `Database` separate, our code stays organized. If we want to change how we save data later, we only need to change the `Database` part without breaking the rest of the app. This makes our project stronger and easier to fix.

### 4) Fetching a List of Places

This sequence diagram illustrates how the system retrieves a list of places based on optional search criteria such as location, category, or rating. It demonstrates how filtering logic is handled in the Business Logic Layer while maintaining proper separation of concerns across the architecture.

![FetchingListofPlaces](https://github.com/user-attachments/assets/30a1310c-c305-4633-957f-e376d8b94c81)

- The diagram highlights:
     - How client search requests are processed
     - The role of the Presentation Layer in validation and formatting
     - The facade’s responsibility in coordinating queries
     - Data retrieval from the Persistence Layer

**Actors / Components**

1. User (Client): Initiates the request to retrieve available places.
2. Presentation Layer (API): Receives the request, validates query parameters, and formats the response.
3. HBnBFacade (Business Logic Layer): Applies business rules, prepares filters, and coordinates data retrieval.
4. Persistence Layer (Database / Repository): Executes queries and returns matching place records.

**Sequence Summary**

1. User → API
- Sends a request to fetch places with optional filters
```(GET /places?location=&category=&rating=)```.

2. API
- Validates query parameters (e.g., rating range, location format).
- Normalizes filter values (default limits, pagination, etc.).

3. API → HBnBFacade
- Forwards the validated filter criteria.

4. HBnBFacade → Database
- Queries the persistence layer for places matching the criteria.

5. Database → HBnBFacade
- Returns a list of matching places (or an empty list).

6. HBnBFacade → API
- Returns the result set to the Presentation Layer.

7. API → User
- If places are found: returns ```200 OK``` with a list of places in JSON format.
- If no places are found: returns ```200 OK``` with an empty list.

**Data Flow Notes**

- Filtering and business rules (such as minimum rating or geographic constraints) are enforced in the Business Logic Layer, not in the API.
- The API layer is responsible only for:
- Input validation
- Request forwarding
- Response formatting
- Returning an empty list instead of an error ensures a consistent and user-friendly API behavior.
- The Persistence Layer remains unaware of request context and only executes data queries.

**Conclusion**

This sequence diagram shows how the system retrieves place data through a well-defined flow across the Presentation, Business Logic, and Persistence layers. It ensures proper validation, centralized business rules, and efficient data access while returning consistent and user-friendly responses.

## Overall Summary

This technical document serves as a comprehensive blueprint for the HBnB application, detailing its architecture, core business logic, and key system interactions. It consolidates all major design artifacts including high level architecture diagrams, business logic class diagrams, and API interaction sequence diagrams into a single, well structured reference that supports both implementation and ongoing development.

The document begins with an overview of the layered architecture, which consists of the Presentation Layer, Business Logic Layer, and Persistence Layer. This design enforces a clear separation of concerns, enhances maintainability, and promotes scalability. The use of the HBnBFacade as a central interface enables controlled communication between layers while shielding external clients from internal system complexity.

The Business Logic Layer is described in detail through class diagrams that define the system’s core domain entities, such as Users, Places, Reviews, and Amenities. These entities encapsulate business rules, validation logic, and domain behavior, ensuring that application rules remain centralized and consistent.

The API Interaction Flow section illustrates how real world use cases including user registration, place creation, review submission, and retrieving a list of places move through the system. The sequence diagrams clarify how requests are validated, processed, and persisted, emphasizing the responsibilities of each layer and reinforcing best practices such as data validation, security, and error handling.

Together, these sections establish a cohesive and well documented technical foundation for HBnB. This document functions not only as an implementation guide but also as a long term reference that supports collaboration, onboarding, debugging, and future system evolution.

## Documentation

- 📘 [Technical Documentation (Markdown)](https://github.com/11968-ship-it/holbertonschool-hbnb/blob/main/part1/README.md )
- 📄 [Technical Documentation (PDF)](https://github.com/user-attachments/files/24356381/README.pdf)
- 📝 [Technical Documentation (Word)](https://github.com/user-attachments/files/24356382/README.docx)
