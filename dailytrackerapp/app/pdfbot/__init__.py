# this is initialize auth blueprint
from flask import Blueprint
bp = Blueprint('pdfbot',__name__,template_folder='templates',static_folder='static')
from app.pdfbot import pdfbot