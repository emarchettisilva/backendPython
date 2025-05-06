# routes/cadastro_routes.py
from flask import Blueprint, request
from db import Db, Mode  
from . import valida

# Definindo o blueprint
cadastro_bp = Blueprint("cadastro_bp", __name__)

