
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from dotenv import load_dotenv,find_dotenv
import os

####################STAGE 0 LOAD CONFIG ############################
load_dotenv(find_dotenv(),override=True)
CHROMADB_HOST = os.environ.get("CHROMADB_HOST")
CHROMADB_PORT = os.environ.get("CHROMADB_PORT")

#print(CHROMADB_HOST)


#####################STAGE 1 BUILDING VECTOR DB########################
###PArt1: Document input 
def load_pdf(file_path):
 loader = PyPDFLoader(file_path= file_path)
 docs = loader.load()
 return docs
 #print(docs)



#pages = load_pdf(sample_pdf_path)

###Part2: Chunking Document
#Spliter model
def split_document(docs,chunk_size = 800, chunk_overlap = 20):
 text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    
    # Splitting the documents into chunks
 chunks = text_splitter.create_documents([docs])
    
    # returning the document chunks
 return chunks


###Part3: Embedding Document
#Create embedding model 
from langchain.embeddings import HuggingFaceEmbeddings


###PART4: Insert to ChromaDB
import chromadb
import uuid
from langchain.vectorstores.chroma import Chroma
##chroma_client = chromadb.HttpClient(host='localhost', port=8000)
#chroma_client = chromadb.PersistentClient()
#collection = chroma_client.get_or_create_collection(name="document_DENSO",embedding_function=embedding_function)
#for chunk in chunks:
# collection.add(
#  ids = [str(uuid.uuid1())],
#  metadatas=chunk.metadata,
#  documents=chunk.page_content
# )
#
#langchain_chroma = chroma(
#    client = chroma_client,
#    collection_name="document_DENSO",
#    embedding_function=embedding_function,
#)
#
#query = "This manual should be considered a permanent part of the vehicle\nand should remain with the vehicle when it is resold."
#docs = langchain_chroma.similarity_search(query)
#print(docs[0].page_content)

 



###PART4.5 INSERT to Pinecone
#import pinecone
#from langchain.vectorstores.pinecone import Pinecone 
#
#pinecone.init(api_key=os.environ.get('PINECONE_API_KEY'), environment=os.environ.get('PINECONE_ENV'))
#
#index_name = 'denso-index'
#if index_name not in pinecone.list_indexes():
#    print(f'Creating index {index_name} ...')
#    pinecone.create_index(index_name, dimension=768, metric='cosine')
#    print('Done!')
#vector_store = Pinecone.from_documents(documents=chunks,embedding=model, index_name = index_name)
model = HuggingFaceEmbeddings(model_name = "bkai-foundation-models/vietnamese-bi-encoder")

def insert_pdf_to_db(file_path):
 #Load pdf into pages
 pages = load_pdf(file_path)
 chunks = []#create empty chunks
 #insert từng chunk vào chunk
 for page in pages:
  docs = split_document(page.page_content)
  for doc in docs:
   chunk = Document(page_content=doc.page_content, metadata=page.metadata)
   chunks.append(chunk)
 #Tạo DB
 
 db2 = Chroma.from_documents(chunks, model, persist_directory="./chroma_db")
 
  
sample_pdf_path = "sample pdf/cnxh.pdf"
sample_pdf_path2 = "sample pdf/kiemtraquyche.pdf"
sample_pdf_path3 = "sample pdf/ktpt.pdf"
#insert_pdf_to_db(sample_pdf_path2)
#insert_pdf_to_db(sample_pdf_path)
#insert_pdf_to_db(sample_pdf_path3)

query = '''Món quà tôi gửi tặng bạn.'''
db3 = Chroma(persist_directory="./chroma_db", embedding_function=model)
docs = db3.similarity_search(query)
for doc in docs:
 print(doc.page_content)
 print(doc.metadata)
 print("-"*50)

 
