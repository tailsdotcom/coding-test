import requests

from middleware import errors


class HelperMethods:
    """These are generic methods that are not class specific"""

    @staticmethod
    def sort_json_alphabetically_by_key(json_list: list, key_to_sort_by: str, reverse_order: bool = False) -> list:
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
            return sorted(json_list, key=lambda k: k[key_to_sort_by], reverse=reverse_order)
        except KeyError:
            raise errors.MiddlewareInputError("Key Error")

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
            post_code_search = requests.post('https://api.postcodes.io/postcodes',
                                             json={"postcodes": list_of_postcodes})
            if post_code_search.status_code == 200:
                output = {}
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
            elif str(post_code_search.status_code)[:1] == "4":
                raise errors.MiddlewareInputError
            elif str(post_code_search.status_code)[:1] == "5":
                raise errors.MiddlewareInternalError
        except requests.RequestException:
            raise errors.MiddlewareInternalError
