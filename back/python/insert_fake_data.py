from elasticsearch import Elasticsearch, helpers
from faker import Faker

# Connect to Elasticsearch
es = Elasticsearch([{"host": "localhost", "port": 9200, "scheme": "http"}])

# Check if Elasticsearch is ready
if not es.ping():
    raise ValueError("Elasticsearch is not responding!")

# Create a Faker instance
fake = Faker()


# Create index mapping to enable autocomplete on the name and first name fields
def create_index_with_mapping(es_instance: Elasticsearch, index_name):
    # Delete the index if it already exists
    if es_instance.indices.exists(index=index_name):
        es_instance.indices.delete(index=index_name)

    # Index mapping
    mappings = {
        "mappings": {
            "properties": {
                "name": {
                    "type": "completion"  # Enable autocomplete
                },
                "first_name": {
                    "type": "completion"  # Enable autocomplete
                },
                "email": {"type": "keyword"},
                "address": {"type": "text"},
                "created_at": {"type": "date"},
                "job": {"type": "text"},
            }
        }
    }

    # Create the index with the mapping
    es_instance.indices.create(index=index_name, body=mappings)


# Generate a batch of documents to be indexed in a single request
def generate_bulk_data(index_name, num_docs):
    # Create a generator for the documents to be indexed in bulk mode
    for _ in range(num_docs):
        # Generate fake data
        doc = {
            "_index": index_name,
            "_source": {
                "name": fake.last_name(),
                "first_name": fake.first_name(),
                "email": fake.email(),
                "address": fake.address(),
                "created_at": fake.date_time_this_decade(),
                "job": fake.job(),
            },
        }
        yield doc


# Use the bulk API to index the documents in a single request
def bulk_index_data(es_instance, index_name, num_docs, chunk_size=500):
    # Use the helpers.bulk function to send data in chunks
    helpers.bulk(
        es_instance, generate_bulk_data(index_name, num_docs), chunk_size=chunk_size
    )


# Create the index and index the documents
if __name__ == "__main__":
    INDEX_NAME = "clients"

    # Create the index with autocomplete mapping
    create_index_with_mapping(es, INDEX_NAME)

    # Index 10,000 documents using the bulk API
    bulk_index_data(es, INDEX_NAME, 100)
