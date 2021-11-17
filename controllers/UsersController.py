# @author: Jose Gonzalez Massini
from flask import jsonify, request
from models.UsersModel import usersModel

class UsersController():

  def __init__(self):
    self.model = usersModel

  # read users
  def showUsers(self):
    result = []
    users = self.model.readUsers()
    
    for i in range(len(users)):
      result.append({
        "uid":users[i][0],
        "uname":users[i][1],
        "uemail":users[i][2],
        "upassword":users[i][3],
        "urole":users[i][4]
      })

    return jsonify({"users":result})
    

  # read user 
  def showUser(self,id):
    user = self.model.readUser(id)

    result = {"uid":user[0], "uname":user[1],"uemail":user[2],"upassword":user[3],"urole":user[4]}

    return jsonify(result)

  # create user
  def insertUser(self, request):
    uemail = request.json['uemail']
    uname = request.json['uname']
    upassword = request.json['upassword']
    urole = request.json['urole']

    createdUser = self.model.createUser(uemail,uname,upassword,urole) 
    result = {"uid":createdUser[0], "uname":createdUser[1],"uemail":createdUser[2],"upassword":createdUser[3],"urole":createdUser[4]}
    
    return jsonify(result)

    
  # delete user
  def removeUser(self,id):
    return self.model.deleteUser(id)
    
  # update user 
  def editUser(self, id, request):
    uemail = request.json['uemail']
    uname = request.json['uname']
    upassword = request.json['upassword']
    urole = request.json['urole']

    return self.model.updateUser(id, uemail, uname, upassword, urole)

  # read user occupance
  def showUserOccupance(self,id):
    occupances=[]
    result = self.model.readUserOccupance(id)
    for i in range(len(result)):
      occupances.append({
        "uname":result[i][0],
        "uotimeframe":str(result[i][1])
      })
      
    return jsonify(occupances)


  # create user occupance
  def insertUserOccupance(self, id, request):
    uid = id
    uotimeframe = request.json['uotimeframe']
    return self.model.createUserOccupance(uid, uotimeframe)


  def whoAppointedRoom(self, request):
    timeframe = request.json['timeframe']
    result = self.model.appointedByWho(timeframe)

    roomAppointers = []

    for i in range(len(result)):
      roomAppointers.append({
        "uname": result[i][0],
        "rnumber": result[i][1]
      })


    return jsonify({"room appointers": roomAppointers})

  def roomMostUsed(self, id):
    result = self.model.usedRoomMost(id)
    mostUsedRoom = {"rnumber": result[0], "times used": result[1]}
    return jsonify({"most used room": mostUsedRoom})


  def mostBookedUsers(self):
    result = self.model.userMostBooked()
    userMostBooked = []

    for i in range(len(result)):
        userMostBooked.append({
            "uname": result[i][0],
            "user_appointments": result[i][1]
        })

    return jsonify({"most booked users": userMostBooked})

  def mostBookedWith(self, id):
    result = self.model.mostBooked(id)
    most_booked_with = []
    for i in range(len(result)):
      most_booked_with.append({
        "uname": result[i][0],
        "times booked": result[i][1]
      })

    return jsonify({"most_booked_with": most_booked_with})


usersController = UsersController()
      