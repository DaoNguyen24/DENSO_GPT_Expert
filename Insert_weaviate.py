import weaviate
import weaviate.classes as wvc
import os

client = weaviate.Client("http://localhost:8081")
print("weaviatedb is ready: ",client.is_ready())
client.schema.delete_all()
class_obj = {
    "class": "Denso_Document",
    "vectorizer": "text2vec-transformers",  # this could be any vectorizer
    "moduleConfig": {
        "text2vec-transformers": {  # this must match the vectorizer used
            "vectorizeClassName": False,
            "model": "paraphrase-multilingual-MiniLM-L12-v2",
        }
    },
    "properties": [
        {
            "name": "source",
            "dataType": ["text"],
            "moduleConfig": {
                "text2vec-transformers": {  # this must match the vectorizer used
                    "skip": True,
                    #"tokenization": "lowercase"
                }
            }
        },
        {
            "name": "page",
            "dataType": ["text"],
            "moduleConfig": {
                "text2vec-transformers": {  # this must match the vectorizer used
                    "skip": True  # Don't vectorize body
                    #"tokenization": "whitespace"
                }
            }
        },
        {
            "name": "content",
            "dataType": ["text"],
            "moduleConfig": {
                "text2vec-transformers": {  # this must match the vectorizer used
                    "vectorizePropertyName": True,  # vectorize body
                    #"tokenization": "whitespace"
                }
            }
        },
    ],
}
# Add the PDFDocument schema
client.schema.create_class(class_obj)

# Get the schema to verify that it worked
schema = client.schema.get()
#import json
#print(json.dumps(schema, indent=4))



import fitz
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

def split_document(docs,chunk_size = 1000, chunk_overlap = 0):
 text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    ) 
 chunks = text_splitter.create_documents([docs])
 return chunks


def insert_pdf_to_db(client, file_path):
    # Load pdf into pages
    pages = fitz.open(file_path)
    chunks = []  # create empty chunks
    # insert từng chunk vào chunk
    for page in pages:
        docs = split_document(page.get_text().replace('\n', ' ').lower())  # Return Langchain Documents list

        for doc in docs:
            chunk_data = {
                'content': doc.page_content,
                'source': str(pages.name), 
                'page': str(page.number)
            }
            chunks.append(chunk_data)

    # Insert chunks into the database
    

# Your existing code...
    #print (chunks)
    client = client
    import time
    counter = 0
    for chunk in chunks:
        try:
            client.batch.configure(batch_size=100)
            with client.batch as batch:
                batch.add_data_object(chunk,'Denso_Document')
            counter = counter+1
        except Exception as e:
            error_message = str(e)
            if "rate_limit_exceeded" in error_message:
                # Implement rate limit handling, e.g., wait for a certain period and retry
                print("Rate limit exceeded. Waiting and retrying...")
                time.sleep(5)  # Wait for 60 seconds
                client.batch.configure(batch_size=100)
                with client.batch as batch:
                    batch.add_data_object(chunk,'Denso_Document')
                counter = counter+1
            else:
                print(f"Error adding chunk: {chunk}. Error: {error_message}")

    print("Inserted ",counter," chunks to Denso_Document")
    


insert_pdf_to_db(client, file_path="sample pdf\LNCT800SoftwareApplicationManual-265-280.pdf")

object={
    'source': "Heloo",
    'page': 'Heloo',
    'content' : "Helooo Content"
}
client.batch.configure(batch_size=100)  # Configure batch
with client.batch as batch:
        batch.add_data_object(
            object,
            'Denso_Document',
            # tenant="tenantA"  # If multi-tenancy is enabled, specify the tenant to which the object will be added.
        )


#response = client.query.get("Denso_Document", ['source','page','content']).do()
response = (
    client.query
    .get("Denso_Document",properties=['source','page','content'])
    .with_bm25(
      query="Int3170"
    )
    .with_additional("score")
    .with_limit(3)
    .do()
)
import json
print(json.dumps(response, indent=2))

response2 = (
    client.query
    .get("Denso_Document", properties=['source','page','content'])
    .with_hybrid(
        query="Int3170",
    )
    .with_additional(["score", "explainScore"])
    .with_limit(3)
    .do()
)
print(json.dumps(response2, indent=2))

response3 = (
    client.query
    .get("Denso_Document", properties=['source','page','content'])
    .with_near_text({
        "concepts": ["Int3170"]
    })
    .with_limit(2)
    .with_additional(["distance"])
    .do()
)

print(json.dumps(response3, indent=2))