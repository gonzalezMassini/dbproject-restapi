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
    pass

meetingsController = MeetingsController()
      