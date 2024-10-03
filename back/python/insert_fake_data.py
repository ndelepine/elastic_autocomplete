from elasticsearch import Elasticsearch
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


# Indexer des fausses données dans Elasticsearch
def index_fake_data(es_instance, index_name, num_docs):
    for i in range(num_docs):
        # Générer des fausses données
        doc = {
            'name': fake.last_name(),
            'first_name': fake.first_name(),
            'email': fake.email(),
            'address': fake.address(),
            'created_at': fake.date_time_this_decade(),
            'job': fake.job()
        }
        # Indexer le document dans Elasticsearch
        res = es_instance.index(index=index_name, body=doc)
        print(f'Document {i+1} indexé avec l\'ID {res["_id"]}')


# Création de l'index et indexation de 10 documents
if __name__ == "__main__":
    INDEX_NAME = 'clients'

    # Créer l'index avec le mapping d'autocomplétion
    create_index_with_mapping(es, INDEX_NAME)

    # Indexer 10 documents
    index_fake_data(es, INDEX_NAME, 100)
