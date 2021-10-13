def get_single_user(uid,mysql):
  cur = mysql.connection.cursor()
  result = cur.execute('SELECT * FROM users')
  users = cur.fetchall()
  cur.close()
  
  for user in users:
    if user['uid'] == uid:
      return user
  return 'user not found'
