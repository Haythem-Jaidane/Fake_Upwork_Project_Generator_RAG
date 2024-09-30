import csv
import json
import logging
from flask import Flask, jsonify, request
from langchain_community.llms import Ollama
from langchain_community.embeddings import OllamaEmbeddings
import chromadb
from flask_cors import CORS
from langchain_core.prompts import PromptTemplate

app = Flask(__name__)
CORS(app)

# Set up logging
logging.basicConfig(level=logging.DEBUG)

def load_csv_data(file_path):
    data = []
    with open(file_path, mode='r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            data.append(row)
    return data

def add_csv_data_to_chroma(data, chroma_client,ollama_emb, collection_name="upwork_projects"):
    collection = chroma_client.get_or_create_collection(name=collection_name)
    for idx, row in enumerate(data):
        content = f"Title: {row['title']}\nkeyphrases: {row['keyphrases']}\nabstract: {row['abstract']}"
        embedding_result = ollama_emb.embed_query(content)
        
        # Add the document with embeddings to the ChromaDB collection
        collection.add(
            embeddings=[embedding_result],
            documents=[content],
            ids=[str(idx)]
        )

        print("hello")
    logging.info(f"Added {len(data)} records to ChromaDB")

@app.route("/", methods=['POST'])
def home():
    logging.info("Received a request")
    try:
        ollama_emb = OllamaEmbeddings(
            model="mxbai-embed-large",
        )

        logging.info("Initialized embedding model")

        llm = Ollama(model="phi3", stop=["<|end|>"])
        logging.info("Initialized language model")

        """csv_data = load_csv_data("./train.csv")
        chroma_client = chromadb.PersistentClient(path="./db")
        add_csv_data_to_chroma(csv_data, chroma_client,ollama_emb)"""

        chroma_client = chromadb.PersistentClient(path="./db")

        data = json.loads(request.data)
        logging.debug(f"Received data: {data}")

        try:
            embed = ollama_emb.embed_query(data["prompt"])
            logging.debug(f"Query embedding: {embed}")
        except AttributeError as e:
            logging.error(f"Error with embedding query: {e}")
            raise


        collection = chroma_client.get_collection(name="upwork_projects")
        results = collection.query(query_embeddings=embed, n_results=10)
        logging.debug(f"Search response: {results}")

        template = """
        <|system|>You are a business consultant professional. You will generate fake project upwork description for freelancer to train.
        the contents is a real project from upwork inspire from them and write a real life fake project.
        you should make a project from the user skills and background your goal is to prepare user to real freelance so the project
        should be a next level in skils. 
        contents:\n\n{contents}\n\n
        <|end|>\n<|user|>\n{question}<|end|>\n<|assistant|>
        """
        prompt = PromptTemplate.from_template(template)

        formatted_contents = "\n".join([doc[0] for doc in results["documents"]])
        response = llm.invoke(prompt.format(question=data["prompt"], contents=formatted_contents))
        logging.debug(f"LLM response: {response}")

        return jsonify({"response": response})
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
