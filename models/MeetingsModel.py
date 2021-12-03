# @author: Jose Gonzalez Massini
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
    result = cur.execute('SELECT * FROM meetings where mid=%s',[id])
    meeting = cur.fetchone()
    cur.close()
    return meeting

  def createMeeting(self, mtype, mtimeframe, rid, attendees, uid):
    # create cursor
    cur = self.conn.cursor()

    resultCreatedMeeting = cur.execute("INSERT INTO meetings (rid, uid, mtimeframe, mtype) VALUES (%s,%s,%s,%s) returning mid",(rid, uid, mtimeframe, mtype))
    id_of_new_row = cur.fetchone()[0]
    # print(id_of_new_row, attendees)
    resultCreatorOccupance = cur.execute("INSERT INTO user_occupance (uid, uotimeframe, title) VALUES (%s,%s)",(uid, mtimeframe, mtype))
    insertCreatorAttendee = cur.execute("INSERT INTO attendees (uid, mid) VALUES (%s,%s)",(uid, id_of_new_row))
    roomOccuance = cur.execute("INSERT INTO room_occupance (rid, rotimeframe) VALUES (%s,%s)",(rid, mtimeframe))

    for attende in attendees:
      attendeeUid = attende['uid']
      cur.execute("INSERT INTO attendees (uid, mid) VALUES (%s,%s)", (attendeeUid, id_of_new_row))
      cur.execute("INSERT INTO user_occupance (uid, uotimeframe, title) VALUES (%s,%s)",(attendeeUid, mtimeframe, mtype))

    # print(mtimeframe)
    # commit to DB
    self.conn.commit()
    # close connection
    cur.close()
    # return jsonify(createdUser)
    return 'new meeting'


  def deleteMeeting(self, id):
    cur = self.conn.cursor()
    result = cur.execute('DELETE FROM meetings WHERE mid=%s',[id])
    self.conn.commit()
    cur.close() 

    return jsonify({"msg":"meeting deleted"})


  def updateMeeting(self, mid, mtype, mtimeframe, rid, uid):
    cur = self.conn.cursor()
    cur.execute('UPDATE meetings SET mtype=%s, mtimeframe=%s, rid=%s, uid=%s WHERE mid=%s',(mtype, mtimeframe, rid, attendees, uid, mid))
    self.conn.commit()
    cur.close()

    return jsonify({'msg':'meeting updated'})

  def busiest(self):
    cur = self.conn.cursor()
    lowerQuery = "select lower_hour, lowerCount from(select lower_hour, count(lower_hour) as lowerCount from(select split_part(lower_bound, ' ',2) as lower_hour from (select cast(lower(mtimeframe) as varchar) as lower_bound from meetings) as noob) as rick group by lower_hour) as food order by lowerCount desc limit 5;"

    upperQuery = "select upper_hour, upperCount from(select upper_hour, count(upper_hour) as upperCount from(select split_part(upper_bound, ' ',2) as upper_hour from (select cast(upper(mtimeframe) as varchar) as upper_bound from meetings) as noob) as rick group by upper_hour) as food order by upperCount desc limit 5;"

    cur.execute(lowerQuery)
    lowerResult = cur.fetchall()

    cur.execute(upperQuery)
    upperResult = cur.fetchall()

    cur.close()
    # print(lowerResult, upperResult)
    return {"lowerBound" : lowerResult,"upperBound": upperResult}


  def availableTimeForEveryOne(self, id):
    # query = 'select get_available_timeframe_for_everyone(%s);'
    # cur = self.conn.cursor()
    # cur.execute(query, [id])
    # result = cur.fetchone()
    # cur.close()
    # return result
    return 'not yet'


meetingsModel = MeetingsModel()