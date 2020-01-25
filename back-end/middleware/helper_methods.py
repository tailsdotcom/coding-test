"""All Generic Helper Methods will be here"""

import math

import requests

from middleware import errors


class HelperMethods:
    """These are generic methods that are not class specific"""

    @staticmethod
    def sort_json_by_key(json_list: list, key_to_sort_by: str, reverse_order: bool = False) -> list:
        """Takes a list of dicts and sorts it by a given key in the order specified.

        :param json_list: This is the list to be sorted.
        :type json_list: list
        :param key_to_sort_by: This is the key value that you wish to sort by.
        :type key_to_sort_by: str
        :param reverse_order: (optional) Flag that if True reverses the order that the list e.g. Z-A rather than A-Z.
        :return: An alphabetically sorted list of dicts.
        :rtype: list
        :raises: middleware.errors.MiddlewareInputError
        """
        try:
            return sorted(
                json_list, key=lambda k: (k[key_to_sort_by] is None, k[key_to_sort_by]), reverse=reverse_order
            )
        except KeyError:
            raise errors.MiddlewareInputError("Key Error")
        except TypeError:
            raise errors.MiddlewareInputError("Type Error")

    @staticmethod
    def bulk_search_postcodes_io(list_of_postcodes: list) -> dict:
        """Takes a list of postcodes in string format and submits a bulk post request to postcodes.io for information

        :param list_of_postcodes: A list of strings of postcodes e.g. ["OX49 5NU", "M32 0JG", "NE30 1DP"].
        :type list_of_postcodes: list
        :return: The formatted result key from postcodes.io's response
        :rtype: dict
        :raises: middleware.errors.MiddlewareInputError, middleware.errors.MiddlewareInternalError
        """
        try:
            post_code_search = requests.post(
                "https://api.postcodes.io/postcodes", json={"postcodes": list_of_postcodes}
            )
            # This is the requests status code
            if post_code_search.status_code == 200:
                output = {}
                status_code = post_code_search.json()["status"]
                # This is the postcodes.io status code (also needs checking)
                if status_code == 200:
                    for result in post_code_search.json()["result"]:
                        # stops duplicate postcode returns from being added
                        if result["query"] not in output:
                            # checks that the result exists
                            if result["result"]:
                                output[result["query"]] = result["result"]
                            else:
                                # todo: log this
                                print(result["query"] + " is an invalid postcode")
                                output[result["query"]] = None
                    return output
                if str(status_code)[:1] == "4":
                    raise errors.MiddlewareInputError
                raise errors.MiddlewareInternalError
            if str(post_code_search.status_code)[:1] == "4":
                raise errors.MiddlewareInputError
            raise errors.MiddlewareInternalError
        except requests.RequestException:
            raise errors.MiddlewareInternalError

    @staticmethod
    def single_search_postcodes_io(postcode: str) -> dict:
        """Takes a postcode in string format and submits a get request to postcodes.io for information

        :param postcode: A postcodes e.g. "OX49 5NU".
        :type postcode: str
        :return: The formatted result key from postcodes.io's response
        :rtype: dict
        :raises: middleware.errors.MiddlewareInputError, middleware.errors.MiddlewareInternalError
        """
        # return {}
        try:
            post_code_search_result = requests.get(f"https://api.postcodes.io/postcodes/{postcode}")
            # This is the requests status code
            status_code = post_code_search_result.status_code
            if status_code == 200:
                output = {}
                result = post_code_search_result.json()
                if "status" in result:
                    status_code = post_code_search_result.json()["status"]
                    # This is the postcodes.io status code (also needs checking)
                    if status_code == 200:
                        result = post_code_search_result.json()
                        if "result" in result:
                            output[postcode] = result["result"]
                        else:
                            raise errors.MiddlewareInputError
                        return output
                    if str(status_code)[:1] == "4":
                        raise errors.MiddlewareInputError
                    raise errors.MiddlewareInternalError
                raise errors.MiddlewareInputError
            if str(status_code)[:1] == "4":
                raise errors.MiddlewareInputError
            raise errors.MiddlewareInternalError
        except requests.RequestException:
            raise errors.MiddlewareInternalError

    @staticmethod
    def haversine_formula(latitude_1: float, latitude_2: float, longitude_1: float, longitude_2: float) -> float:
        """Returns the distance between two co-ordinates longitude and latitude in km

        :param latitude_1: latitude of the first ordinate
        :type latitude_1: float
        :param latitude_2: latitude of the second ordinate
        :type latitude_2: float
        :param longitude_1: longitude of the first ordinate
        :type longitude_1: float
        :param longitude_2: longitude of the second ordinate
        :type longitude_2: float
        :return: the distance between the points in km
        :rtype: float
        """
        try:
            earth_radius_meters = 6371e3
            latitude_1_radians = math.radians(latitude_1)
            latitude_2_radians = math.radians(latitude_2)
            delta_latitude = math.radians(latitude_2 - latitude_1)
            delta_longitude = math.radians(longitude_2 - longitude_1)
            square_of_half_chord_length = math.sin(delta_latitude / 2) * math.sin(delta_latitude / 2) + math.cos(
                latitude_1_radians
            ) * math.cos(latitude_2_radians) * math.sin(delta_longitude / 2) * math.sin(delta_longitude / 2)
            angular_distance_radians = 2 * math.atan2(
                math.sqrt(square_of_half_chord_length), math.sqrt(1 - square_of_half_chord_length)
            )
            distance_km = (earth_radius_meters * angular_distance_radians) / 1000
            return float("%.2f" % distance_km)
        except TypeError:
            raise errors.MiddlewareInputError
