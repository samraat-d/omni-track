# this is initialize login blueprint
from flask import Blueprint
login = Blueprint('login',__name__,template_folder='templates',static_folder='static')
from app.login import login_page
