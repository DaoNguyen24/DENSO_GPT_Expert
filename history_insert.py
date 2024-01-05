import weaviate
import weaviate.classes as wvc
import os

def insert_history_to_db(client, doc, class_obj):
    #print (chunks)
    client = client
    import time
    counter = 0
    try:
        client.batch.configure(batch_size=100)
        with client.batch as batch:
            batch.add_data_object(doc,class_obj)
    except Exception as e:
        error_message = str(e)
        if "rate_limit_exceeded" in error_message:
            # Implement rate limit handling, e.g., wait for a certain period and retry
            print("Rate limit exceeded. Waiting and retrying...")
            time.sleep(5)  # Wait for 60 seconds
            client.batch.configure(batch_size=100)
            with client.batch as batch:
                batch.add_data_object(doc,class_obj)
        else:
            print(f"Error adding chunk: Error: {error_message}")

    print(("Inserted to {} Denso_Document from ").format(doc["source"]))


def insert_history(dicts):
 client = weaviate.Client("http://localhost:8081")
 
 print("weaviatedb is ready: ",client.is_ready())

 
 if client.schema.exists("Denso_history"):
  print("Denso_history class has already exists")
 else:
  class_obj = {
     "class": "Denso_history",
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
             "name": "month",
             "dataType": ["text"],
             "moduleConfig": {
                 "text2vec-transformers": {  # this must match the vectorizer used
                     "skip": True  # Don't vectorize body
                     #"tokenization": "whitespace"
                 }
             }
         },
         {
             "name": "year",
             "dataType": ["text"],
             "moduleConfig": {
                 "text2vec-transformers": {  # this must match the vectorizer used
                     "skip": True  # Don't vectorize body
                     #"tokenization": "whitespace"
                 }
             }
         },
         {
             "name": "machine_name",
             "dataType": ["text"],
             "moduleConfig": {
                 "text2vec-transformers": {  # this must match the vectorizer used
                     "skip" : True,  # vectorize body
                     #"tokenization": "whitespace"
                 }
             }
         },
         {
             "name": "code",
             "dataType": ["text"],
             "moduleConfig": {
                 "text2vec-transformers": {  # this must match the vectorizer used
                     "skip" : True,  # vectorize body
                     #"tokenization": "whitespace"
                 }
             }
         },
         {
             "name": "line",
             "dataType": ["text"],
             "moduleConfig": {
                 "text2vec-transformers": {  # this must match the vectorizer used
                     "skip" : True,  # vectorize body
                     #"tokenization": "whitespace"
                 }
             }
         },
         
 
     ],
  }
  client.schema.create(class_obj)
  print("Created Denso_history class")
  for dict in dicts:
     insert_history_to_db(client=client,doc=dict,class_obj="Denso_history")


if __name__ == "__main__":
   
