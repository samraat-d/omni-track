
#pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib'
import datetime
import sys, json, flask, flask_socketio, httplib2, uuid
from flask import Response, request
from flask_socketio import SocketIO
from apiclient import discovery
from oauth2client import client
from googleapiclient import sample_tools
from rfc3339 import rfc3339
from dateutil import parser
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

app = flask.Flask(__name__)
socketio = SocketIO(app)

#Begin flask route
@app.route('/')
def index():
    if 'credentials' not in flask.session:
      return flask.redirect(flask.url_for('oauth2callback'))
    credentials = client.OAuth2Credentials.from_json(flask.session['credentials'])
    if credentials.access_token_expired:
        return flask.redirect(flask.url_for('oauth2callback'))
    return flask.render_template('index.html')

#Begin oauth callback route
@app.route('/oauth2callback')
def oauth2callback():
  flow = client.flow_from_clientsecrets(
      'client_secrets.json',
      scope='https://www.googleapis.com/auth/calendar',
      redirect_uri=flask.url_for('oauth2callback', _external=True))
  if 'code' not in flask.request.args:
    auth_uri = flow.step1_get_authorize_url()
    return flask.redirect(auth_uri)
  else:
    auth_code = flask.request.args.get('code')
    credentials = flow.step2_exchange(auth_code)
    flask.session['credentials'] = credentials.to_json()
    return flask.redirect(flask.url_for('index'))

#On event submission from client
@socketio.on('eventDesc')
def eventDesc(data):
    print("INSIDE eventDesc!!!")
    name = data['name']
    sTime =  parser.parse(data['sTime'])
    eTime =  parser.parse(data['eTime'])
    cid = data['cid']
    sConverted = rfc3339(sTime)
    eConverted = rfc3339(eTime)
    oauth(name, cid, sConverted, eConverted)

#On getCalendars event from client. Gets the calendar names and their corresponding ID's
@socketio.on("getCalendars")
def getCalendars():
    calendars = []
    try:
        credentials = client.OAuth2Credentials.from_json(flask.session['credentials'])
    except credError:
        print("did not assign credentials")
    http_auth = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http_auth)
    page_token = None
    while True:
      calendar_list = service.calendarList().list(pageToken=page_token).execute()
      for calendar_list_entry in calendar_list['items']:
        calendars.append({"name": calendar_list_entry['summary'], "id": calendar_list_entry['id']})
      now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
      print("Getting the upcoming 10 events")
      events_result = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=now,
            maxResults=10,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
      )
      events = events_result.get("items", [])

      if not events:
        print("No upcoming events found.")
        return

    # Prints the start and name of the next 10 events
      for event in events:
        start = event["start"].get("dateTime", event["start"].get("date"))
        print(start, event["summary"])

      page_token = calendar_list.get('nextPageToken')
      if not page_token:
        break
    flask_socketio.emit("calendarReturn", {"data": calendars})

#Function to add event into calendar selected
def oauth(name, cid, sTime, eTime):
    print(sTime)
    print(eTime)
    print(name)
    print(cid)
    try:
        credentials = client.OAuth2Credentials.from_json(flask.session['credentials'])
    except credError:
        print("did not assign credentials")
    http_auth = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http_auth)
    eventName = ""
    event = {
        'summary': name,
        'start': {
        'dateTime': sTime
        },
        'end': {
        'dateTime': eTime
        },
        'iCalUID': 'originalUID'
    }
    imported_event = service.events().import_(calendarId=cid, body=event).execute()
    print("Succesfully Imported Event")

@socketio.on("show_events")
def show_events():
  try:
    creds = client.OAuth2Credentials.from_json(flask.session['credentials'])
    service = build("calendar", "v3", credentials=creds)
    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
    print("Getting the upcoming 10 events")
    events_result = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=now,
            maxResults=10,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = events_result.get("items", [])

    if not events:
      print("No upcoming events found.")
      return

    # Prints the start and name of the next 10 events
    for event in events:
      start = event["start"].get("dateTime", event["start"].get("date"))
      print(start, event["summary"])

  except HttpError as error:
    print(f"An error occurred: {error}")

#Server setup
if __name__ == '__main__':
    app.secret_key = str(uuid.uuid4())
    socketio.run(
    app,
    allow_unsafe_werkzeug=True,
    #cors_allowed_origins="*",
    host='localhost',
    port=int(3000)
    )



