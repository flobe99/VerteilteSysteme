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

@app.route('/blackboard/create', methods=['GET'])      #create a new blackboard und save data in the mongoDB
def createBlackboard():
	#parameters
	name = request.args.get('name')
	validity = request.args.get('validity')
	validity_time = request.args.get('validityTime')
	try:
		tv = type(int(validity_time))
	except ValueError:
		return 'ERROR: (400) Invalid parameters', 400

	status_code = db.create_blackboard(name, validity, time.time())[1]
	if status_code == 200:
	    return 'Blackboard updated successfully', status_code
	else:
		return 'An error occurred', status_code

@app.route('/blackboard/display', methods=['GET'])      #update Data from the blackboard
def displayBlackboard():
	#parameters
	name = request.args.get('name')
	data = request.args.get('data')

	status_code = db.display_blackboard(name, data, None, time.time())[1]
    
	if status_code == 200:
	    return 'DISPLAY_BLACKBOARD', status_code
	else:
		return 'An error occurred', status_code

@app.route('/blackboard/clear', methods=['GET'])        #clear content from the blackboard
def clearBlackboard():
	#parameters
	name = request.args.get('name')
	status_code = db.clear_blackboard(name, time.time())[1]

	if status_code == 200:
	    return 'Blackboard cleared successfully', status_code
	else:
		return 'An error occurred', status_code

@app.route('/blackboard/read', methods=['GET'])         #read Data from the blackboard
def readBlackboard():
	#parameters
	name = request.args.get('name')
	result, status_code = db.read_blackboard(name)

	if result is None:
		return 'ERROR: (404) Blackboard does not exists', 404

	if 'content' not in result:
		return 'ERROR: (444) Blackboard is empty', 444

	if status_code == 200:
		return jsonify(result), status_code
	else:
		return 'An error occurred', status_code

@app.route('/blackboard/getStatus', methods=['GET'])    #return the state from the blackboard
def getBlackboardStatus():
	#parameters
	name = request.args.get('name')
	result, status_code = db.get_blackboard_status(name)

	if status_code == 200:
		return jsonify(result),status_code
	else:
		return 'An error occurred', status_code

@app.route('/blackboard/list', methods=['GET'])         #get all blackboardnames
def listBlackboard():
	results, status_code = db.list_blackboards()

	if status_code == 200:
	
		return jsonify(results), status_code
	else:
		return 'An error occurred', status_code

@app.route('/blackboard/delete',methods=['DELETE'])     #delete current blacklist
def deleteBlackboard():
	#parameters
	name = request.args.get('name')
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

app.run()