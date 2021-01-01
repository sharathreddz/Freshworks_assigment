import json
import uuid
from pathlib import Path
from sys import getsizeof
from datetime import datetime
from flask import Flask, request, jsonify

DATABSE_FILE_NAME = 'database.json'
database  = []
app = Flask(__name__)

def write_json(data, filename='database.json'):
    with open(filename,'w') as f:
        json.dump(data, f, indent=4)

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == "GET":
        with open('database.json') as f:
            database = json.load(f)
        file_size = Path(DATABSE_FILE_NAME).stat().st_size
        if (int(file_size) >= 1073741824):
            sendf = [
                {
                    "DATA_FILE_SIZE": str(Path(DATABSE_FILE_NAME).stat().st_size,),
                    "DATA_SIZE_LIMIT": "1 GB",
                    "DATA_SIZE_LIMIT_PERMISSION": "REJECT-PERMISSION"
                }
            ]
        else:
            with open('database.json') as f:
                database = json.load(f)
            sendf = [
                {
                    "DATA_FILE_SIZE": Path(DATABSE_FILE_NAME).stat().st_size,
                    "DATA_SIZE_LIMIT": "1 GB",
                    "DATA_SIZE_LIMIT_PERMISSION": "ACCEPT-PERMISSION"
                },
                {
                    "database": database,
                }
            ]
        return jsonify(sendf)
    if request.method == "POST":
        with open('database.json') as f:
            database = json.load(f)
        data = request.json
        current_instance = {
            "id": str(uuid.uuid4()),
            "name": data["name"],
            "age": data["age"],
            "class": data["current_class"],
            "section": data["current_section"],
            "created_at": str(datetime.now()),
            "updated_at": str(datetime.now())
        }
        sendf = [
            {
                "DATA_FILE_SIZE": Path(DATABSE_FILE_NAME).stat().st_size,
                "DATA_SIZE_LIMIT": "1 GB",
                "DATA_SIZE_LIMIT_PERMISSION": "ACCEPT-PERMISSION",
                "CURRENTINSERT_SIZE": getsizeof(current_instance),
                "FINAL_OUT_SIZE": int(int(getsizeof(current_instance)) + int(Path(DATABSE_FILE_NAME).stat().st_size))
            },
            {
                "DATA": current_instance,
                "TYPE": "INSERT-CRUD-POST",
                "VALID": True
            }
        ]
        att = database["stu_details"]
        att.append(current_instance)
        write_json(database)
        return jsonify(sendf)

@app.route('/<string:id>', methods=['POST'])
def deleteData(id):
    with open('database.json') as f:
        database = json.load(f)
    d = database.get('stu_details')
    for i in range(0, len(d)):
        if d[i].get('id') == id:
            del d[i]
    new = database["stu_details"]
    xx = {}
    xx["stu_details"] = new
    write_json(xx)
    return jsonify(d)


if __name__ == '__main__':
    app.run()
