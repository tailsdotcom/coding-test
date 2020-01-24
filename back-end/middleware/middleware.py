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
            self.json_stores = self.helper_methods.sort_json_alphabetically_by_key(self.json_stores, "name")
            self.save_json_stores()
            return self.json_stores
        except errors.MiddlewareInputError:
            raise errors.MiddlewareInputError

    def sort_array_alphabetically_by_postcode(self):
        try:
            self.json_stores = self.helper_methods.sort_json_alphabetically_by_key(self.json_stores, "postcode")
            self.save_json_stores()
            return self.json_stores
        except errors.MiddlewareInputError:
            raise errors.MiddlewareInputError

    def postcodes_io_lookup(self):
        search_list = []
        for store in self.json_stores:
            # if the store already has longitude & latitude skip as it has already been searched for
            if "longitude" not in store or "latitude" not in store:
                search_list.append(store["postcode"])

        try:
            returned_search_list = self.helper_methods.bulk_search_postcodes_io(search_list)
        except errors.MiddlewareInputError:
            raise errors.MiddlewareInputError
        except errors.MiddlewareInternalError:
            raise errors.MiddlewareInternalError

        for store in self.json_stores:
            if store["postcode"] in returned_search_list:
                if returned_search_list[store["postcode"]]:
                    store["postcode_validity"] = True
                    store["longitude"] = returned_search_list[store["postcode"]]["longitude"]
                    store["latitude"] = returned_search_list[store["postcode"]]["latitude"]
                else:
                    store["postcode_validity"] = False
                    store["longitude"] = None
                    store["latitude"] = None

        self.save_json_stores()
        return self.json_stores


