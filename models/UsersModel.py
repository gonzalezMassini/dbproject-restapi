# @author: Jose Gonzalez Massini
from config.dbconfig import pg_config
from flask import jsonify, request
import psycopg2
class UsersModel():

  def __init__(self):
    connection_url = "dbname=%s user=%s password=%s port=%s host='%s'"%(pg_config['dbname'], pg_config['user'],pg_config['password'],pg_config['dbport'], pg_config['host'])
    self.conn = psycopg2.connect(connection_url)


  def signin(self, uemail, upassword):
    cur = self.conn.cursor()
    query = "select * from users where uemail=%s and upassword=%s;"
    cur.execute(query, (uemail, upassword))
    loginResult = cur.fetchone()
    # print(loginResult[0])
    # print(type(loginResult[0]))
    try:
      if loginResult:
        # print('login succesful')
        cur.close()
        return {"uid":loginResult[0], "urole":loginResult[3]}
      else:
        # print('worng credentials')
        cur.close()
        return 'worng credentials'
    except Exception as e:
      cur.close()
      print('DB error')



  def readUsers(self):
    cur = self.conn.cursor()
    cur.execute("SELECT * FROM users;")
    result = cur.fetchall() 
    cur.close()
    return result
    

  def readUser(self,id):
    cur = self.conn.cursor()
    result = cur.execute('SELECT * FROM users where uid=%s',[id])
    user = cur.fetchone()
    cur.close()
    return user

  def createUser(self,uemail,uname,upassword,urole):
    # create cursor
    cur = self.conn.cursor()

    result = cur.execute("INSERT INTO users(uemail, uname, upassword, urole) VALUES(%s,%s,%s,%s) returning uid",(uemail, uname, upassword, urole))
    
    id_of_new_row = cur.fetchone()[0]
    resultCreatedUser = cur.execute("select * from users where uid=%s",[id_of_new_row])
    createdUser = cur.fetchone()
    # commit to DB
    self.conn.commit()
    # close connection
    cur.close()
    return createdUser


  def deleteUser(self, id):
    cur = self.conn.cursor()
    result = cur.execute('DELETE FROM users WHERE uid=%s',[id])
    self.conn.commit()
    cur.close() 

    return jsonify({"msg":"user deleted"})

  def updateUser(self, id, uemail, uname, upassword):
    cur = self.conn.cursor()
    cur.execute('UPDATE users SET uemail=%s, uname=%s, upassword=%s WHERE uid=%s',(uemail, uname, upassword, id))
    self.conn.commit()
    cur.close()

    return jsonify({'msg':'user updated'})

  def readUserOccupance(self, id):
    cur = self.conn.cursor()
    cur.execute('select uname, uotimeframe, title from user_occupance natural inner join users where uid=%s',[id])
    queryResult = cur.fetchall()
    result = cur.fetchall()
    cur.close()
    return queryResult

  def createUserOccupance(self, uid, uotimeframe, title):
    cur = self.conn.cursor()
    cur.execute("INSERT INTO user_occupance(uid, uotimeframe, title) VALUES(%s,%s,%s)",(uid, uotimeframe, title))
    self.conn.commit()
    cur.close()
    return jsonify({"message": "user occupance created"})

  def appointedByWho(self, timeframe):
    cur = self.conn.cursor()
    query = 'select uname, rnumber from users natural inner join meetings natural inner join rooms where mtimeframe in (%s)'
    cur.execute(query, [timeframe])
    result = cur.fetchall()
    cur.close()
    return result

  def usedRoomMost(self, id):
    cur = self.conn.cursor()

    query = "select rooms.rnumber, rooms_appointments from(select rooms.rnumber, rooms.rid, count(rooms.rid) as rooms_appointments from meetings inner join rooms on meetings.rid = rooms.rid inner join attendees on meetings.mid = attendees.mid where attendees.uid=%s group by  rooms.rid, rooms.rnumber order by rooms_appointments desc) as foo natural inner join rooms where rooms_appointments = (select max(rooms_appointments)from (select rooms.rid, count(rooms.rid) as rooms_appointments from meetings inner join rooms on meetings.rid = rooms.rid inner join attendees on meetings.mid = attendees.mid where attendees.uid=%s group by  rooms.rid, rooms.rnumber order by rooms_appointments desc) as food);"

    cur.execute(query, (id, id))
    result = cur.fetchone()
    print(result)
    cur.close()
    return result

  def userMostBooked(self):
    cur = self.conn.cursor()
    query = 'select uname, user_appointments from (select uid, count(uid) as user_appointments from attendees group by uid) as foo inner join users on foo.uid = users.uid order by user_appointments desc limit 10'
    cur.execute(query)
    result = cur.fetchall()
    cur.close()
    return result

  def mostBooked(self, id):
    cur = self.conn.cursor()
    query = 'select name, max(joins) as maxJoins from (select name ,count(mid) as joins from (select attendees.uid, meetings.mid, users.uname as name from (meetings inner join attendees on meetings.mid = attendees.mid inner join users on attendees.uid = users.uid)where meetings.mid in (select meetings.mid from meetings inner join attendees on meetings.mid = attendees.mid where attendees.uid = %s))as foo where uid != %s group by foo.uid, name )as food group by name limit 1;'
    cur.execute(query, (id, id))
    result = cur.fetchall()
    print(result)
    cur.close()
    return result


  def meetingOfOccupances(self, id):
    cur = self.conn.cursor()
    query = "select mtimeframe,mtype from attendees inner join meetings on meetings.mid = attendees.mid where attendees.uid = %s;"
    cur.execute(query, [id])
    result = cur.fetchall()
    cur.close()
    return result

  def createdMeetings(self, uid):
    cur = self.conn.cursor()
    query = "select * from meetings where uid = %s;"
    
    cur.execute(query, [uid])
    result = cur.fetchall()

    attendeesQuery = "select users.uname,  users.uid, meetings.mid from meetings inner join attendees on meetings.mid = attendees.mid inner join users on attendees.uid = users.uid where meetings.uid = %s and attendees.uid != %s;"
    cur.execute(attendeesQuery, (uid, uid))
    attendees = cur.fetchall()


    cur.close()
    return {"meets":result, "attendees":attendees}



  def occ(self):
    cur = self.conn.cursor()
    query = "select * from user_occupance natural inner join users;"
    
    cur.execute(query)
    result = cur.fetchall()
    cur.close()
    return result


usersModel = UsersModel()
