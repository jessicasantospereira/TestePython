from flask import Flask, Blueprint, url_for
from api.views import health
from api.rotas import home
from api.rotas import cadastrar, editar, deletar

def create_app():
    api = Blueprint('api', __name__)
    app = Flask(__name__)

    # define api routes
    api.add_url_rule('/status', 'health', view_func=health, methods=['GET'])
    api.add_url_rule('/', 'home', view_func=home, methods=['GET'])
    api.add_url_rule('/cadastrar', 'cadastrar', view_func=cadastrar, methods=['GET','POST'])
    api.add_url_rule('/editar/<int:id>', 'editar', view_func=editar, methods=['GET','POST'])
    api.add_url_rule('/deletar/<int:id>', 'deletar', view_func=deletar, methods=['GET', 'POST'])

    app.register_blueprint(api, url_prefix='/api')
    return app