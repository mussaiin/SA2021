import os
import time
import json
import flask
from flask import Flask
from flask_cors import CORS
from flask import request
from flask import make_response, jsonify

app = Flask(__name__)
cors = CORS(app)

@app.route("/")
def hello():
    return os.environ['GREETINGS'] + ' from ' + os.environ['HOSTNAME'] + "!"

@app.route("/config")
def config():
    return json.dumps(config)

@app.route("/version")
def version():
    return {"version":"0.1"}

@app.route("/db")
def db():
    from sqlalchemy import create_engine
    engine = create_engine(os.environ['DATABASE_URI'], echo=True)
    rows = []
    with engine.connect() as connection:
        result = connection.execute('select id, name from client;')
        rows = [dict(r.items()) for r in result]
    return json.dumps(rows)

@app.route('/user', methods=['POST', 'PUT'])
def create_user():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            from sqlalchemy import create_engine
            engine = create_engine(os.environ['DATABASE_URI'], echo=True)
            with engine.connect() as connection:
                result = connection.execute("INSERT INTO client (id, name) VALUES (?, ?) ;", (data.id, data.name))
                print('res get', result)
            return f"{data.id}  {data.name}"
        else:
            return {"error": "The request payload is not in JSON format"}

    elif request.method == 'PUT':
        if request.is_json:
            data = request.get_json()
            from sqlalchemy import create_engine
            engine = create_engine(os.environ['DATABASE_URI'], echo=True)
            with engine.connect() as connection:
                result = connection.execute("UPDATE client c SET name=(?) where c.id=(?) ;", (data.name), (data.id))
                print('res get', result)
            return {'success': True}
        else:
            return {"error": "The request payload is not in JSON format"}


@app.route('/user/<int:user_id>', methods=['GET', 'DELETE'])
def edit_user(user_id):
    if request.method == 'GET':
        from sqlalchemy import create_engine
        engine = create_engine(os.environ['DATABASE_URI'], echo=True)
        with engine.connect() as connection:
            result = connection.execute("select id, name from client c where c.id=(?) ;", (user_id))
            print('res get', result)
            return {'success': True}
    elif request.method == 'DELETE':
        from sqlalchemy import create_engine
        engine = create_engine(os.environ['DATABASE_URI'], echo=True)
        with engine.connect() as connection:
            result = connection.execute("DELETE FROM client c WHERE c.id=(?);", (user_id))
            print('res delete', result)
            return {'success': True}

if __name__ == "__main__":
    time.sleep(10)
    app.run(host='0.0.0.0', port='80')
