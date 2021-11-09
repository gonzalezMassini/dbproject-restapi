from config.dbconfig import pg_config
from flask import jsonify, request
import psycopg2
class MeetingsModel():

  def __init__(self):
    connection_url = "dbname=%s user=%s password=%s port=%s host='%s'"%(pg_config['dbname'], pg_config['user'],pg_config['password'],pg_config['dbport'],pg_config['host'])
    self.conn = psycopg2.connect(connection_url)

  def readMeetings(self):
    cur = self.conn.cursor()
    cur.execute("SELECT * FROM meetings;")
    result = cur.fetchall() 
    cur.close()
    return result
    

  def readMeeting(self,id):
    cur = self.conn.cursor()
    result = cur.execute('SELECT * FROM meetings where uid=%s',[id])
    meeting = cur.fetchone()
    cur.close()
    return meeting

  def createMeeting(self, mtype, mtimeframe, rid, attendees, uid):
    # create cursor
    cur = self.conn.cursor()

    resultCreatedMeeting = cur.execute("INSERT INTO meetings (rid, uid, mtimeframe, mtype) VALUES (%s,%s,%s,%s) returning mid",(rid, uid, mtimeframe, mtype))
    id_of_new_row = cur.fetchone()[0]
    # print(id_of_new_row, attendees)
    resultCreatorOccupance = cur.execute("INSERT INTO user_occupance (uid, uotimeframe) VALUES (%s,%s)",(uid, mtimeframe))
    insertCreatorAttendee = cur.execute("INSERT INTO attendees (uid, mid) VALUES (%s,%s)",(uid, id_of_new_row))
    roomOccuance = cur.execute("INSERT INTO room_occupance (rid, rotimeframe) VALUES (%s,%s)",(rid, mtimeframe))

    for attende in attendees:
      attendeeUid = attende['uid']
      cur.execute("INSERT INTO attendees (uid, mid) VALUES (%s,%s)", (attendeeUid, id_of_new_row))
      cur.execute("INSERT INTO user_occupance (uid, uotimeframe) VALUES (%s,%s)",(attendeeUid, mtimeframe))

    # print(mtimeframe)
    # commit to DB
    self.conn.commit()
    # close connection
    cur.close()
    # return jsonify(createdUser)
    return 'new meeting'


  def deleteMeeting(self, id):
    cur = self.conn.cursor()
    result = cur.execute('DELETE FROM meeting WHERE uid=%s',[id])
    self.conn.commit()
    cur.close() 

    return jsonify({"msg":"meeting deleted"})


  def updateUser(self):
    cur = self.conn.cursor()
    # cur.execute('UPDATE users SET uemail=%s, uname=%s, upassword=%s, urole=%s WHERE uid=%s',(uemail, uname, upassword, urole, id))
    self.conn.commit()
    cur.close()

    return jsonify({'msg':'meeting updated'})

    
  


meetingsModel = MeetingsModel()