from flask import request
from flask_restful import Resource


class Todo_Api(Resource):
    def get(self):
        return {'message': 'Server is running'}

    def post(self):
        data = request.get_json()
        # Process the data and return a response
        return {'message': 'Data received', 'data': data}

    def put(self):
        data = request.get_json()
        # Update the server configuration with the provided data
        return {'message': 'Server configuration updated', 'data': data}

    def delete(self):
        # Perform any necessary cleanup or shutdown procedures
        return {'message': 'Server deleted'}