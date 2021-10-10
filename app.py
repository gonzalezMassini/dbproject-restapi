from flask import Flask, request, jsonify
from flask_mysqldb import MySQL

# init app
app = Flask(__name__)

# config mysql
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'flask'
app.config['MYSQL_PASSWORD'] = 'none'
app.config['MYSQL_DB'] = 'dbproject'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# init MySQL
mysql = MySQL(app)


# create user
@app.route('/create_user', methods=['POST'])
def create_user():
  uemail = request.json['uemail']
  uname = request.json['uname']
  upassword = request.json['upassword']
  urole = request.json['urole']

  # create cursor
  cur = mysql.connection.cursor()

  # execute
  cur.execute("INSERT INTO users(uemail, uname, upassword, urole) VALUES(%s,%s,%s,%s)",(uemail, uname, upassword, urole))

  # commit to DB
  mysql.connection.commit()

  # close connection
  cur.close()
  
  return {'uemail':uemail, 'uname':uname, 'upassword':upassword, 'urole':urole}


@app.route('/', methods=['GET'])
def get():
  return {'msg':'hello word'}


# run server
if __name__ == '__main__':
  app.run(debug=True)