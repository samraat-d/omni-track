# this is initialize auth blueprint
from flask import Blueprint
bp = Blueprint('calendar',__name__,template_folder='templates',static_folder='static')
from app.calendar import calendar