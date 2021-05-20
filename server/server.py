from flask import Flask

app = Flask(__name__)

@app.route('/')
def welcome():
    return 'Welcome'

@app.route('/createBlackboard')
def createBlackboard():
    return 'Creating blackboard'

@app.route('/displayBlackboard')
def displayBlackboard():
    return 'DISPLAY_BLACKBOARD '

@app.route('/clearBlackboard')
def clearBlackboard():
    return 'CLEAR_BLACKBOARD '

@app.route('/deleteBlackboard')
def deleteBlackboard():
    return 'DELETE_BLACKBOARD '

@app.route('/deleteAllBlackboards')
def deleteAllBlackboards():
    return 'DELETE_ALL_BLACKBOARDS  '

app.run()