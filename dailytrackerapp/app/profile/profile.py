# Store this code in 'app.py' file

from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import re
from app.profile import bp
from app.models import Account_Details
from app import db
import random
from flask_socketio import SocketIO
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import inspect
from sqlalchemy import text
from sqlalchemy.sql import func
def object_as_dict(obj):
	return {c.key: getattr(obj, c.key)
		for c in inspect(obj).mapper.column_attrs}

@bp.route('/profile')
def login():
	#account = Account_Details.query.filter_by(username=id, password=password1).first()
	return render_template('profile/profile.html', )

