from flask import Flask

app = Flask(__name__)

@app.route('/')
def welcome():
    return 'Welcome'

@app.route('/blackboard')
def welcome():
    return 'Welcome'

@app.route('/blackboard/create')
def createBlackboard():
    return 'Creating blackboard'

@app.route('/blackboard/display')
def displayBlackboard():
    return 'DISPLAY_BLACKBOARD'

@app.route('/blackboard/clear')
def clearBlackboard():
    return 'CLEAR_BLACKBOARD '

@app.route('/blackboard/read')
def clearBlackboard():
    return 'READ_BLACKBOARD '

@app.route('/blackboard/getStatus')
def clearBlackboard():
    return 'GET_BLACKBOARD_STATUS'

@app.route('/blackboard/list')
def clearBlackboard():
    return 'List_BLACKBOARD '

@app.route('/blackboard/delete')
def deleteBlackboard():
    return 'DELETE_BLACKBOARD '

@app.route('/blackboard/deleteAll')
def deleteAllBlackboards():
    return 'DELETE_ALL_BLACKBOARDS  '

app.run()