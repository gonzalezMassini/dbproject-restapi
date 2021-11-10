from config.dbconfig import pg_config
from flask import jsonify, request
import psycopg2

class AttendeesModel():

  def __init__(self):
    connection_url = "dbname=%s user=%s password=%s port=%s host=%s"%(pg_config['dbname'], pg_config['user'],pg_config['password'],pg_config['dbport'], pg_config['host'])
    self.conn = psycopg2.connect(connection_url)

  def readAttendees(self):
    cur = self.conn.cursor()
    cur.execute("SELECT * FROM attendees;")
    result = cur.fetchall() 
    cur.close()
    return result
    

  def readAttendee(self,id):
    cur = self.conn.cursor()
    result = cur.execute('SELECT * FROM attendees where aid=%s',[id])
    attendee = cur.fetchone()
    cur.close()
    return attendee


  def createAttendee(self,uid,mid):
    # create cursor
    cur = self.conn.cursor()

    result = cur.execute("INSERT INTO attendees(uid, mid) VALUES(%s,%s) returning aid",(uid, mid))
  
    id_of_new_row = cur.fetchone()[0]
    resultCreatedAttendee = cur.execute("select * from attendees where aid=%s",[id_of_new_row])
    createdAttendee = cur.fetchone()
    # commit to DB
    self.conn.commit()
    # close connection
    cur.close()
    # return jsonify(createdAttendee)
    return createdAttendee


  def deleteAttendee(self, id):
    cur = self.conn.cursor()
    result = cur.execute('DELETE FROM attendees WHERE aid=%s',[id])
    self.conn.commit()
    cur.close() 

    return jsonify({"msg":"attendee deleted"})


  def updateAttendee(self, id, uid, mid):
    cur = self.conn.cursor()
    cur.execute('UPDATE attendees SET uid=%s, mid=%s WHERE aid=%s',(uid, mid, id))
    self.conn.commit()
    cur.close()

    return jsonify({'msg':'attendee updated'})


attendeesModel = AttendeesModel()