# IMPORTS
from database import sql
from flask import jsonify
import json
import time
from helpers.functions import isSpace


# to prevent various requests at same time
requesting = False
def wait(function):
    def wrapper(*args, **kwargs):
        global requesting
        while requesting:
            time.sleep(0.5)
        requesting = True       
        result = function(*args, **kwargs)
        requesting = False
        return result
    return wrapper


# to send all the data from the detailed view
@wait
def selectElements(section, userID):
    query = "SELECT * FROM {}View WHERE userID={}".format(section.lower(), userID)
    result = sql.run(query) 

    try:
        resultJSON = json.loads(result)
    except:
        resultJSON = result
    return jsonify(resultJSON)


# to send the graph data
@wait
def selectGraph(section, userID):
    query = "SELECT * FROM {}Graph WHERE userID={}".format(section, userID)
    result = sql.run(query) 

    try:
        resultJSON = json.loads(result)
    except:
        resultJSON = result
    return jsonify(resultJSON)

# to send all gruped elements of the table
@wait
def selectGroupedElements(section, userID):
    query = "SELECT * FROM grouped{}View WHERE userID={}".format(section.capitalize(), userID)
    result = sql.run(query)    

    try:
        resultJSON = json.loads(result)
    except:
        resultJSON = result
    return jsonify(resultJSON)


# to send all elements of the table
@wait
def selectToSelect(select, userID):
    query = "SELECT * FROM {}SelectView WHERE userID={}".format(select, userID)
    result = sql.run(query) 

    try:
        resultJSON = json.loads(result)
    except:
        resultJSON = result
    return jsonify(resultJSON)


# to send all the equal elements to another
@wait
def selectEqualElements(section, userID, element):
    if section.lower() == "sales":
        client = " IS NULL" if isSpace(element["client"]) else " = '{}'".format(element['client'])
        date = " IS NULL" if isSpace(element["date"]) else " = '{}'".format(element['date'])
        query = "SELECT id, product, quantity, obtained, profit, discount, date, type, client, clientID, productID, orderID FROM salesView WHERE client{} and date{} and userID={}".format(
            client, date, userID)
    elif section.lower() == "products":
        name = " IS NULL" if isSpace(element["name"]) else " = '{}'".format(element['name'])
        char1 = " IS NULL" if isSpace(element["char1"]) else " = '{}'".format(element['char1'])
        char2 = " IS NULL" if isSpace(element["char2"]) else " = '{}'".format(element['char2'])
        query = "SELECT id, `order`, name, char1, char2, initialStock, available, sold, retailPrice, wholesalePrice, purchasePrice, obtained, profit, invested, orderID, userID FROM productsView WHERE name{} and char1{} and char2{} and userID={}".format(
            name, char1, char2, userID)
    result = sql.run(query)

    try:
        resultJSON = json.loads(result)
    except:
        resultJSON = result
    return jsonify(resultJSON)


# to insert one or more elements
@wait
def insertElements(section, userID, elements):
    query = "INSERT INTO {} ".format(section.lower())
    query += "(userID, "
    for item in elements[0]:
        query += "{},".format(item)
    query = query.rstrip(",") + ") VALUES "
    for element in elements:
        query += "({}, ".format(userID)
        for value in element.values():
            value = 'NULL' if isSpace(value) else "'{}'".format(value)
            query += "{},".format(value)
        query = query.rstrip(",") + "),"
    query = query.rstrip(",")
    result = sql.run(query, fetch=False)

    return result


# to delete one ore more elements
@wait
def deleteElements(section, ids):
    if len(ids) > 1:
        query = "DELETE FROM {} WHERE id IN {}".format(section.lower(), ids)
    else:
        query = "DELETE FROM {} WHERE id={}".format(section.lower(), ids[0])
    result = sql.run(query, fetch=False)

    return result


# to update one element
@wait
def updateElement(section, updatedElement):
    query = "UPDATE {} SET ".format(section.lower())
    for key, value in updatedElement.items():
        newValue = "NULL" if isSpace(value) else "'{}'".format(value)
        query += "{}={},".format(key, newValue)
    query = query.rstrip(",")
    query += " WHERE id={}".format(updatedElement["id"])
    result = sql.run(query, fetch=False)

    return result

# to sign in
@wait
def login(user):
    query = "SELECT id as userID, username FROM users WHERE username='{}' and password='{}'".format(user["username"], user["password"])
    result = sql.run(query, fetch=True)

    try:
        resultJSON = json.loads(result)[0]
        return jsonify(resultJSON)
    except IndexError:
        return {
            "username": False,
            "userID": False
        }
    except Exception as e:
        return result

#to sign up
@wait
def signup(user):
    query = "INSERT INTO users VALUES (null, '{}', '{}')".format(user['username'], user['password'])
    result = sql.run(query, fetch=False)

    result['username'] = user['username']
    return result
