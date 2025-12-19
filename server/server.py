from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from server.api import todo_api
from server.api.db_utils import exec_sql_file


app = Flask(__name__)
CORS(app)
api = Api(app)

api.add_resource(todo_api, '/assignments')
api.add_resource(todo_api, '/assignments/<int:todo_id>')
if __name__ == '__main__':
    print("loading database")
    exec_sql_file('data.sql')
    print("database loaded")
    app.run(debug=True)