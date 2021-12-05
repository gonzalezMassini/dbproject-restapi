# @author: Ralph Ulysse 
from flask import jsonify, request
from models.RoomModel import roomModel


class RoomController():

    def __init__(self):
        self.model = roomModel

    # read rooms
    # def showRooms(self, request):
    def showRooms(self):
        result = []
        # uid = request.json['uid']
        # rooms = self.model.readRooms(uid)
        rooms = self.model.readRooms()
        if type(rooms) == str:
            return jsonify({"msg":rooms})
            
        for i in range(len(rooms)):
            result.append({
                "rid": rooms[i][0],
                "rcapacity": rooms[i][1],
                "rtype": rooms[i][2],
                "rnumber": rooms[i][3],
                "rbuilding": rooms[i][4]
            })
            

        return jsonify({"rooms": result})

    # read room
    def showRoom(self, id, request):
        uid = request.json['uid']
        room = self.model.readRoom(id, uid)
        if type(room) == str:
            return jsonify({"msg":room})

        result = {"rid": room[0], "rcapacity": room[1], "rtype": room[2], "rnumber": room[3], "rbuilding": room[4]}

        return jsonify(result)

    # create room
    def insertRoom(self, request):
        rcapacity = request.json['rcapacity']
        rtype = request.json['rtype']
        rnumber = request.json['rnumber']
        rbuilding = request.json['rbuilding']

        createdRoom = self.model.createRoom(rcapacity, rtype, rnumber, rbuilding)
        # result = {"rid": createdRoom[0], "rcapacity": createdRoom[1], "rtype": createdRoom[2], "rnumber": createdRoom[3],"rbuilding": createdRoom[4]}

        # return jsonify(result)
        return jsonify({"message":createdRoom})

    # delete room
    def removeRoom(self, id):
        return self.model.deleteRoom(id)

    # update room
    def editRoom(self, id, request):
        rcapacity = request.json['rcapacity']
        

        return self.model.updateRoom(id, rcapacity)

    def showRoomOccupance(self,id, request):
        uid = request.json['uid']
        occupances=[]
        result = self.model.readRoomOccupance(id, uid)
        if type(result) == str:
            return jsonify({"msg": result})
        for i in range(len(result)):
            occupances.append({
                "roid":result[i][0],
                "rotimeframe":str(result[i][1])
                }
            )
        return jsonify(occupances)

    def insertRoomOccupance(self,id, request):
        rotimeframe = request.json['rotimeframe']
        uid = request.json['uid']

        createdRoomOccupance = self.model.createRoomOccupance(id, rotimeframe, uid)

        return jsonify({"msg":createdRoomOccupance}) 

    def removeRoomOccupance(self, id):
        return self.model.deleteRoomOccupance(id)

        # update room Occupance

    def editRoomOccupance(self, id, request):
        rid = request.json['rid']
        rotimeframe = request.json['rotimeframe']

        return self.model.updateRoom(id, rid, rotimeframe)


    def findAvailableRoom(self, request):
        # @author: Jose Gonzalez Massini
        timeframe = request.json["timeframe"]
        result = self.model.roomFinder(timeframe)

        availableRooms = []

        for i in range(len(result)):
            availableRooms.append({
                "rcapacity": result[i][1],
                "rtype": result[i][2],
                "rnumber": result[i][3],
                "rbuilding": result[i][4]
            })

        return jsonify({"available rooms": availableRooms})

    def findAvailableRoomRoute(self, timeframe):
        timeframe = timeframe
        result = self.model.roomFinder(timeframe)

        availableRooms = []

        for i in range(len(result)):
            availableRooms.append({
                "rid": result[i][0],
                "rcapacity": result[i][1],
                "rtype": result[i][2],
                "rnumber": result[i][3],
                "rbuilding": result[i][4]
            })

        return jsonify({"available rooms": availableRooms})



    def mostUsedRoom(self):
        # @author: Jose Gonzalez Massini
        result = self.model.mostBookedRoom()
        mostUsedRooms = []

        for i in range(len(result)):
            mostUsedRooms.append({
                "rnumber": result[i][0],
                "room_appointments": result[i][1]
            })

        return jsonify({"most used rooms": mostUsedRooms})

roomController = RoomController()