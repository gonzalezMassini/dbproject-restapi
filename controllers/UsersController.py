# @author: Jose Gonzalez Massini
from flask import jsonify, request
from models.UsersModel import usersModel

class UsersController():

  def __init__(self):
    self.model = usersModel


  def login(self, request):
    uemail = request.json['uemail']
    upassword = request.json['upassword']

    result = self.model.signin(uemail, upassword)

    if type(result) == dict:
      print({"uid": result})
      # return jsonify({"uid": result})
      return jsonify(result)
    else:
      print(result)
      return jsonify({"uid": result})

      







  # read users
  def showUsers(self):
    result = []
    users = self.model.readUsers()
    
    # print(users)
    for i in range(len(users)):
      result.append({
        "uid":users[i][0],
        "uemail":users[i][1],
        "upassword":users[i][2],
        "urole":users[i][3],
        "uname":users[i][4]
      })

    return jsonify({"users":result})
    

  # read user 
  def showUser(self,id):
    user = self.model.readUser(id)
    
    result = {"uid":user[0], "uemail":user[1],"upassword":user[2],"urole":user[3],"uname":user[4]}

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

    return self.model.updateUser(id, uemail, uname, upassword)

  # read user occupance
  def showUserOccupance(self,id):
    occupances=[]
    result = self.model.readUserOccupance(id)
    # print(result)
    for i in range(len(result)):
      occupances.append({
        "uname":result[i][0],
        "uotimeframe":str(result[i][1]),
        "title":result[i][2]
      })
      
    return jsonify(occupances)


  # create user occupance
  def insertUserOccupance(self, id, request):
    uid = id
    uotimeframe = request.json['uotimeframe']
    title = request.json['title']
    return self.model.createUserOccupance(uid, uotimeframe, title)


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
    if(type(result) != tuple):
      return 'riip'
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
    if(type(result) != list):
      # print('none type')
      return ''
    most_booked_with = []
    for i in range(len(result)):
      most_booked_with.append({
        "uname": result[i][0],
        "times booked": result[i][1]
      })

    return jsonify({"most_booked_with": most_booked_with})


  def meetingOccupances(self, id):
    result = self.model.meetingOfOccupances(id)
    # print(str(result))
    meetingTimeFrames = []
    for i in range(len(result)):
      meetingTimeFrames.append({"uotimeframe":str(result[i][0]), "title":result[i][1]})
    return jsonify({'meetings': meetingTimeFrames})



  def userMeets(self, id):
    uid = id
    result = self.model.createdMeetings(uid)
    meetings = []
    for i in range(len(result["meets"])):
      meetings.append({"mid":result["meets"][i][0], "rid":result["meets"][i][1], "mtimeframe":str(result["meets"][i][3]), "mtype":result["meets"][i][4]})

    atnds = []

    for i in range(len(result["attendees"])):
      atnds.append({"uname":result["attendees"][i][0], "uid":result["attendees"][i][1],"mid":result["attendees"][i][2]})


    return jsonify({"createdMeetings":meetings, "attendees":atnds})


usersController = UsersController()