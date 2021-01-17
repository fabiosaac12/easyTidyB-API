# IMPORTS
import os
from flask import Flask, request
from flask_cors import CORS


# SETTINGS
app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content_Type'
app.secret_key = os.environ["SECRET_KEY"]
app.port = 9000


# ROUTES
from routes import *

@app.route('/<section>/<userID>', methods=['GET'])
def selectElementsSC(section, userID):
    return selectElements(section, userID)

@app.route('/graph/<section>/<userID>', methods=['GET'])
def selectGraphSC(section, userID):
    return selectGraph(section, userID)

@app.route('/info/<section>/<ID>', methods=['GET'])
def selectInfoSC(section, ID):
    return selectInfo(section, ID)

@app.route('/<section>/grouped/<userID>', methods=['GET'])
def selectGroupedElementsSC(section, userID):
    return selectGroupedElements(section, userID)

@app.route('/<select>/select/<userID>', methods=['GET'])
def selectToSelectSC(select, userID):
    return selectToSelect(select, userID)

@app.route('/<section>/equalelements/<userID>', methods=['POST'])
def selectEqualElementsSC(section, userID):
    data = request.get_json(silent=True)
    return selectEqualElements(section, userID, data)

@app.route('/<section>/<userID>', methods=['POST'])
def insertElementsSC(section, userID):
    data = request.get_json(silent=True)
    return insertElements(section, userID, data)

@app.route('/<section>', methods=['DELETE'])
def deleteElementsSC(section):
    data = tuple(request.get_json(silent=True))
    return deleteElements(section, data)

@app.route('/<section>', methods=['PUT'])
def updateElementSC(section):
    data = request.get_json(silent=True)
    return updateElement(section, data)

@app.route('/login', methods=['POST'])
def loginSC():
    data = request.get_json(silent=True)
    return login(data)

@app.route('/signup', methods=['POST'])
def signupSC():
    data = request.get_json(silent=True)
    return signup(data)


# STARTING APP
if __name__ == "__main__":
    if os.environ["FLASK_ENV"] == 'production':
        from waitress import serve
        serve(app=app, host="0.0.0.0", port=app.port)
    else:
        app.run(host="localhost", port=app.port, debug=True)
