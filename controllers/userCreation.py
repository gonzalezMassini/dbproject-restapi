def user_creation(request, mysql):
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