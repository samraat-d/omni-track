# this is initialize auth blueprint
from flask import Blueprint
bp = Blueprint('todo',__name__,template_folder='templates',static_folder='static')
from app.todo import todo_list