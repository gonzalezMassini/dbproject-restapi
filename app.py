from flask import Flask, request, jsonify
from flask_cors import CORS
from controllers.createUserOccupance import create_user_occupance
from controllers.UsersController import usersController
from controllers.MeetingsController import meetingsController
from controllers.AttendeesController import attendeesController


# init app
app = Flask(__name__)
CORS(app)



# create user
@app.route('/create_user', methods=['POST'])
def create_user():
  return usersController.insertUser(request)

# delete user
@app.route('/delete_user/<int:id>', methods=['DELETE'])
def delete_user(id):
  return usersController.removeUser(id)

# read all users
@app.route('/read_users', methods=['GET'])
def get_users():
  return usersController.showUsers()

# read single user
@app.route('/read_user/<int:id>', methods=['GET'])
def get_user(id):
  return usersController.showUser(id)
# update user
@app.route('/update_user/<int:id>', methods=['PUT'])
def update_user(id):
  return usersController.editUser(id, request)

# read user occupance
@app.route('/user/<int:id>/read_user_occupance', methods=['GET'])
def user_occupance(id):
  return usersController.showUserOccupance(id)

# create user occupance

# update user occupance

# delete user occupance

# create meeting
@app.route('/create_meeting', methods=['POST'])
def create_meeting():
  # return 'trying to create a meet as user '
  return meetingsController.insertMeeting(request)

# read meetings
@app.route('/read_meetings', methods=['GET'])
def read_meetings():
  return meetingsController.showMeetings()

# read meeting
@app.route('/read_meeting/<int:id>', methods=['GET'])
def read_meeting(id):
  return meetingsController.showMeeting(id)

# update meeting

# delete meeting





# Isabel
# create attendee
@app.route('/create_attendee', methods=['POST'])
def create_attendee():
  return attendeesController.insertAttendee(request)

# delete attendee
@app.route('/delete_attendee/<int:id>', methods=['DELETE'])
def delete_attendee(id):
  return attendeesController.removeAttendee(id)

# show attendees
@app.route('/read_attendees', methods=['GET'])
def get_attendees():
  return attendeesController.showAttendees()

# show attendee
@app.route('/read_attendee/<int:id>', methods=['GET'])
def get_attendee(id):
  return attendeesController.showAttendee(id)

# update attendee
@app.route('/update_attendee/<int:id>', methods=['PUT'])
def update_attendee(id):
  return attendeesController.editAttendee(id, request)
# Isabel

@app.route('/')
def greet():
  return 'hello'

# run server
if __name__ == '__main__':
  app.run(debug=True)