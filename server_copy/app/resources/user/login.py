from flask_restful import Resource, reqparse
from flask import request


class login(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username', required=True, nullable=False)
    parser.add_argument('password', required=True, nullable=False)

    def put(self):

        data = self.parser.parse_args(strict=True)

        # Do Validation....

        return data
