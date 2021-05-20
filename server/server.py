#from .db.mongodb import Database
from flask import Flask, request
import sys
import time
from database import Database

d = Database()

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

	ret = Database.create_blackboard(name,validity,time.time())

	if ret == 200:
	    return 'Blackboard updated successfully', ret
	else:
		return 'An error occurred', ret

@app.route('/blackboard/display', methods=['GET'])      #update Data from the blackboard
def displayBlackboard():
	#parameters
	name = request.args.get('name')
	data = request.args.get('data')

	ret = Database.display_blackboard(name,data,None, time.time())
    
	if ret == 200:
	    return 'DISPLAY_BLACKBOARD', ret
	else:
		return 'An error occurred', ret

@app.route('/blackboard/clear', methods=['GET'])        #clear content from the blackboard
def clearBlackboard():
	#parameters
	name = request.args.get('name')
	ret=Database.clear_blackboard(name,time.time())

	if ret == 200:
	    return 'Blackboard cleared successfully', ret
	else:
		return 'An error occurred', ret

@app.route('/blackboard/read', methods=['GET'])         #read Data from the blackboard
def readBlackboard():
	#parameters
	name = request.args.get('name')
	ret = Database.read_blackboard(name)

	if ret == 200:
	    return 'Blackboard read successfully', ret
	else:
		return 'An error occurred', ret

@app.route('/blackboard/getStatus', methods=['GET'])    #return the state from the blackboard
def getBlackboardStatus():
	#parameters
	name = request.args.get('name')

	ret = d.get_blackboard_status(name)

	if ret == 200:
	    return 'GET_BLACKBOARD_STATUS', ret
	else:
		return 'An error occurred', ret

@app.route('/blackboard/list', methods=['GET'])         #get all blackboardnames
def listBlackboard():
	ret = d.list_blackboards()

	if ret == 200:
	    return 'List_BLACKBOARD', ret
	else:
		return 'An error occurred', ret

@app.route('/blackboard/delete',methods=['DELETE'])     #delete current blacklist
def deleteBlackboard():
	#parameters
	name = request.args.get('name')
	ret = d.delete_blackboard(name)

	if ret == 200:
	    return 'DELETE_BLACKBOARD', ret
	else:
		return 'An error occurred', ret

@app.route('/blackboard/deleteAll', methods=['DELETE'])   #delete all blacklists
def deleteAllBlackboards():
	ret = d.delete_all_blackboards()

	if ret == 200:
	    return 'DELETE_ALL_BLACKBOARDS', ret
	else:
		return 'An error occurred', ret

app.run()