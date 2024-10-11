from flask import Blueprint
from Controllers.ProjectController import ProjectController

project = ProjectController()


project_route = Blueprint('project_route', __name__)
project_route.route('/', methods=['POST'])(project.generate)