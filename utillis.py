import os
from tempfile import NamedTemporaryFile
from langchain.document_loaders import UnstructuredFileLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import pinecone
from langchain.vectorstores import Pinecone
from langchain.embeddings import SentenceTransformerEmbeddings
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')
pinecone.init(api_key='fd9453a9-749a-4400-9673-053edbbe70a7', environment='gcp-starter')
index = pinecone.Index('imageprototpe')



def get_pdf_with_images(bytes_data):
    try:
        with NamedTemporaryFile(delete=False) as tmp:
            tmp.write(bytes_data)
            data = PyPDFLoader(tmp.name,extract_images=True)
            image_data=data.load()
        os.remove(tmp.name)
        return image_data
    except Exception as e:
        raise e



def split_docs(documents,chunk_size=1000,chunk_overlap=20):
  try:
      text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
      docs = text_splitter.split_documents(documents)
      return docs
  except Exception as e:
      raise e

def pinecone_clinet(docs):
    try:
        embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
        pinecone.init(
        api_key="fd9453a9-749a-4400-9673-053edbbe70a7",
        environment="gcp-starter")
        index_name = "imageprototpe"
        index = Pinecone.from_documents(docs, embeddings, index_name=index_name)
    except Exception as e:
        raise e

def find_match(input):
    try:
        input_em = model.encode(input).tolist()
        result = index.query(input_em, top_k=2, includeMetadata=True)
        return result['matches'][0]['metadata']['text']+"\n"+result['matches'][1]['metadata']['text']
    except Exception as e:
        raise e

