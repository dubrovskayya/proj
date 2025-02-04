# Health Tracker

## Overview
This is a basic health tracking application that allows users to log their daily activity, sleep, nutrition, and workouts and receive statistical insights based on. 

Users log in or register on the start page and then access the home page, where they can view their statistics and fill out a form with relevant information for a selected date. The application processes the submitted data, performs calculations, and updates the user's statistics based on all available records stored in the database, while also taking into account the physical characteristics entered during registration.
## Technologies Used
- **Python**: programming language
- **Flask**: web framework for handling routes and user interactions
- **MySQL**: database for storing user data
- **SQLAlchemy**: ORM for database interaction

## Project Structure
- **`main.py`** – entry point for running the application
- **`db_session.py`** – manages database connections and sessions
- **`db_setup.py`** – initializes database tables and inserts required data (only needs to be run once)
- **`models.py`** – defines database table models
- **`routes.py`** – contains Flask routes for handling user interactions
- **`session_manager.py`** – manages user sessions and processes form data
- **`analytics.py`** – provides functions for analyzing user data


   
