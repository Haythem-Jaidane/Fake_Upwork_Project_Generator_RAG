import json
import logging
from flask import Flask, jsonify, request
from langchain_community.llms import Ollama
from langchain_community.embeddings import OllamaEmbeddings
import chromadb
from langchain_core.prompts import PromptTemplate

from Services.ProjectService import ProjectService

class ProjectController:

    def __init__(self):
        self.service = ProjectService()


    def generate(self):
        try:
            response = self.service.generate()

            return jsonify({"response": response})
        except Exception as e:
            logging.error(f"Error occurred: {e}")
            return jsonify({"error": str(e)}), 500