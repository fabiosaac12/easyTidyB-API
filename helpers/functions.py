from decimal import Decimal
from datetime import date
import json

def jsonDefault(obj):
    if isinstance(obj, Decimal) or isinstance(obj, date):
        return str(obj)
    raise TypeError("Object of type '%s' is not JSON serializable" % type(obj).__name__)

# to convert lists of lists to JSON format
def toJSON(cursor, lofl):
    columns = [x[0] for x in cursor.description]
    jsonResult = []
    for ele in lofl:
        jsonResult.append(dict(zip(columns,ele)))

    return json.dumps(jsonResult, default=jsonDefault)

# to really know if a string contains only spaces (different to a string that does not contain any character) 
def isSpace(string):
    return (string=='' or string.isspace())
