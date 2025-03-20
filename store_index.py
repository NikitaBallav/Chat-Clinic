from src.helper import load_pdf_file, text_split, download_hugging_face_embeddings
from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from dotenv import load_dotenv
import os

load_dotenv()

Pinecone_API_Key = os.environ.get('Pinecone_API_Key')
os.environ["Pinecone_API_Key"] = Pinecone_API_Key

extracted_data=load_pdf_file(data='Data/')
text_chunks= text_split(extracted_data)
embeddings= download_hugging_face_embeddings()

pc = Pinecone(api_key=Pinecone_API_Key)

index_name="clinicvector"

pc.create_index(
    name=index_name,
    dimension=384,
    metric="cosine",
    spec=ServerlessSpec(
        cloud="aws",
        region="us-east-1"
    )
)

docsearch= PineconeVectorStore.from_documents(
    documents=text_chunks,
    index_name=index_name,
    embedding=embeddings

)

