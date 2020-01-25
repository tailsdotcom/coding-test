"""This module contains all functions that interface with the stores_json"""

import copy
import json
from pathlib import Path

from middleware import errors
from middleware import helper_methods


class Middleware:
    """This is the only class in this module and contains all functions surrounding the interface between the API
    endpoints and the json file"""

    def __init__(self, json_location: str):
        """This sets up the class, it requires the location of the json file. It then verifies the data in the json
        file.

        :param json_location: The location of the json file
        :type json_location: str
        """
        self.helper_methods = helper_methods.HelperMethods()
        self.json_location = Path(json_location)
        self.json_stores = self.import_json_stores()
        self.verify_stores_data()

    def verify_stores_data(self) -> None:
        """Ensures that the stores json file has the minimum required keys e.i. name and postcode.

        :return: None.
        :raises: errors.MiddlewareInternalError
        """
        for store in self.json_stores:
            if "name" not in store:
                print("Error")
                raise errors.MiddlewareInternalError
            if "postcode" not in store:
                print("Error")
                raise errors.MiddlewareInternalError

    def import_json_stores(self) -> list:
        """Imports the json file from the location given in self.json_location then returns the list.

        :return: List containing the data from the stores.json file.
        """
        try:
            with open(self.json_location) as json_file:
                data = json.load(json_file)
            return data
        except IOError:
            return []

    def save_json_stores(self) -> None:
        """Saves the contents of self.json_stores to the file specified in self.json_location.

        :return: None.
        :raises: errors.MiddlewareInternalError
        """
        try:
            with open(self.json_location, "w+") as outfile:
                json.dump(self.json_stores, outfile)
        except IOError:
            raise errors.MiddlewareInternalError

    def sort_array_alphabetically_by_name(self) -> list:
        """Takes the stores json and sorts it by the key "name" then returns that list.

        :return: sorted values from self.json_stores.
        :rtype: list
        :raises: errors.MiddlewareInputError
        """
        try:
            self.json_stores = self.helper_methods.sort_json_by_key(self.json_stores, "name")
            self.save_json_stores()
            return self.json_stores
        except errors.MiddlewareInputError:
            raise errors.MiddlewareInputError

    def sort_array_alphabetically_by_postcode(self):
        """Takes the stores json and sorts it by the key "postcode" then returns that list.

        :return: sorted values from self.json_stores.
        :rtype: list
        :raises: errors.MiddlewareInputError
        """
        try:
            self.json_stores = self.helper_methods.sort_json_by_key(self.json_stores, "postcode")
            self.save_json_stores()
            return self.json_stores
        except errors.MiddlewareInputError:
            raise errors.MiddlewareInputError

    def postcodes_io_lookup(self) -> list:
        """Performs an API request to postcodes.io using the postcodes in self.json_stores. It updates self.json_stores
        with the longitude and latitude and postcode_validity and then returns self.json_stores.

        :return: An updated version of self.json_stores with longitude and latitude and postcode_validity.
        :rtype: list
        :raises: errors.MiddlewareInternalError, errors.MiddlewareInputError
        """
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

    def nearest_store_lookup(self, postcode: str, max_distance: float) -> list:
        """Takes the postcode given and calculates all distances using the haversine function, it then excludes all
        entries that are greater than the max_distance parameter. It then sorts the output by latitude giving a North
        to South list of store locations within the max_distance.

        :param postcode: A valid UK postcode string.
        :type postcode: str
        :param max_distance: The maximum distance a store can be from the given postcode in Km.
        :type max_distance: float
        :return: A list of store locations within the max_distance, ordered by North to South.
        :rtype: list
        :raises: errors.MiddlewareInputError, errors.MiddlewareInternalError
        """
        try:
            user_location = self.helper_methods.single_search_postcodes_io(postcode)
            user_location = user_location[postcode]
            distances = {}
            for store in self.json_stores:
                if store["latitude"] and store["longitude"]:
                    distance = self.helper_methods.haversine_formula(
                        user_location["latitude"], store["latitude"], user_location["longitude"], store["longitude"]
                    )
                    distances[store["postcode"]] = distance
            json_stores_copy = copy.deepcopy(self.json_stores)
            for store in json_stores_copy:
                if store["postcode"] in distances:
                    store["distance_to_store_in_km"] = distances[store["postcode"]]
                else:
                    store["distance_to_store_in_km"] = None
            # remove any None value for distance_to_store_in_km
            json_stores_copy[:] = [d for d in json_stores_copy if d.get("distance_to_store_in_km")]
            # remove any value that are greater than max_distance for distance_to_store_in_km
            json_stores_copy[:] = [
                d for d in json_stores_copy if d.get("distance_to_store_in_km") < float(max_distance)
            ]
            # order by longitude i.e. North to South
            json_stores_copy = self.helper_methods.sort_json_by_key(json_stores_copy, "latitude")
            return json_stores_copy
        except errors.MiddlewareInputError:
            raise errors.MiddlewareInputError
        except errors.MiddlewareInternalError:
            raise errors.MiddlewareInternalError
