from flask import jsonify, request
from models.AttendeesModel import attendeesModel

class AttendeesController():

  def __init__(self):
    self.model = attendeesModel


  # read attendees
  def showAttendees(self):
    result = []
    attendees = self.model.readAttendees()
    
    for i in range(len(attendees)):
      result.append({
        "aid":attendees[i][0],
        "uid":attendees[i][1],
        "mid":attendees[i][2]
      })

    return jsonify({"attendees":result})


  # read attendee 
  def showAttendee(self,id):
    attendee = self.model.readAttendee(id)

    result = {"uid":attendee[0], "uid":attendee[1], "mid":attendee[2]}

    return jsonify(result)


# create attendee
  def insertAttendee(self, request):
    uid = request.json['uid']
    mid = request.json['mid']

    createdAttendee = self.model.createAttendee(uid,mid) 
    result = {"aid":createdAttendee[0], "uid":createdAttendee[1],"mid":createdAttendee[2]}

    return jsonify(result)
    

# delete attendee
  def removeAttendee(self,id):
    return self.model.deleteAttendee(id)

# update attendee 
  def editAttendee(self,id,request):
    uid = request.json['uid']
    mid = request.json['mid']

    return self.model.updateAttendee(id, uid, mid)


attendeesController = AttendeesController()