from flask import Flask, request, jsonify, session
from flask_cors import CORS
import psycopg2
from controllers.UsersController import usersController
from controllers.AttendeesController import attendeesController
from controllers.MeetingsController import meetingsController
from controllers.RoomController import roomController
import psycopg2.extras


# from werkzeug.security import generate_password_hash, check_password_hash
# from datetime import timedelta
# redeploy
# git test

# init app
app = Flask(__name__)
CORS(app)

# CORS(app, origins=['localhost:3000'], supports_credentials=True)


# DB_HOST = "ec2-54-92-230-7.compute-1.amazonaws.com"
# DB_NAME = "d8c6ms71i5k6np"
# DB_USER = "bdtkvvsguqkyhw"
# DB_PASS = "31a04c2244936db8bfd5b69cc33966261cf08c00d2bfb41e83b3e20d67256ba1"

# conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)

# app.config['SECRET_KEY'] = 'elproyectotuyo'
  
# app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=10)

 
# @app.route('/gleatok/')
# def home():
#     # passhash = generate_password_hash('sejodio')
#     # print(passhash)
#     if 'username' in session:
#         username = session['username']
#         return jsonify({'message' : 'You are already logged in', 'username' : username})
#     else:
#         resp = jsonify({'message' : 'Unauthorized'})
#         # resp.status_code = 401
#         return resp
  
# @app.route('/gelatok/login', methods=['POST'])
# def login():
#     _json = request.json
#     _username = _json['username']
#     _password = _json['password']
#     print(_password)
#     # validate the received values
#     if _username and _password:
#         #check user exists          
#         cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
          
#         sql = "SELECT * FROM users WHERE uname=%s"
#         sql_where = (_username)
          
#         cursor.execute(sql, [sql_where])
#         row = cursor.fetchone()
#         username = row['uname']
#         password = row['upassword']
#         print(password)
#         if row:
#             # if check_password_hash(password, _password):
#             if password == _password:
#                 session['username'] = username
#                 cursor.close()
#                 return jsonify({'message' : 'You are logged in successfully'})
#             else:
#                 resp = jsonify({'message' : 'Bad Request - invalid password'})
#                 # resp.status_code = 400
#                 cursor.close()
#                 return resp
#     else:
#         resp = jsonify({'message' : 'Bad Request - invalid credendtials'})
#         # resp.status_code = 400
#         return resp
          
# @app.route('/gelatok/logout')
# def logout():
#     if 'username' in session:
#         session.pop('username', None)
#     return jsonify({'message' : 'You successfully logged out'})

# @Jose Gonzalez Massini

# Login
@app.route('/gelatok/login', methods=['POST'])
def loginTec():
  return usersController.login(request)


# create user
@app.route('/gelatok/create_user', methods=['POST'])
def create_user():
  return usersController.insertUser(request)

# delete user
@app.route('/gelatok/delete_user/<int:id>', methods=['DELETE'])
def delete_user(id):
  return usersController.removeUser(id)

# read all users
@app.route('/gelatok/read_users', methods=['GET'])
def get_users():

  # if 'username' in session:
  return usersController.showUsers()
  # else:
  #     resp = jsonify({'message' : 'Unauthorized'})
  #     resp.status_code = 401
  #     return resp

# read user single
@app.route('/gelatok/read_user/<int:id>', methods=['GET'])
def get_user(id):
  return usersController.showUser(id)

# update user
@app.route('/gelatok/update_user/<int:id>', methods=['PUT'])
def update_user(id):
  return usersController.editUser(id, request)

# read user occupance
@app.route('/gelatok/user/<int:id>/read_user_occupance', methods=['GET'])
def read_user_occupance(id):
  return usersController.showUserOccupance(id)

# create user occupance
@app.route('/gelatok/user/<int:id>/create_user_occupance', methods=['POST'])
def create_user_occupance(id):
  return usersController.insertUserOccupance(id, request)

# create meeting
@app.route('/gelatok/create_meeting', methods=['POST'])
def create_meeting():
  # return 'trying to create a meet as user '
  return meetingsController.insertMeeting(request)

# read meetings
@app.route('/gelatok/read_meetings', methods=['GET'])
def read_meetings():
  return meetingsController.showMeetings()

# read meeting
@app.route('/gelatok/read_meeting/<int:id>', methods=['GET'])
def read_meeting(id):
  return meetingsController.showMeeting(id)

# update meeting
@app.route('/gelatok/update_meeting/<int:id>', methods=['PUT'])
def update_meeting(id):
  # return meetingsController.editMeeting(id, request)
  return "not yet"

# delete meeting
@app.route('/gelatok/delete_meeting/<int:id>', methods=['DELETE'])
def delete_meeting(id):
  # return meetingsController.removeMeeting(id)
  return "not yet due to cascade delete"

# find available room at a time frame
@app.route('/gelatok/find_available_room', methods=['GET'])
def find_available_room():
  return roomController.findAvailableRoom(request)

# same without request, insted pass timeframe through the route params
@app.route('/gelatok/find_available_room/<string:timeframe>', methods=['GET'])
def find_available_room_route(timeframe):
  return usersController.findAvailableRoomRoute(timeframe)


# find who appointed a room at a certain time
@app.route('/gelatok/who_appointed_room', methods=['GET'])
def who_appointed_room():
  return usersController.whoAppointedRoom(request)

# top 10 most booked rooms
@app.route('/gelatok/most_booked_rooms', methods=['GET'])
def most_used_room():
  return roomController.mostUsedRoom()

# most used room by a user
@app.route('/gelatok/user/<int:id>/most_booked_rooms', methods=['GET'])
def most_used_room_byUser(id):
  return usersController.roomMostUsed(id)


# top 10 most booked users
@app.route('/gelatok/most_booked_users', methods=['GET'])
def most_booked_users():
  return usersController.mostBookedUsers()

# user logged in user has been most booked with
@app.route('/gelatok/user/<int:id>/most_booked_with')
def most_booked_with(id):
  return usersController.mostBookedWith(id)

# find busiest hours
@app.route('/gelatok/busiest_hours', methods=['GET'])
def busiest_hours():
  return meetingsController.busiestHours()


# time available for everyone in a meeting
@app.route('/gelatok/meeting/<int:id>/time_available', methods=['GET'])
def time_available(id):
  return meetingsController.timeAvailable(id)

  # @Jose Gonzalez Massini



# @Isabel Muniz
# create attendee
@app.route('/gelatok/create_attendee', methods=['POST'])
def create_attendee():
  return attendeesController.insertAttendee(request)

# delete attendee
@app.route('/gelatok/delete_attendee/<int:id>', methods=['DELETE'])
def delete_attendee(id):
  return attendeesController.removeAttendee(id)

# show attendees
@app.route('/gelatok/read_attendees', methods=['GET'])
def get_attendees():
  return attendeesController.showAttendees()

# show attendee
@app.route('/gelatok/read_attendee/<int:id>', methods=['GET'])
def get_attendee(id):
  return attendeesController.showAttendee(id)

# update attendee
@app.route('/gelatok/update_attendee/<int:id>', methods=['PUT'])
def update_attendee(id):
  return attendeesController.editAttendee(id, request)
# @Isabel Muniz


# @Ralph Ulysse

# create room
@app.route('/gelatok/create_room', methods=['POST'])
def create_room():
  return roomController.insertRoom(request)

# delete room
@app.route('/gelatok/delete_room/<int:id>', methods=['DELETE'])
def delete_room(id):
  return roomController.removeRoom(id)

# read single room
@app.route('/gelatok/read_room/<int:id>', methods=['GET'])
def get_room(id):
  return roomController.showRoom(id, request)

# read all rooms
@app.route('/gelatok/read_rooms', methods=['GET'])
def get_rooms():
    return roomController.showRooms()
  # return roomController.showRooms(request)

# update room
@app.route('/gelatok/update_room/<int:id>', methods=['PUT'])
def update_room(id):
  return roomController.editRoom(id, request)

# room occupance routes

# read room occupance
@app.route('/gelatok/room/<int:id>/read_room_occupance', methods=['GET'])
def room_occupance(id):
  return roomController.showRoomOccupance(id, request)

# delete room
@app.route('/gelatok/delete_room_occupance/<int:id>', methods=['DELETE'])
def delete_room_occupance(id):
  return roomController.removeRoomOccupance(id)

# create room occupance
@app.route('/gelatok/room/<int:id>/create_room_occupance', methods=['POST'])
def create_room_occupance(id):
  return roomController.insertRoomOccupance(id,request)

# update room occupance
@app.route('/gelatok/update_room_occupance/<int:id>', methods=['PUT'])
def update_room_occupance(id):
  return roomController.editRoomOccupance(id, request)
# @Ralph Ulysse


# @app.route('/')
# def greet():
#   return 'hello world'

# run server
if __name__ == '__main__':
  app.run(debug=True)