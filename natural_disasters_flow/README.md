# Natural Disasters Data Pipeline

## Overview
This project is a data pipeline for collecting, processing, and visualizing information about natural disasters. The pipeline utilizes Apache Kafka for event streaming, MySQL for data storage, Apache Airflow for scheduling, and Dash for web-based visualization.

## Technologies Used
- **Python** – core programming language.
- **Apache Kafka** – message broker for data ingestion.
- **MySQL** – database for storing processed event data.
- **Apache Airflow** – workflow scheduler for automated data collection.
- **Dash (Plotly)** – web framework for data visualization.

## Project Structure
- **`api_requests.py`** – fetches natural disaster data from the API.
- **`producer.py`** – sends fetched data to Kafka.
- **`consumer.py`** – reads data from Kafka, processes it, and stores it in MySQL.
- **`tables.py`** – creates necessary tables in MySQL (run once for setup).
- **`dags/`** – contains Apache Airflow DAG to schedule data retrieval every 3 hours.
- **`charts/`** –
  - **`charts_functions.py`** – functions for generating different visualizations.
  - **`dash_app.py`** – web application for displaying statistics and charts.

## How It Works
1. **Data Ingestion** – `producer.py` fetches disaster data and sends it to Kafka.
2. **Processing & Storage** – `consumer.py` reads Kafka messages, processes the data, and stores it in MySQL.
3. **Automation** – Airflow DAG triggers data collection every 3 hours.
4. **Visualization** – `dash_app.py` periodically checks for new data in MySQL and updates the dashboard accordingly.
