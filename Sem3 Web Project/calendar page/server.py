# (A) INIT
# (A1) LOAD MODULES
import sys
from flask import Flask, request, render_template, make_response
from datetime import datetime
from calendar import monthrange
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, DateTime
import re
from flask_socketio import SocketIO
from sqlalchemy import create_engine
from sqlalchemy import inspect
 
# (A2) FLASK SETTINGS + INIT
HOST_NAME = "localhost"
HOST_PORT = 5000
app = Flask(__name__)
# app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trial.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#Table class
class Events(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  start = db.Column(db.DateTime)
  end = db.Column(db.DateTime)
  text = db.Column(db.String, nullable=False)
  color = db.Column(db.String, nullable=False)
  bg = db.Column(db.String, nullable=False)

def object_as_dict(obj):
	return {c.key: getattr(obj, c.key)
		for c in inspect(obj).mapper.column_attrs}


# (B) SAVE EVENT
def save_event(start, end, txt, color, bg, id=None):

  # (B1) DATA & SQL
  data = (start, end, txt, color, bg,)
  if id is None:
    #sql = "INSERT INTO `events` (`start`, `end`, `text`, `color`, `bg`) VALUES (?,?,?,?,?)"
    new_event = Events(start = start, end = end, text = txt, color = color, bg = bg)
    db.session.add(new_event)
    
  else:
    #sql = "UPDATE `events` SET `start`=?, `end`=?, `text`=?, `color`=?, `bg`=? WHERE `id`=?"
    db.query(Events).\
    filter(Events.id == id).\
    update({'start': start, 'end': end, 'text': txt, 'color': color, 'bg': bg})
    data = data + (id,)

  # (B2) EXECUTE
  db.session.commit()
  return True

# (C) DELETE EVENT
def delete_event(id):
  # (C2) EXECUTE
  #"DELETE FROM `events` WHERE `id`=?", (id,)
  Events.query.filter(Events.id == id).delete()
  db.session.commit()
  return True

# (D) GET EVENTS
def get_event(month, year):

  # (D2) DATE RANGE CALCULATIONS
  daysInMonth = str(monthrange(year, month)[1])
  month = month if month>=10 else "0" + str(month)
  dateYM = str(year) + "-" + str(month) + "-"
  start = dateYM + "01 00:00:00"
  end = dateYM + daysInMonth + " 23:59:59"

  # (D3) GET EVENTS
    #"SELECT * FROM `events` WHERE ((`start` BETWEEN ? AND ?) OR (`end` BETWEEN ? AND ?) OR (`start` <= ? AND `end` >= ?))", (start, end, start, end, start, end)
  rows = Events.query.filter((Events.start.between(start, end)) | (Events.end.between(start, end)) | ((Events.start<=start) & (Events.end>=end)))
  if len(rows.all())==0:
    return None

  # s & e : start & end date
  # c & b : text & background color
  # t : event text
  data = {}
  for r_obj in rows:
    r = object_as_dict(r_obj)
    data[r['id']] = {
      "s" : r['start'], "e" : r['end'],
      "c" : r['color'], "b" : r['bg'],
      "t" : r['text']
    }
  return data

# (B) ROUTES
# (B1) CALENDAR PAGE
@app.route("/", methods=["GET", "POST"])
def index():
  return render_template("calendar.html")

# (B2) ENDPOINT - GET EVENTS
@app.route("/get/", methods=["POST"])
def get():
  data = dict(request.form)
  events = get_event(int(data["month"]), int(data["year"]))
  return "{}" if events is None else events

# (B3) ENDPOINT - SAVE EVENT
@app.route("/save/", methods=["POST"])
def save():
  data = dict(request.form)
  start_time = data["s"].split(" ")
  start_date = datetime(int(data["s"].split("-")[0]), int(data["s"].split("-")[1]), int(data["s"].split("-")[2][0:2]), int(start_time[1].split(":")[0]), int(start_time[1].split(":")[1]))
  end_time = data["e"].split(" ")
  end_date = datetime(int(data["e"].split("-")[0]), int(data["e"].split("-")[1]), int(data["e"].split("-")[2][0:2]), int(end_time[1].split(":")[0]), int(end_time[1].split(":")[1]))
  ok = save_event(start_date, end_date, data["t"], data["c"], data["b"], data["id"] if "id" in data else None)
  msg = "OK" if ok else sys.last_value
  return make_response(msg, 200)

# (B4) ENDPOINT - DELETE EVENT
@app.route("/delete/", methods=["POST"])
def delete():
  data = dict(request.form)
  ok = delete_event(data["id"])
  msg = "OK" if ok else sys.last_value
  return make_response(msg, 200)

# (C) START
if __name__ == "__main__":
  with app.app_context():
        db.create_all()
  app.run(HOST_NAME, HOST_PORT)

