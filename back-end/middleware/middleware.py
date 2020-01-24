import json
import sys
from pathlib import Path

from middleware import errors
from middleware import helper_methods


class Middleware:
    def __init__(self, json_location: str):
        self.helper_methods = helper_methods.HelperMethods()
        self.json_location = Path(json_location)
        self.json_stores = self.import_json_stores()
        self.verify_stores_data()

    def verify_stores_data(self):
        for store in self.json_stores:
            if "name" not in store:
                print("Error")
                sys.exit(1)
            if "postcode" not in store:
                print("Error")
                sys.exit(1)

    def import_json_stores(self):
        try:
            with open(self.json_location) as json_file:
                data = json.load(json_file)
            return data
        except IOError:
            return []

    def save_json_stores(self):
        try:
            with open(self.json_location, "w+") as outfile:
                json.dump(self.json_stores, outfile)
        except IOError:
            raise errors.MiddlewareInternalError

    def sort_array_alphabetically_by_name(self):
        try:
            return self.helper_methods.sort_json_alphabetically_by_key(self.json_stores, "name")
        except errors.MiddlewareInputError:
            raise errors.MiddlewareInputError

    def sort_array_alphabetically_by_postcode(self):
        try:
            return self.helper_methods.sort_json_alphabetically_by_key(self.json_stores, "postcode")
        except errors.MiddlewareInputError:
            raise errors.MiddlewareInputError
