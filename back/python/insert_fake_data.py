from elasticsearch import Elasticsearch, helpers
from faker import Faker

# Connexion à Elasticsearch
es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme':'http'}])

# Vérifier si Elasticsearch est prêt
if not es.ping():
    raise ValueError("Elasticsearch ne répond pas!")

# Créer une instance Faker
fake = Faker()

# Créer le mapping de l'index pour activer l'autocomplétion sur les champs nom et prénom
def create_index_with_mapping(es_instance, index_name):
    # Supprimer l'index s'il existe déjà
    if es_instance.indices.exists(index=index_name):
        es_instance.indices.delete(index=index_name)

    # Mapping de l'index
    mappings = {
        "mappings": {
            "properties": {
                "name": {
                    "type": "completion"  # Activer l'autocomplétion
                },
                "first_name": {
                    "type": "completion"  # Activer l'autocomplétion
                },
                "email": {"type": "keyword"},
                "address": {"type": "text"},
                "created_at": {"type": "date"},
                "job": {"type": "text"}
            }
        }
    }

    # Créer l'index avec le mapping
    es_instance.indices.create(index=index_name, body=mappings)


# Générer un lot de documents à indexer en une seule requête
def generate_bulk_data(index_name, num_docs):
    # Créer un générateur pour les documents à indexer en mode bulk
    for _ in range(num_docs):
        # Générer des fausses données
        doc = {
            '_index': index_name,
            '_source': {
                'name': fake.last_name(),
                'first_name': fake.first_name(),
                'email': fake.email(),
                'address': fake.address(),
                'created_at': fake.date_time_this_decade(),
                'job': fake.job()
            }
        }
        yield doc

# Utiliser l'API bulk pour indexer les documents en une seule requête
def bulk_index_data(es_instance, index_name, num_docs, chunk_size=500):
    # Utilisation de la fonction helpers.bulk pour envoyer en chunks les données
    helpers.bulk(es_instance, generate_bulk_data(index_name, num_docs), chunk_size=chunk_size)

# Création de l'index et indexation des documents
if __name__ == "__main__":
    INDEX_NAME = 'clients'

    # Créer l'index avec le mapping d'autocomplétion
    create_index_with_mapping(es, INDEX_NAME)

    # Indexer 10 000 documents en utilisant l'API bulk
    bulk_index_data(es, INDEX_NAME, 100000)
