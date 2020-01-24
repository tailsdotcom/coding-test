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
        """
        try:
            return sorted(json_list, key=lambda k: k[key_to_sort_by], reverse=reverse_order)
        except KeyError:
            raise errors.MiddlewareInputError("Key Error")
