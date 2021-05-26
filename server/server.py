#!/usr/bin/env python3
#from .db.mongodb import Database
from flask import Flask, request, jsonify
import sys
import time
from database import Database
import json

db = Database()

app = Flask(__name__)

@app.route('/')
def welcome():
	return 'Welcome'

@app.route('/blackboard' , methods=['GET'])
def blackboard():
	return 'blackboard'

@app.route('/blackboard/create', methods=['POST'])      #create a new blackboard und save data in the mongoDB
def createBlackboard():
	#parameters
	name = request.args.get('name')
	validityTime = request.args.get('validityTime')
	if name is None or validityTime is None or not validityTime.isnumeric():
		return "", 400

	status_code = db.create_blackboard(name, int(validityTime))[1]

	if status_code == 200:
	    return 'Blackboard updated successfully', status_code
	else:
		return 'An error occurred', status_code

@app.route('/blackboard/display', methods=['GET'])      #update Data from the blackboard
def displayBlackboard():
	#parameters
	name = request.args.get('name')
	data = request.args.get('data')
	if name is None or data is None:
		return "", 400

	status_code = db.display_blackboard(name, data)[1]
    
	if status_code == 200:
	    return 'DISPLAY_BLACKBOARD', status_code
	else:
		return 'An error occurred', status_code

@app.route('/blackboard/clear', methods=['GET'])        #clear content from the blackboard
def clearBlackboard():
	#parameters
	name = request.args.get('name')
	if name is None:
		return "", 400

	status_code = db.clear_blackboard(name)[1]

	if status_code == 200:
	    return 'Blackboard cleared successfully', status_code
	else:
		return 'An error occurred', status_code

@app.route('/blackboard/read', methods=['GET'])         #read Data from the blackboard
def readBlackboard():
	#parameters
	name = request.args.get('name')
	if name is None:
		return "", 400

	result, status_code = db.read_blackboard(name)

	# Blackboard not foudn
	if result is None:
		return "", 404

	# Blackboard is empty
	if result["content"] == "":
		return "", 444

	result = { "validity": result["validity"], "content": result["content"] }

	if status_code == 200:
		return jsonify(result), status_code
	else:
		return 'An error occurred', status_code

@app.route('/blackboard/getStatus', methods=['GET'])    #return the state from the blackboard
def getBlackboardStatus():
	#parameters
	name = request.args.get('name')
	if name is None:
		return "", 400

	result, status_code = db.get_blackboard_status(name)

	# Blackboard not found
	if result is None:
		return "", 404

	result = { "timestamp": result["timestamp"].isoformat(), "validity": result["validity"], "validityTime": result["validityTime"], "empty": result["content"] == "" }

	if status_code == 200:
		return jsonify(result),status_code
	else:
		return 'An error occurred', status_code

@app.route('/blackboard/list', methods=['GET'])         #get all blackboardnames
def listBlackboard():
	results, status_code = db.list_blackboards()

	blackboardsList = []
	for result in results:
		blackboardsList.append( { "name": result['name'] } )

	if status_code == 200:
		return jsonify(blackboardsList), status_code
	else:
		return 'An error occurred', status_code

@app.route('/blackboard/delete',methods=['DELETE'])     #delete current blacklist
def deleteBlackboard():
	#parameters
	name = request.args.get('name')
	if name is None:
		return "", 400

	status_code = db.delete_blackboard(name)[1]

	if status_code == 200:
	    return 'DELETE_BLACKBOARD', status_code
	else:
		return 'An error occurred', status_code

@app.route('/blackboard/deleteAll', methods=['DELETE'])   #delete all blacklists
def deleteAllBlackboards():
	status_code = db.delete_all_blackboards()[1]

	if status_code == 200:
	    return 'DELETE_ALL_BLACKBOARDS', status_code
	else:
		return 'An error occurred', status_code

if __name__ == '__main__':
	app.run()