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
fff
