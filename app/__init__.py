from flask import Flask
from app.controller.project import project

app = Flask(__name__)
app.register_module(project)

