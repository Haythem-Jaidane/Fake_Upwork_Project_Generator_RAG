from flask import Blueprint
from Controllers.ProjectController import *


project_route = Blueprint('project_route', __name__)
project_route.route('/', methods=['POST'])(home)