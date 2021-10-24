from config.dbconfig import pg_config
from flask import jsonify, request
import psycopg2
class UsersModel():

  def __init__(self):
    connection_url = "dbname=%s user=%s password=%s port=%s host='localhost'"%(pg_config['dbname'], pg_config['user'],pg_config['password'],pg_config['dbport'])
    self.conn = psycopg2.connect(connection_url)

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
    # return jsonify(createdUser)
    return createdUser


  def deleteUser(self, id):
    cur = self.conn.cursor()
    result = cur.execute('DELETE FROM users WHERE uid=%s',[id])
    self.conn.commit()
    cur.close() 

    return jsonify({"msg":"user deleted"})


  def updateUser(self, id, uemail, uname, upassword, urole):
    cur = self.conn.cursor()
    cur.execute('UPDATE users SET uemail=%s, uname=%s, upassword=%s, urole=%s WHERE uid=%s',(uemail, uname, upassword, urole, id))
    self.conn.commit()
    cur.close()

    return jsonify({'msg':'user updated'})
    
  


usersModel = UsersModel()