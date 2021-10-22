def create_user_occupance(id,mysql,request):
  uid = id
  uodate = request.json['uodate']
  uostarttime = request.json['uostarttime']
  uoendtime = request.json['uoendtime']

  cur = mysql.connection.cursor()
  cur.execute("INSERT INTO user_occupance(uid, uodate, uostarttime, uoendtime) VALUES(%s,%s,%s,%s)",(uid, uodate, uostarttime, uoendtime))
  mysql.connection.commit()
  cur.close()

  return {'uid':uid, 'uodate':uodate,'uostarttime':uostarttime,'uoendtime':uoendtime}