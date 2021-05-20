#from .db.mongodb import Database
from flask import Flask, request
import sys
import time

d = mongodb.Database()


app = Flask(__name__)

@app.route('/')
def welcome():
    return 'Welcome'

@app.route('/blackboard')
def blackboard():
    return 'blackboard'

@app.route('/blackboard/create', methods=['POST'])      #create a new blackboard und save data in the mongoDB
def createBlackboard(pName, pValidity):
    #parameters
    name = request.args.post('name')
    validity = request.args.post('validity')

    ret = d.create_blackboard(name,validity,time.time())

    return 'Blackboard updated successfully',200

@app.route('/blackboard/display', methods=['GET'])      #update Data from the blackboard
def displayBlackboard():
    #parameters
    name = request.args.get('name')
    data = request.args.get('data')

    ret = d.display_blackboard(name,data,None, time.time())
    
    return 'DISPLAY_BLACKBOARD',200

@app.route('/blackboard/clear', methods=['GET'])        #clear content from the blackboard
def clearBlackboard():
    #parameters
    name = request.args.get('name')
    ret=d.clear_blackboard(name,time.time())
    return 'Blackboard cleared successfully',200

@app.route('/blackboard/read', methods=['GET'])         #read Data from the blackboard
def readBlackboard():
    #parameters
    name = request.args.get('name')
    return 'Blackboard read successfully',200

@app.route('/blackboard/getStatus', methods=['GET'])    #return the state from the blackboard
def getBlackboardStatus():
    #parameters
    name = request.args.get('name')

    ret = d.get_blackboard_status(name)

    return 'GET_BLACKBOARD_STATUS',200

@app.route('/blackboard/list', methods=['GET'])         #get all blackboardnames
def listBlackboard():
    ret = d.list_blackboards()
    return 'List_BLACKBOARD',200

@app.route('/blackboard/delete',methods=['DELETE'])     #delete current blacklist
def deleteBlackboard():
    #parameters
    name = request.args.get('name')
    ret = d.delete_blackboard(name)
    return 'DELETE_BLACKBOARD',200

@app.route('/blackboard/deleteAll', methods=['DELETE'])   #delete all blacklists
def deleteAllBlackboards():
    ret = d.delete_all_blackboards()
    return 'DELETE_ALL_BLACKBOARDS',200

app.run()