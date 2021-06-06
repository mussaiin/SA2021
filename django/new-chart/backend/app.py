import os
import time
import json
import flask
from flask import Flask
from flask_cors import CORS

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

if __name__ == "__main__":
    time.sleep(10)
    app.run(host='0.0.0.0', port='80')
