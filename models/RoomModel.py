# @author: Ralph Ulysse
from config.dbconfig import pg_config
from flask import jsonify, request
import psycopg2


class RoomModel():

    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s port=%s host='%s'" % (pg_config['dbname'], pg_config['user'], pg_config['password'], pg_config['dbport'], pg_config['host'])
        self.conn = psycopg2.connect(connection_url)

    # def readRooms(self, uid):
    def readRooms(self):
        cur = self.conn.cursor()
        # cur.execute('select urole from users where uid=%s', [uid])
        # role = cur.fetchone()
        # print(role[0])
        # if role[0] == 'staff':
        cur.execute("SELECT * FROM rooms;")
        result = cur.fetchall()
        cur.close()
        return result
        # else:
        #     cur.close()
        #     return "Must be staff member"

    def readRoom(self, id, uid):
        cur = self.conn.cursor()
        cur.execute('select urole from users where uid=%s', [uid])
        role = cur.fetchone()
        print(role[0])
        if role[0] == 'staff':
            result = cur.execute('SELECT * FROM rooms where rid=%s', [id])
            room = cur.fetchone()
            cur.close()
            return room
        else:
            cur.close()
            return "Must be staff member"

    def createRoom(self, rcapacity, rtype, rnumber, rbuilding):
        cur = self.conn.cursor()
        result = cur.execute("INSERT INTO rooms(rcapacity, rtype, rnumber, rbuilding) VALUES(%s,%s,%s,%s)",(rcapacity, rtype, rnumber, rbuilding))
        # commit to DB
        self.conn.commit()
        # close connection
        cur.close()
        return "room created"


    def deleteRoom(self, id):
        cur = self.conn.cursor()
        result = cur.execute('DELETE FROM rooms WHERE rid=%s', [id])
        self.conn.commit()
        cur.close()

        return jsonify({"msg": "room deleted"})

    def updateRoom(self, id, rcapacity, rtype, rnumber, rbuilding):
        cur = self.conn.cursor()
        cur.execute('UPDATE rooms SET rcapacity=%s, rtype=%s, rnumber=%s, rbuilding=%s WHERE rid=%s',
                    (rcapacity, rtype, rnumber, rbuilding, id))
        self.conn.commit()
        cur.close()

        return jsonify({'msg': 'room updated'})

    def readRoomOccupance(self, id, uid):
        cur= self.conn.cursor()
        cur.execute('select urole from users where uid=%s', [uid])
        role = cur.fetchone()
        print(role[0])
        if role[0] == 'staff':
            cur.execute('select roid, rotimeframe, rnumber from room_occupance natural inner join rooms where rid=%s',[id])
            queryResult= cur.fetchall()
            cur.close()
            return queryResult
        else:
            cur.close()
            return "Must be staff member"

    def createRoomOccupance(self, id, rotimeframe, uid):
        cur = self.conn.cursor()
        cur.execute('select urole from users where uid=%s', [uid])
        role = cur.fetchone()
        print(role[0])
        if role[0] == 'staff':
            result = cur.execute("INSERT INTO room_occupance(rid, rotimeframe) VALUES(%s,%s)",(id, rotimeframe))
            # commit to DB
            self.conn.commit()
            # close connection
            cur.close()
            return "Room Occupance has been created"
        else:
            cur.close()
            return "Must be staff member"

    def deleteRoomOccupance(self, id):
        cur = self.conn.cursor()
        result = cur.execute('DELETE FROM room_occupance WHERE roid=%s', [id])
        self.conn.commit()
        cur.close()

        return jsonify({"msg": "room occupance deleted"})

    def updateRoomOccupance(self, id, rid, rotimeframe):
        cur = self.conn.cursor()
        cur.execute('UPDATE room_occupance SET rid=%s, rotimeframe=%s, WHERE roid=%s',
                    (rid, rotimeframe, id))
        self.conn.commit()
        cur.close()

        return jsonify({'msg': 'room Occupance updated'})

    def roomFinder(self, timeframe):
        # @author: Jose Gonzalez Massini
        cur = self.conn.cursor()

        query = 'select * from rooms where rid not in (select rid from rooms natural inner join room_occupance where rotimeframe in (%s))'

        cur.execute(query, [timeframe])
        result = cur.fetchall()
        cur.close()
        return result 

    def mostBookedRoom(self):
        # @author: Jose Gonzalez Massini
        cur = self.conn.cursor()
        query = 'select rooms.rnumber, rooms_appointments from(select rooms.rnumber, rooms.rid, count(rooms.rid) as rooms_appointments from meetings inner join rooms on meetings.rid = rooms.rid group by  rooms.rid, rooms.rnumber) as foo inner join rooms on foo.rid = rooms.rid order by rooms_appointments desc limit 10;'

        cur.execute(query)
        result = cur.fetchall()
        cur.close()
        return result



roomModel = RoomModel()