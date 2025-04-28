# Elasticsearch Autocomplete

## Description

This project contains a backend to send fake customer data to Elasticsearch using `Faker` in Python, as well as a frontend in Vue.js to query the data in autocomplete mode via a user interface.

The ElasticSearch server is run via Docker Compose and comes with Kibana to visualize and manage the indexes.

The Kibana instances is available on port 5601 by default.

## Requirements

- Docker and Docker Compose
- Python 3.x
- Vue.js (if the frontend is implemented)

## Installation

1. Clone the project:

   ```bash
   git clone https://github.com/myaccount/my-elasticsearch-project.git
   cd my-elasticsearch-project

   ```

2. Set up the virtual environment:

   ```bash
   make venv
   ```

3. Start the Elasticsearch service with Docker Compose:

   ```bash
   cd back
   docker-compose up -d
   ```

   or

   ```bash
   make run-back
   ```

4. Run the Python script to index fake customer data (created with Faker):

   ```bash
   python index_faker_data.py
   ```

   or

   ```bash
   make insert-index
   ```

5. Run the front (Vue.JS) :

   ```bash
   cd front
   npm run dev
   ```

   or

   ```bash
   make run-front
   ```
