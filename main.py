# IMPORTS
import os
from flask import Flask, request
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token, get_jwt_identity, get_raw_jwt
)

# SETTINGS
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": os.environ["CLIENT_DOMAIN"]}})
app.config['CORS_HEADERS'] = 'Content_Type'
app.secret_key = os.environ["SECRET_KEY"]
app.port = 9000

app.config['JWT_SECRET_KEY'] = os.environ["SECRET_KEY"]
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
jwt = JWTManager(app)

blacklist = set()

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in blacklist


# ROUTES
from routes import *

@app.route('/login', methods = ['POST'])
def loginSC():
    data = {
        "username": request.authorization['username'],
        "password": request.authorization['password']
    }
    print("\n\n\n\n")
    result = login(data)
    print(result)
    try:
        if result['userID']:
            accessToken = create_access_token(identity = result['userID'])
            return jsonify(accessToken = accessToken)
    except KeyError:
        return jsonify(message='Database Error')
    return jsonify( result )

@app.route('/signup', methods = ['POST'])
def signupSC():
    data = {
        "username": request.authorization['username'],
        "password": request.authorization['password']
    }
    result = signup(data)
    try:
        if result['id']:
            accessToken = create_access_token(identity = result['id'])
            return jsonify(accessToken = accessToken)
    except KeyError:
        return jsonify(message='Database Error')
    return jsonify( result )

@app.route('/logout', methods=['DELETE'])
@jwt_required
def logout():
    jti = get_raw_jwt()['jti']
    blacklist.add(jti)
    return jsonify({"msg": "Successfully logged out"})


@app.route('/<section>', methods = ['GET'])
@jwt_required
def selectElementsSC(section):
    userID = get_jwt_identity()
    return selectElements(section, userID)

@app.route('/<section>', methods = ['POST'])
@jwt_required
def insertElementsSC(section):
    userID = get_jwt_identity()
    data = request.get_json(silent = True)
    return insertElements(section, userID, data)

@app.route('/<section>', methods = ['DELETE'])
@jwt_required
def deleteElementsSC(section):
    data = tuple(request.get_json(silent = True))
    return deleteElements(section, data)

@app.route('/<section>', methods = ['PUT'])
@jwt_required
def updateElementSC(section):
    data = request.get_json(silent = True)
    return updateElement(section, data)


@app.route('/<section>/graph', methods = ['GET'])
@jwt_required
def selectGraphSC(section):
    userID = get_jwt_identity()
    return selectGraph(section, userID)

@app.route('/<section>/grouped', methods = ['GET'])
@jwt_required
def selectGroupedElementsSC(section):
    userID = get_jwt_identity()
    return selectGroupedElements(section, userID)

@app.route('/<select>/select', methods = ['GET'])
@jwt_required
def selectToSelectSC(select):
    userID = get_jwt_identity()
    return selectToSelect(select, userID)

@app.route('/<section>/equalelements', methods = ['POST'])
@jwt_required
def selectEqualElementsSC(section):
    userID = get_jwt_identity()
    data = request.get_json(silent = True)
    return selectEqualElements(section, userID, data)


@app.route('/<section>/info/<elementID>', methods = ['GET'])
@jwt_required
def selectInfoSC(section, elementID):
    return selectInfo(section, elementID)


# STARTING APP
if __name__ == "__main__":
    if os.environ["FLASK_ENV"] == 'production':
        from waitress import serve
        serve(app = app, host = "0.0.0.0", port = app.port)
    else:
        app.run(host = "0.0.0.0", port = app.port, debug = True)
