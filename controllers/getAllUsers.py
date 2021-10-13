def get_all_users(mysql):
  
  cur = mysql.connection.cursor()
  result = cur.execute('SELECT * FROM users')
  users = cur.fetchall()
  cur.close() 

  return {"users":users}

