import pinecone
import os
from dotenv import load_dotenv,find_dotenv
import Model

load_dotenv(find_dotenv(),override=True)
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.environ.get("PINECONE_ENVIRONMENT")

embedding_model = Model.Embedding_Model.embedding_model
#sparse_model = Model.Sparse_Model.sparse_model
try: 
  import pickle
  with open('model.pkl', 'rb') as f:
    sparse_model = pickle.load(f)
except:
  sparse_model = Model.Sparse_Model.sparse_model

pinecone.init(
    api_key='b4c87a8a-b071-4410-b6ca-a61ec0e8e019',
    environment="gcp-starter"
)

# choose a name for your index
index_name = "test3"

if index_name not in pinecone.list_indexes():
    # create the index
    pinecone.create_index(
      index_name,
      dimension=Model.Embedding_Model.dim,
      metric="dotproduct",
      pod_type="s1"
    )
index = pinecone.Index(index_name)

###########################################################3

from langchain.docstore.document import Document
import fitz
from langchain.text_splitter import RecursiveCharacterTextSplitter

def split_document(docs,chunk_size = 1000, chunk_overlap = 0):
 text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    ) 
 chunks = text_splitter.create_documents([docs])
 return chunks

def load_data(file_path):
 #Load pdf into pages
 pages = fitz.open(file_path)
 chunks = []#create empty chunks
 data = []
 #insert từng chunk vào chunk
 id = 0
 for page in pages:
  docs = split_document(page.get_text().replace('\n', ' ').lower())#Return Langchain Documents list
  
  for doc in docs:
   chunk = Document(page_content=doc.page_content, metadata={'id' : id,'source': pages.name,'page': page.number,'text' : doc.page_content})
   id = id +1
   data.append(doc.page_content)
   chunks.append(chunk)
 sparse_model.fit(data)
 import pickle
 with open('model.pkl','wb') as f:
    pickle.dump(sparse_model,f)
 return chunks



def upsert_to_pinecone(chunks,index):
  sparse_vector = []
  dense_vector = []
  for chunk in chunks:
    sparse_vector.append(sparse_model.encode_documents(chunk.page_content))
    dense_vector.append(embedding_model.encode(chunk.page_content).tolist())
  
  
  upsert = []
  for chunk,sparse, dense in zip(chunks,sparse_vector,dense_vector):
    upsert.append({
      'id' : str(chunk.metadata['id']),
      'sparse_values': sparse,
      'values': dense,
      'metadata': chunk.metadata
    })
  index.upsert(upsert)



example_file_path = "sample pdf\LNCT800SoftwareApplicationManual-265-280.pdf"
chunks = load_data(example_file_path)
upsert_to_pinecone(chunks=chunks, index= index)

print(index.describe_index_stats())
#from langchain.vectorstores.pinecone import Pinecone
#from langchain.embeddings import HuggingFaceEmbeddings
#model = HuggingFaceEmbeddings(model_name = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
#docsearch = Pinecone.from_documents(chunks,embedding=model,index_name= index_name)



 

