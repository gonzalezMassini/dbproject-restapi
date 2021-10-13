from flask import Flask, request
from flask_mysqldb import MySQL
from controllers.userCreation import user_creation
from controllers.getAllUsers import get_all_users
from controllers.getSingleUser import get_single_user

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
  return user_creation(request, mysql)

# get all users
@app.route('/users', methods=['GET'])
def get_users():
  return get_all_users(mysql)

# user
@app.route('/user/<int:uid>', methods=['GET'])
def get_user(uid):
  if request.method == 'GET':
    return get_single_user(uid,mysql)

# user occupance
@app.route('/user/<int:uid>/user_occupance',methods=['POST'])
def user_occupance():
  return 'trying to be occupied'

# example route
@app.route('/', methods=['GET'])
def get():
  return {'msg':'hello word'}


# run server
if __name__ == '__main__':
  app.run(debug=True)