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

        data = json.loads(request.data)
        logging.debug(f"Received data: {data}")

        try:
            embed = ollama_emb.embed_query(data["prompt"])
            logging.debug(f"Query embedding: {embed}")
        except AttributeError as e:
            logging.error(f"Error with embedding query: {e}")
            raise

        try:
            embedding_result = ollama_emb.embed_query(
            "Need a good MERN developer to work on a short project.  Must be experienced with Node. A big plus if you know native and web development languages such as Flutter, Swift, Kotlin/Java. Previous experience building a social membership app with personalised videos and group messaging would be ideal or social apps that use video, images and messaging\
            The app is mostly built, we need to make a few edits and a supporting dashboard. Please bear in mind we are very limited with our budget so we don't have much flexibility on the price\
            \
            Fix a few website bugs\
            Re-structure the backend for its new use case and improve performance\
            Stripe integration\
            Build admin dashboard e.g. club side, admin side etc\
            Fix bugs\
            Connect frontend to backend\
            \
            Check kaadi.app for more info"
            )
            logging.debug(f"Embedding result: {embedding_result}")
        except AttributeError as e:
            logging.error(f"Error with embedding query: {e}")
            raise
        #vectorstore = Chroma("langchain_store", ollama_emb)

        chroma_client = chromadb.PersistentClient(path="./db")
        collection = chroma_client.get_or_create_collection(name="upwork_projects")

        collection.add(
            embeddings=[embedding_result],
            documents=[
                "Need a good MERN developer to work on a short project.  Must be experienced with Node. A big plus if you know native and web development languages such as Flutter, Swift, Kotlin/Java. Previous experience building a social membership app with personalised videos and group messaging would be ideal or social apps that use video, images and messaging\
                The app is mostly built, we need to make a few edits and a supporting dashboard. Please bear in mind we are very limited with our budget so we don't have much flexibility on the price\
                \
                Fix a few website bugs\
                Re-structure the backend for its new use case and improve performance\
                Stripe integration\
                Build admin dashboard e.g. club side, admin side etc\
                Fix bugs\
                Connect frontend to backend\
                \
                Check kaadi.app for more info"
            ],
            ids=["1"]
        )

        results = collection.query(
            query_embeddings=embed,
            n_results=3 
        )

        logging.debug(f"search response: {results}")

        template = """
        <|system|>You are a business consultant professional. You will generate fake project upwork description for freelancer to train.
        the contents is a real project from upwork inspire from them and write a real life fake project.
        you should make a project from the user skills and background your goal is to prepare user to real freelance so the project
        should be a next level in skils. 
        contents:\n\n{contents}\n\n
        <|end|>\n<|user|>\n{question}<|end|>\n<|assistant|>
        """
        prompt = PromptTemplate.from_template(template)

        response = llm.invoke(prompt.format(question=data["prompt"], contents=results))
        logging.debug(f"LLM response: {response}")

        return jsonify({"response": response})
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
