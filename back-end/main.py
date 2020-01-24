from flask import Flask
from flask_cors import CORS
from flask_restplus import Resource, Api, reqparse

import middleware

FLASK_APP = Flask(__name__)
CORS(FLASK_APP, resources={r"/*": {"origins": "*"}})
FLASK_APP.config["CORS_HEADERS"] = "Content-Type"
APP = Api(app=FLASK_APP, version="1.0", title="Tails.com API")
NAME_SPACE_ARRAY = APP.namespace("sorted", description="Sorts the list")
NAME_SPACE_POSTCODE = APP.namespace("postcode", description="Postcode related queries")
FLASK_APP.config.SWAGGER_UI_DOC_EXPANSION = "list"
MIDDLEWARE = middleware.Middleware("stores.json")
PARSER = reqparse.RequestParser()
GENERIC_RESPONSES = {200: "OK", 400: "Bad Request", 500: "Internal Service Error"}


@NAME_SPACE_ARRAY.route("/name")
class SortedName(Resource):
    @staticmethod
    @APP.doc(responses=GENERIC_RESPONSES)
    def get():
        try:
            return {"status": "success", "data": MIDDLEWARE.sort_array_alphabetically_by_name(), "message": None}, 200
        except middleware.errors.MiddlewareInputError as error:
            return {"status": "failure", "data": None, "message": error}, 400
        except middleware.errors.MiddlewareInternalError as error:
            return {"status": "error", "data": None, "message": error}, 500


@NAME_SPACE_ARRAY.route("/postcode")
class SortedPostcode(Resource):
    @staticmethod
    @APP.doc(responses=GENERIC_RESPONSES)
    def get():
        try:
            return (
                {"status": "success", "data": MIDDLEWARE.sort_array_alphabetically_by_postcode(), "message": None},
                200,
            )
        except middleware.errors.MiddlewareInputError as error:
            return {"status": "failure", "data": None, "message": error}, 400
        except middleware.errors.MiddlewareInternalError as error:
            return {"status": "error", "data": None, "message": error}, 500


@NAME_SPACE_POSTCODE.route("/")
class PostcodeSearch(Resource):
    @staticmethod
    @APP.doc(responses=GENERIC_RESPONSES)
    def get():
        try:
            return (
                {"status": "success", "data": MIDDLEWARE.postcodes_io_lookup(), "message": None},
                200,
            )
        except middleware.errors.MiddlewareInputError as error:
            return {"status": "failure", "data": None, "message": error}, 400
        except middleware.errors.MiddlewareInternalError as error:
            return {"status": "error", "data": None, "message": error}, 500


if __name__ == "__main__":
    FLASK_APP.run(debug=True, host="0.0.0.0")
