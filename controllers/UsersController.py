from flask import jsonify, request
from models.UsersModel import usersModel

class UsersController():

  def __init__(self):
    self.model = usersModel

  # read users
  def showUsers(self):
    return self.model.readUsers()
    

  # read user 
  def showUser(self,id):
    return self.model.readUser(id)

  # create user
  def insertUser(self, request):
    uemail = request.json['uemail']
    uname = request.json['uname']
    upassword = request.json['upassword']
    urole = request.json['urole']
    
    return self.model.createUser(uemail,uname,upassword,urole)

    
# delete user
  def removeUser(self,id):
    return self.model.deleteUser(id)
    
  # update user 
  def editUser(self, name, price, quantity):
    return null

usersController = UsersController()
      