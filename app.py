from flask import Flask, render_template, jsonify, request
from src.helper import download_hugging_face_embeddings
from langchain_pinecone import PineconeVectorStore
from langchain_community.llms import Ollama
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from src.prompt import *
import os

app = Flask(__name__)

load_dotenv()

Pinecone_API_Key = os.environ.get('Pinecone_API_Key')
os.environ["Pinecone_API_Key"] = Pinecone_API_Key

embeddings= download_hugging_face_embeddings()

index_name="clinicvector"
docsearch = PineconeVectorStore.from_existing_index(
    index_name= index_name,
    embedding=embeddings
)

retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k":3})

llm = Ollama(model="deepseek-r1:14b")

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)


question_answer_chain= create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)

# **Home Page Route**
@app.route("/")
def home():
    return render_template("index.html")  # Loads the chatbot UI

@app.route("/get", methods=["GET", "POST"])
def chat():
    # msg = request.form["msg"]
    msg = request.form.get("msg", "") if request.method == "POST" else request.args.get("msg", "")

    input = msg
    print(input)
    response = rag_chain.invoke({"input": msg})
    clean_answer = response['answer'].split("</think>\n\n")[-1]
    print("Response :", clean_answer)
    return str(clean_answer)


if __name__=="__main__":
    app.run(host="0.0.0.0",port=8080, debug=True)