# this is initialize login blueprint
from flask import Blueprint
bp = Blueprint('calculators',__name__,template_folder='templates',static_folder='static')
from app.calculators import calculators
