#from .db.mongodb import Database
from flask import Flask, request
import sys
import time
from database import Database
import json

db = Database()

app = Flask(__name__)

@app.route('/')
def welcome():
	return 'Welcome'

@app.route('/blackboard')
def blackboard():
	return 'blackboard'

@app.route('/blackboard/create', methods=['POST'])      #create a new blackboard und save data in the mongoDB
def createBlackboard():
	#parameters
	name = request.args.post('name')
	validity = request.args.post('validity')

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

	if status_code == 200:
		del result['_id']
		return json.dumps(result), status_code
	else:
		return 'An error occurred', status_code

@app.route('/blackboard/getStatus', methods=['GET'])    #return the state from the blackboard
def getBlackboardStatus():
	#parameters
	name = request.args.get('name')
	result, status_code = db.get_blackboard_status(name)

	if status_code == 200:
		del result['_id']
		return json.dumps(result), status_code
	else:
		return 'An error occurred', status_code

@app.route('/blackboard/list', methods=['GET'])         #get all blackboardnames
def listBlackboard():
	results, status_code = db.list_blackboards()
	tmp = { }
	count = 1
	for r in results:
		tmp[str(count)] = [ ]
		tmp[str(count)].append(r['name'])
		tmp[str(count)].append(r['text'])
		count += 1

	if status_code == 200:
	    return json.dumps(tmp), status_code
	else:
		return 'An error occurred', status_code

@app.route('/blackboard/delete',methods=['DELETE'])     #delete current blacklist
def deleteBlackboard():
	#parameters
	name = request.args.get('name')
	status_code = d.delete_blackboard(name)[1]

	if status_code == 200:
	    return 'DELETE_BLACKBOARD', status_code
	else:
		return 'An error occurred', status_code

@app.route('/blackboard/deleteAll', methods=['DELETE'])   #delete all blacklists
def deleteAllBlackboards():
	status_code = d.delete_all_blackboards()[1]

	if status_code == 200:
	    return 'DELETE_ALL_BLACKBOARDS', status_code
	else:
		return 'An error occurred', status_code

app.run()