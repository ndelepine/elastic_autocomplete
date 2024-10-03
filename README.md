# Elasticsearch Autocomplete

## Description

Ce projet contient un backend pour envoyer des fausses données clients à Elasticsearch à l'aide de `Faker` en Python, ainsi qu'un frontend en Vue.js (à développer) pour requêter les données en mode autocomplete via une interface utilisateur.

## Prérequis

- Docker et Docker Compose
- Python 3.x
- Vue.js (si le frontend est implémenté)

## Installation

1. Clonez le projet :
   ```bash
   git clone https://github.com/moncompte/my-elasticsearch-project.git
   cd my-elasticsearch-project
   ```

2. Installez l'environnement virtuel :
   ```bash
   make venv
   ```

3. Lancez le service elasticsearch avec Docker Compose :
   ```bash
   cd backend
   docker-compose up -d
   ```
4. Lancez le script Python pour indexer des données clients :
   ```bash
   python index_faker_data.py
   ````
