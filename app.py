from flask import Flask, request, jsonify
from flask_cors import CORS
from controllers.createUserOccupance import create_user_occupance
from controllers.UsersController import usersController


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
@app.route('/users', methods=['GET'])
def get_users():
  return usersController.showUsers()

# read single user
@app.route('/user/<int:id>', methods=['GET'])
def get_user(id):
  return usersController.showUser(id)









# update user
@app.route('/update_user/<int:id>', methods=['PUT'])
def update_user(id):
  return userUpdate(id, request, postgresql)







# user occupance
@app.route('/user/<int:id>/user_occupance',methods=['POST'])
def user_occupance(id):
  return create_user_occupance(id, mysql, request)

# create meeting
@app.route('/user/<int:id>/create_meeting', methods=['POST'])
def create_meeting(id):
  return 'trying to create a meet as user '+ str(id)

# room occupance
@app.route('/user/<int:id>/room_occupance',methods=['POST'])
def room_occupance(id):
  return 'trying to occupy a room as a staff'


@app.route('/')
def greet():
  return 'hello'

# run server
if __name__ == '__main__':
  app.run(debug=True)