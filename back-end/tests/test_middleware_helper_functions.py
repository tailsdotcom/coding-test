import os
import sys
import unittest

import middleware

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


class MiddlewareHelper(unittest.TestCase):
    def setUp(self) -> None:
        self.helper_methods = middleware.HelperMethods()

    def test_sort_json_by_key_correct(self):
        unsorted_list_of_dicts = [{"name": "z"}, {"name": "g"}, {"name": "q"}, {"name": "n"}, {"name": "i"}]
        sorted_list_of_dicts = [{"name": "g"}, {"name": "i"}, {"name": "n"}, {"name": "q"}, {"name": "z"}]
        self.assertEqual(self.helper_methods.sort_json_by_key(unsorted_list_of_dicts, "name"), sorted_list_of_dicts)

    def test_sort_json_by_key_correct_reverse(self):
        unsorted_list_of_dicts = [{"name": "z"}, {"name": "g"}, {"name": "q"}, {"name": "n"}, {"name": "i"}]
        sorted_list_of_dicts = [{"name": "z"}, {"name": "q"}, {"name": "n"}, {"name": "i"}, {"name": "g"}]
        self.assertEqual(
            self.helper_methods.sort_json_by_key(unsorted_list_of_dicts, "name", True), sorted_list_of_dicts
        )

    def test_sort_json_by_key_incorrect_no_key(self):
        unsorted_list_of_dicts = [{"names": "z"}, {"names": "g"}, {"names": "q"}, {"names": "n"}, {"names": "i"}]
        self.assertRaises(
            middleware.MiddlewareInputError, self.helper_methods.sort_json_by_key, unsorted_list_of_dicts, "name"
        )

    def test_sort_json_by_key_correct_none(self):
        unsorted_list_of_dicts = [{"name": "z"}, {"name": "g"}, {"name": "q"}, {"name": None}, {"name": "i"}]
        sorted_list_of_dicts = [{"name": "g"}, {"name": "i"}, {"name": "q"}, {"name": "z"}, {"name": None}]
        self.assertEqual(self.helper_methods.sort_json_by_key(unsorted_list_of_dicts, "name"), sorted_list_of_dicts)

    def test_sort_json_by_key_incorrect_bool(self):
        unsorted_list_of_dicts = [{"name": "z"}, {"name": True}, {"name": 1}, {"name": "n"}, {"name": 4.6}]
        self.assertRaises(
            middleware.MiddlewareInputError, self.helper_methods.sort_json_by_key, unsorted_list_of_dicts, "name"
        )

    def test_sort_json_by_key_incorrect_int(self):
        unsorted_list_of_dicts = [{"names": "z"}, {"names": 8}, {"names": "q"}, {"names": "n"}, {"names": "i"}]
        self.assertRaises(
            middleware.MiddlewareInputError, self.helper_methods.sort_json_by_key, unsorted_list_of_dicts, "name"
        )

    def test_sort_json_by_key_incorrect_float(self):
        unsorted_list_of_dicts = [{"names": "z"}, {"names": "g"}, {"names": "q"}, {"names": "n"}, {"names": 4.6}]
        self.assertRaises(
            middleware.MiddlewareInputError, self.helper_methods.sort_json_by_key, unsorted_list_of_dicts, "name"
        )

    def test_bulk_search_postcodes_io_correct(self):
        list = ["OX49 5NU", "M32 0JG", "NE30 1DP"]
        output = {
            "OX49 5NU": {
                "postcode": "OX49 5NU",
                "quality": 1,
                "eastings": 464438,
                "northings": 195677,
                "country": "England",
                "nhs_ha": "South Central",
                "longitude": -1.069876,
                "latitude": 51.6562,
                "european_electoral_region": "South East",
                "primary_care_trust": "Oxfordshire",
                "region": "South East",
                "lsoa": "South Oxfordshire 011B",
                "msoa": "South Oxfordshire 011",
                "incode": "5NU",
                "outcode": "OX49",
                "parliamentary_constituency": "Henley",
                "admin_district": "South Oxfordshire",
                "parish": "Brightwell Baldwin",
                "admin_county": "Oxfordshire",
                "admin_ward": "Chalgrove",
                "ced": "Chalgrove and Watlington",
                "ccg": "NHS Oxfordshire",
                "nuts": "Oxfordshire",
                "codes": {
                    "admin_district": "E07000179",
                    "admin_county": "E10000025",
                    "admin_ward": "E05009735",
                    "parish": "E04008109",
                    "parliamentary_constituency": "E14000742",
                    "ccg": "E38000136",
                    "ccg_id": "10Q",
                    "ced": "E58001238",
                    "nuts": "UKJ14",
                },
            },
            "M32 0JG": {
                "postcode": "M32 0JG",
                "quality": 1,
                "eastings": 379988,
                "northings": 395476,
                "country": "England",
                "nhs_ha": "North West",
                "longitude": -2.302836,
                "latitude": 53.455654,
                "european_electoral_region": "North West",
                "primary_care_trust": "Trafford",
                "region": "North West",
                "lsoa": "Trafford 003C",
                "msoa": "Trafford 003",
                "incode": "0JG",
                "outcode": "M32",
                "parliamentary_constituency": "Stretford and Urmston",
                "admin_district": "Trafford",
                "parish": "Trafford, unparished area",
                "admin_county": None,
                "admin_ward": "Gorse Hill",
                "ced": None,
                "ccg": "NHS Trafford",
                "nuts": "Greater Manchester South West",
                "codes": {
                    "admin_district": "E08000009",
                    "admin_county": "E99999999",
                    "admin_ward": "E05000829",
                    "parish": "E43000163",
                    "parliamentary_constituency": "E14000979",
                    "ccg": "E38000187",
                    "ccg_id": "02A",
                    "ced": "E99999999",
                    "nuts": "UKD34",
                },
            },
            "NE30 1DP": {
                "postcode": "NE30 1DP",
                "quality": 1,
                "eastings": 435958,
                "northings": 568671,
                "country": "England",
                "nhs_ha": "North East",
                "longitude": -1.439269,
                "latitude": 55.011303,
                "european_electoral_region": "North East",
                "primary_care_trust": "North Tyneside",
                "region": "North East",
                "lsoa": "North Tyneside 016C",
                "msoa": "North Tyneside 016",
                "incode": "1DP",
                "outcode": "NE30",
                "parliamentary_constituency": "Tynemouth",
                "admin_district": "North Tyneside",
                "parish": "North Tyneside, unparished area",
                "admin_county": None,
                "admin_ward": "Tynemouth",
                "ced": None,
                "ccg": "NHS North Tyneside",
                "nuts": "Tyneside",
                "codes": {
                    "admin_district": "E08000022",
                    "admin_county": "E99999999",
                    "admin_ward": "E05001130",
                    "parish": "E43000176",
                    "parliamentary_constituency": "E14001006",
                    "ccg": "E38000127",
                    "ccg_id": "99C",
                    "ced": "E99999999",
                    "nuts": "UKC22",
                },
            },
        }
        self.assertEqual(self.helper_methods.bulk_search_postcodes_io(list), output)

    def test_bulk_search_postcodes_io_incorrect(self):
        list = ["ABC", "123", "XYZ"]
        output = {
            "ABC": None,
            "123": None,
            "XYZ": None
        }
        self.assertEqual(self.helper_methods.bulk_search_postcodes_io(list), output)

    def test_single_search_postcodes_io_correct(self):
        output = {
            "OX49 5NU": {
                "postcode": "OX49 5NU",
                "quality": 1,
                "eastings": 464438,
                "northings": 195677,
                "country": "England",
                "nhs_ha": "South Central",
                "longitude": -1.069876,
                "latitude": 51.6562,
                "european_electoral_region": "South East",
                "primary_care_trust": "Oxfordshire",
                "region": "South East",
                "lsoa": "South Oxfordshire 011B",
                "msoa": "South Oxfordshire 011",
                "incode": "5NU",
                "outcode": "OX49",
                "parliamentary_constituency": "Henley",
                "admin_district": "South Oxfordshire",
                "parish": "Brightwell Baldwin",
                "admin_county": "Oxfordshire",
                "admin_ward": "Chalgrove",
                "ced": "Chalgrove and Watlington",
                "ccg": "NHS Oxfordshire",
                "nuts": "Oxfordshire",
                "codes": {
                    "admin_district": "E07000179",
                    "admin_county": "E10000025",
                    "admin_ward": "E05009735",
                    "parish": "E04008109",
                    "parliamentary_constituency": "E14000742",
                    "ccg": "E38000136",
                    "ccg_id": "10Q",
                    "ced": "E58001238",
                    "nuts": "UKJ14",
                },
            },
            "M32 0JG": {
                "postcode": "M32 0JG",
                "quality": 1,
                "eastings": 379988,
                "northings": 395476,
                "country": "England",
                "nhs_ha": "North West",
                "longitude": -2.302836,
                "latitude": 53.455654,
                "european_electoral_region": "North West",
                "primary_care_trust": "Trafford",
                "region": "North West",
                "lsoa": "Trafford 003C",
                "msoa": "Trafford 003",
                "incode": "0JG",
                "outcode": "M32",
                "parliamentary_constituency": "Stretford and Urmston",
                "admin_district": "Trafford",
                "parish": "Trafford, unparished area",
                "admin_county": None,
                "admin_ward": "Gorse Hill",
                "ced": None,
                "ccg": "NHS Trafford",
                "nuts": "Greater Manchester South West",
                "codes": {
                    "admin_district": "E08000009",
                    "admin_county": "E99999999",
                    "admin_ward": "E05000829",
                    "parish": "E43000163",
                    "parliamentary_constituency": "E14000979",
                    "ccg": "E38000187",
                    "ccg_id": "02A",
                    "ced": "E99999999",
                    "nuts": "UKD34",
                },
            },
            "NE30 1DP": {
                "postcode": "NE30 1DP",
                "quality": 1,
                "eastings": 435958,
                "northings": 568671,
                "country": "England",
                "nhs_ha": "North East",
                "longitude": -1.439269,
                "latitude": 55.011303,
                "european_electoral_region": "North East",
                "primary_care_trust": "North Tyneside",
                "region": "North East",
                "lsoa": "North Tyneside 016C",
                "msoa": "North Tyneside 016",
                "incode": "1DP",
                "outcode": "NE30",
                "parliamentary_constituency": "Tynemouth",
                "admin_district": "North Tyneside",
                "parish": "North Tyneside, unparished area",
                "admin_county": None,
                "admin_ward": "Tynemouth",
                "ced": None,
                "ccg": "NHS North Tyneside",
                "nuts": "Tyneside",
                "codes": {
                    "admin_district": "E08000022",
                    "admin_county": "E99999999",
                    "admin_ward": "E05001130",
                    "parish": "E43000176",
                    "parliamentary_constituency": "E14001006",
                    "ccg": "E38000127",
                    "ccg_id": "99C",
                    "ced": "E99999999",
                    "nuts": "UKC22",
                },
            },
        }
        for test in output:
            self.assertEqual(self.helper_methods.single_search_postcodes_io(test), {test: output[test]})

    def test_single_search_postcodes_io_incorrect(self):
        self.assertRaises(middleware.MiddlewareInputError, self.helper_methods.single_search_postcodes_io, "ABC")
        self.assertRaises(middleware.MiddlewareInputError, self.helper_methods.single_search_postcodes_io, "123")
        self.assertRaises(middleware.MiddlewareInputError, self.helper_methods.single_search_postcodes_io, "XYZ")

    def test_haversine_formula_correct(self):
        print("test")
