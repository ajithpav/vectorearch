from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
from bson import ObjectId

# Connect to MongoDB
client = MongoClient("mongodb+srv://polarisqadbadmin:dbp0l%40ris%401qa@polaris-qa.hurip.mongodb.net/test?authSource=admin")
db = client["test"]

# Initialize the embedding model
embedding_model = SentenceTransformer("thenlper/gte-large")

def get_embeddings(text):
    if not text.strip():
        return []
    embedding = embedding_model.encode(text)
    return embedding.tolist()

def store_embeddings(db, collection_name, document_id, embeddings):
    print(f"Storing embeddings for Collection: {collection_name}, Document ID: {document_id}")
    collection = db[collection_name]
    updated_document = {"$set": {"embeddings": embeddings}}

    try:
        result = collection.update_one({'_id': ObjectId(document_id)}, updated_document)
        if result.matched_count:
            print(f"Success: Embeddings stored for Document ID {document_id} in Collection {collection_name}")
        else:
            print(f"Skipped: Document ID {document_id} was not updated in Collection {collection_name}")
    except Exception as e:
        print(f"Error: {str(e)}")
        
def process_collection(db, collection_name):
    collection = db[collection_name]
 
    for document in collection.find():
        document_id = str(document['_id'])  
        document_data = {}
        for column, text in document.items():
            if column not in ['_id', 'embeddings']:
                embedded_vectors = get_embeddings(str(text))
                document_data[column] = embedded_vectors

        if document_data:
            store_embeddings(db, collection_name, document_id, document_data)

# Extract all collections and process them
all_collections = db.list_collection_names()

for collection_name in all_collections:
    print(f"\nProcessing collection: {collection_name}")
    process_collection(db, collection_name)