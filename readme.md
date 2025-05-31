# Flask Todo App with REST API and Swagger Documentation

## Description

This project is a simple Todo application built with Flask. It supports both a web UI and a REST API with full CRUD operations. The API is documented using Swagger, and the project includes unit tests with 100% coverage.

## Features

* Web interface for managing todos (add, edit, update, delete)
* REST API endpoints for managing todos
* Swagger UI for interactive API documentation
* Unit tests covering all API routes and core functionality

## Setup Instructions

### Requirements

* Python 3.x
* Flask
* Flask-SQLAlchemy
* Flasgger
* Pytest

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Ryannn20/flask-todo-app
   cd flask-todo-app
   ```

2. Create and activate a virtual environment:

   * On Windows:
     python -m venv venv
     venv\Scripts\activate


3. Install dependencies:
   pip install -r requirements.txt


4. Run the app:
   python app.py


   The app will be accessible at: [http://127.0.0.1:5000](http://127.0.0.1:5000)

### Access the Swagger UI

Open your browser at: [http://127.0.0.1:5000/apidocs/](http://127.0.0.1:5000/apidocs/)

## Running Tests

To run the unit tests with coverage:
pytest


## Branch Information

The new feature (REST API with Swagger and tests) is implemented on branch `feature/rest-api`.

## Notes

* The database used is SQLite for simplicity.
* Tests use an in-memory SQLite database to ensure isolation.


## Repository Links

-Original Repository: https://github.com/onurtacc/flask-todo-app

-Forked with Enhancements: https://github.com/Ryannn20/flask-todo-app/tree/feature/rest-swaggerapi
