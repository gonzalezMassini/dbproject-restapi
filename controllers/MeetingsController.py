# @author: Jose Gonzalez Massini
from flask import jsonify, request
from models.MeetingsModel import meetingsModel

class MeetingsController():

  def __init__(self):
    self.model = meetingsModel


  # read meetings
  def showMeetings(self):
    meetings=[]
    result = self.model.readMeetings()
    for i in range(len(result)):
      meetings.append({
        "mid":result[i][0],
        "rid":result[i][1],
        "uid":result[i][2],
        "mtimeframe":str(result[i][3]),
        "mtype":result[i][4]
      })
    return jsonify({"meetings":meetings})


  # read meeting 
  def showMeeting(self,id):
    result = self.model.readMeeting(id)
    createdMeeting = {
        "mid":result[0],
        "rid":result[1],
        "uid":result[2],
        "mtimeframe":str(result[3]),
        "mtype":result[4]
      }

    return jsonify({"meeting":createdMeeting})



  # create meeting
  def insertMeeting(self, request):
    mtype = request.json['mtype']
    mtimeframe = request.json['mtimeframe']
    rid = request.json['rid']
    attendees = request.json['attendees']
    uid = request.json['uid']

    createdMeeting = self.model.createMeeting(mtype, mtimeframe, rid, attendees, uid)
    return createdMeeting


# delete meeting
  def removeMeeting(self,id):
    return self.model.deleteMeeting(id)



  # update meeting 
  def editMeeting(self,id,request):
    mid = id
    mtype = request.json['mtype']
    mtimeframe = request.json['mtimeframe']
    rid = request.json['rid']
    uid = request.json['uid']

    return self.model.updateMeeting(mid, mtype, mtimeframe, rid, attendees, uid)

  def busiestHours(self):
    result = self.model.busiest()
    # print(result)
    # print(result['lowerBound'][1])
    if(result['lowerBound'][1] > result['upperBound'][1]):
      return jsonify({"busiest hour": result['lowerBound'][0]})

    elif(result['lowerBound'][1] < result['upperBound'][1]):
      return jsonify({"busiest hour": result['upperBound'][0]})

    else:
      return jsonify({"busiest hour": str(result['lowerBound'][0]) + ' and ' + str(result["upperBound"][0])})

  

  def timeAvailable(self, id):
    result = self.model.availableTimeForEveryOne(id)

    # return jsonify({"available time for everyone in meeting with id:"+str(id): str(result[0])})
    return result

meetingsController = MeetingsController()
      