from flask import Blueprint
bp = Blueprint('auth', __name__)
from . import routes  # keeps imports local to the package
