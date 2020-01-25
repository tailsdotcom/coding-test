import copy
import json
import os
import sys
import unittest
from pathlib import Path

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

    def test_single_search_postcodes_io_incorrect_bad_url(self):
        self.assertRaises(middleware.MiddlewareInputError, self.helper_methods.single_search_postcodes_io, [67])

    def test_single_search_postcodes_io_incorrect_bad_path(self):
        self.assertRaises(middleware.MiddlewareInputError, self.helper_methods.single_search_postcodes_io,
                          "invalid/test")

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
        """https://www.movable-type.co.uk/scripts/latlong.html?from=51.597747,-0.387732&to=51.110464,0.180509
        This website defines the distance as around 67.03km
        """

        lon1 = -0.387732
        lat1 = 51.597747
        lon2 = 0.180509
        lat2 = 51.110464

        self.assertEqual(self.helper_methods.haversine_formula(lat1, lat2, lon1, lon2), 67.03)

    def test_haversine_formula_correct_int(self):
        """https://www.movable-type.co.uk/scripts/latlong.html?from=51.597747,0&to=51.110464,0.180509
        This website defines the distance as around 55.61km
        """

        lon1 = 0
        lat1 = 51.597747
        lon2 = 0.180509
        lat2 = 51.110464

        self.assertEqual(self.helper_methods.haversine_formula(lat1, lat2, lon1, lon2), 55.61)

    def test_haversine_formula_incorrect_type_string(self):
        lon1 = "abc"
        lat1 = 51.597747
        lon2 = 0.180509
        lat2 = 51.110464

        self.assertRaises(middleware.MiddlewareInputError, self.helper_methods.haversine_formula, lat1, lat2, lon1,
                          lon2)


class MiddlewareMiddleware(unittest.TestCase):
    def setUp(self) -> None:
        file_contents = [{"name": "St_Albans", "postcode": "AL1 2RJ"}, {"name": "Hatfield", "postcode": "AL9 5JP"},
                         {"name": "Worthing", "postcode": "BN14 9GB"}, {"name": "Rustington", "postcode": "BN16 3RT"},
                         {"name": "Eastbourne", "postcode": "BN23 6QD"}, {"name": "Hove", "postcode": "BN3 7PN"},
                         {"name": "Newhaven", "postcode": "BN9 0AG"}, {"name": "Orpington", "postcode": "BR5 3RP"},
                         {"name": "Chelmsford", "postcode": "CM2 6XE"}, {"name": "Harlow", "postcode": "CM20 2SX"},
                         {"name": "Croydon", "postcode": "CR0 4NX"},
                         {"name": "Canterbury_Sturry_Road", "postcode": "CT1 1DX"},
                         {"name": "Canterbury", "postcode": "CT1 3TQ"}, {"name": "Broadstairs", "postcode": "CT10 2RQ"},
                         {"name": "Dover", "postcode": "CT16 3PS"}, {"name": "Folkestone", "postcode": "CT19 5SY"},
                         {"name": "Crayford", "postcode": "DA1 4LD"}, {"name": "Gravesend", "postcode": "DA11 0DQ"},
                         {"name": "Chingford", "postcode": "E4 8JA"}, {"name": "Beckton", "postcode": "E6 6LG"},
                         {"name": "Enfield", "postcode": "EN1 1TH"}, {"name": "Waltham_Abbey", "postcode": "EN9 1BY"},
                         {"name": "Farnborough", "postcode": "GU14 7QL"}, {"name": "Bagshot", "postcode": "GU19 5DG"},
                         {"name": "Woking", "postcode": "GU22 8BD"}, {"name": "Alton", "postcode": "GU34 2QS"},
                         {"name": "Godalming", "postcode": "GU7 1DR"}, {"name": "Farnham", "postcode": "GU9 9QJ"},
                         {"name": "Ruislip", "postcode": "HA4 0LN"}, {"name": "High_Wycombe", "postcode": "HP11 1FY"},
                         {"name": "Aylesbury", "postcode": "HP20 1DH"},
                         {"name": "Hemel_Hempstead", "postcode": "HP3 9AA"}, {"name": "Ilford", "postcode": "IG2 6BE"},
                         {"name": "Walton_On_Thames", "postcode": "KT12 2SS"},
                         {"name": "Byfleet", "postcode": "KT14 7NP"}, {"name": "Luton", "postcode": "LU1 3JH"},
                         {"name": "Dunstable", "postcode": "LU5 4XZ"},
                         {"name": "Sittingbourne", "postcode": "ME10 2XD"},
                         {"name": "Maidstone", "postcode": "ME20 7TP"}, {"name": "Chatham", "postcode": "ME5 9SQ"},
                         {"name": "Gillingham", "postcode": "ME8 0PU"}, {"name": "Bletchley", "postcode": "MK1 1BN"},
                         {"name": "Buckingham", "postcode": "MK18 1TB"},
                         {"name": "Friern_Barnet", "postcode": "N11 3PW"}, {"name": "Camden", "postcode": "NW1 9EX"},
                         {"name": "Hendon", "postcode": "NW9 7TH"}, {"name": "Chichester", "postcode": "PO19 7YH"},
                         {"name": "Bognor_Regis", "postcode": "PO22 9NF"},
                         {"name": "Portsmouth", "postcode": "PO3 5LZ"}, {"name": "Havant", "postcode": "PO9 1ND"},
                         {"name": "Bracknell", "postcode": "RG12 1EN"}, {"name": "Reading", "postcode": "RG2 0HB"},
                         {"name": "Basingstoke", "postcode": "RG22 4TT"}, {"name": "Tilehurst", "postcode": "RG30 1PR"},
                         {"name": "Wokingham", "postcode": "RG40 2NU"}, {"name": "Winnersh", "postcode": "RG41 5HH"},
                         {"name": "Redhill", "postcode": "RH1 6QL"}, {"name": "Crawley", "postcode": "RH11 7ST"},
                         {"name": "Horsham", "postcode": "RH12 1HR"}, {"name": "Burgess_Hill", "postcode": "RH15 9QT"},
                         {"name": "East_Grinstead", "postcode": "RH19 1QL"}, {"name": "Dorking", "postcode": "RH4 1RU"},
                         {"name": "Thurrock", "postcode": "RM20 3LP"}, {"name": "Romford", "postcode": "RM7 0AN"},
                         {"name": "Dagenham", "postcode": "RM9 6SJ"}, {"name": "Old_Kent_Road", "postcode": "SE1 5BA"},
                         {"name": "Blackheath", "postcode": "SE10 8DA"}, {"name": "Sydenham", "postcode": "SE26 4PU"},
                         {"name": "Thamesmead", "postcode": "SE28 8RD"}, {"name": "Charlton", "postcode": "SE7 7TZ"},
                         {"name": "Eltham", "postcode": "SE9 5LT"}, {"name": "Hertford", "postcode": "SG13 7RQ"},
                         {"name": "Slough", "postcode": "SL1 4XB"}, {"name": "Maidenhead", "postcode": "SL6 1AY"},
                         {"name": "Southend_Victoria", "postcode": "SS1 1PA"},
                         {"name": "Basildon", "postcode": "SS13 3BY"},
                         {"name": "Basildon_Pipps_Hill", "postcode": "SS14 3AF"},
                         {"name": "Southend-on-Sea", "postcode": "SS2 6FW"}, {"name": "Rayleigh", "postcode": "SS67UP"},
                         {"name": "Battersea", "postcode": "SW11 3RX"}, {"name": "Wimbledon", "postcode": "SW17 0BW"},
                         {"name": "New_Malden", "postcode": "SW20 0JQ"}, {"name": "Sevenoaks", "postcode": "TN14 5EW"},
                         {"name": "Tunbridge_Wells", "postcode": "TN2 3FB"},
                         {"name": "Ashford", "postcode": "TN23 7DH"}, {"name": "Hastings", "postcode": "TN37 7PB"},
                         {"name": "Bexhill", "postcode": "TN40 2JS"}, {"name": "Feltham", "postcode": "TW13 4EX"},
                         {"name": "Brentford", "postcode": "TW8 8JW"}, {"name": "Richmond", "postcode": "TW9 1YB"},
                         {"name": "Hayes", "postcode": "UB4 0TU"}, {"name": "Greenford", "postcode": "UB6 0UW"},
                         {"name": "West_Drayton", "postcode": "UB8 2TE"}, {"name": "Watford", "postcode": "WD17 2SF"},
                         {"name": "Borehamwood", "postcode": "WD6 4PR"}]
        with open(Path("stores-test.json"), "w+") as outfile:
            json.dump(file_contents, outfile)
        self.middleware = middleware.Middleware("stores-test.json")

    def test_sort_by_name(self):
        final_sorted_output = [{"name": "Alton", "postcode": "GU34 2QS"}, {"name": "Ashford", "postcode": "TN23 7DH"},
                               {"name": "Aylesbury", "postcode": "HP20 1DH"},
                               {"name": "Bagshot", "postcode": "GU19 5DG"},
                               {"name": "Basildon", "postcode": "SS13 3BY"},
                               {"name": "Basildon_Pipps_Hill", "postcode": "SS14 3AF"},
                               {"name": "Basingstoke", "postcode": "RG22 4TT"},
                               {"name": "Battersea", "postcode": "SW11 3RX"}, {"name": "Beckton", "postcode": "E6 6LG"},
                               {"name": "Bexhill", "postcode": "TN40 2JS"},
                               {"name": "Blackheath", "postcode": "SE10 8DA"},
                               {"name": "Bletchley", "postcode": "MK1 1BN"},
                               {"name": "Bognor_Regis", "postcode": "PO22 9NF"},
                               {"name": "Borehamwood", "postcode": "WD6 4PR"},
                               {"name": "Bracknell", "postcode": "RG12 1EN"},
                               {"name": "Brentford", "postcode": "TW8 8JW"},
                               {"name": "Broadstairs", "postcode": "CT10 2RQ"},
                               {"name": "Buckingham", "postcode": "MK18 1TB"},
                               {"name": "Burgess_Hill", "postcode": "RH15 9QT"},
                               {"name": "Byfleet", "postcode": "KT14 7NP"}, {"name": "Camden", "postcode": "NW1 9EX"},
                               {"name": "Canterbury", "postcode": "CT1 3TQ"},
                               {"name": "Canterbury_Sturry_Road", "postcode": "CT1 1DX"},
                               {"name": "Charlton", "postcode": "SE7 7TZ"}, {"name": "Chatham", "postcode": "ME5 9SQ"},
                               {"name": "Chelmsford", "postcode": "CM2 6XE"},
                               {"name": "Chichester", "postcode": "PO19 7YH"},
                               {"name": "Chingford", "postcode": "E4 8JA"}, {"name": "Crawley", "postcode": "RH11 7ST"},
                               {"name": "Crayford", "postcode": "DA1 4LD"}, {"name": "Croydon", "postcode": "CR0 4NX"},
                               {"name": "Dagenham", "postcode": "RM9 6SJ"}, {"name": "Dorking", "postcode": "RH4 1RU"},
                               {"name": "Dover", "postcode": "CT16 3PS"}, {"name": "Dunstable", "postcode": "LU5 4XZ"},
                               {"name": "East_Grinstead", "postcode": "RH19 1QL"},
                               {"name": "Eastbourne", "postcode": "BN23 6QD"},
                               {"name": "Eltham", "postcode": "SE9 5LT"}, {"name": "Enfield", "postcode": "EN1 1TH"},
                               {"name": "Farnborough", "postcode": "GU14 7QL"},
                               {"name": "Farnham", "postcode": "GU9 9QJ"}, {"name": "Feltham", "postcode": "TW13 4EX"},
                               {"name": "Folkestone", "postcode": "CT19 5SY"},
                               {"name": "Friern_Barnet", "postcode": "N11 3PW"},
                               {"name": "Gillingham", "postcode": "ME8 0PU"},
                               {"name": "Godalming", "postcode": "GU7 1DR"},
                               {"name": "Gravesend", "postcode": "DA11 0DQ"},
                               {"name": "Greenford", "postcode": "UB6 0UW"}, {"name": "Harlow", "postcode": "CM20 2SX"},
                               {"name": "Hastings", "postcode": "TN37 7PB"},
                               {"name": "Hatfield", "postcode": "AL9 5JP"}, {"name": "Havant", "postcode": "PO9 1ND"},
                               {"name": "Hayes", "postcode": "UB4 0TU"},
                               {"name": "Hemel_Hempstead", "postcode": "HP3 9AA"},
                               {"name": "Hendon", "postcode": "NW9 7TH"}, {"name": "Hertford", "postcode": "SG13 7RQ"},
                               {"name": "High_Wycombe", "postcode": "HP11 1FY"},
                               {"name": "Horsham", "postcode": "RH12 1HR"}, {"name": "Hove", "postcode": "BN3 7PN"},
                               {"name": "Ilford", "postcode": "IG2 6BE"}, {"name": "Luton", "postcode": "LU1 3JH"},
                               {"name": "Maidenhead", "postcode": "SL6 1AY"},
                               {"name": "Maidstone", "postcode": "ME20 7TP"},
                               {"name": "New_Malden", "postcode": "SW20 0JQ"},
                               {"name": "Newhaven", "postcode": "BN9 0AG"},
                               {"name": "Old_Kent_Road", "postcode": "SE1 5BA"},
                               {"name": "Orpington", "postcode": "BR5 3RP"},
                               {"name": "Portsmouth", "postcode": "PO3 5LZ"},
                               {"name": "Rayleigh", "postcode": "SS67UP"}, {"name": "Reading", "postcode": "RG2 0HB"},
                               {"name": "Redhill", "postcode": "RH1 6QL"}, {"name": "Richmond", "postcode": "TW9 1YB"},
                               {"name": "Romford", "postcode": "RM7 0AN"}, {"name": "Ruislip", "postcode": "HA4 0LN"},
                               {"name": "Rustington", "postcode": "BN16 3RT"},
                               {"name": "Sevenoaks", "postcode": "TN14 5EW"},
                               {"name": "Sittingbourne", "postcode": "ME10 2XD"},
                               {"name": "Slough", "postcode": "SL1 4XB"},
                               {"name": "Southend-on-Sea", "postcode": "SS2 6FW"},
                               {"name": "Southend_Victoria", "postcode": "SS1 1PA"},
                               {"name": "St_Albans", "postcode": "AL1 2RJ"},
                               {"name": "Sydenham", "postcode": "SE26 4PU"},
                               {"name": "Thamesmead", "postcode": "SE28 8RD"},
                               {"name": "Thurrock", "postcode": "RM20 3LP"},
                               {"name": "Tilehurst", "postcode": "RG30 1PR"},
                               {"name": "Tunbridge_Wells", "postcode": "TN2 3FB"},
                               {"name": "Waltham_Abbey", "postcode": "EN9 1BY"},
                               {"name": "Walton_On_Thames", "postcode": "KT12 2SS"},
                               {"name": "Watford", "postcode": "WD17 2SF"},
                               {"name": "West_Drayton", "postcode": "UB8 2TE"},
                               {"name": "Wimbledon", "postcode": "SW17 0BW"},
                               {"name": "Winnersh", "postcode": "RG41 5HH"}, {"name": "Woking", "postcode": "GU22 8BD"},
                               {"name": "Wokingham", "postcode": "RG40 2NU"},
                               {"name": "Worthing", "postcode": "BN14 9GB"}]
        sorted_output = copy.deepcopy(self.middleware.sort_array_alphabetically_by_name())
        self.assertEqual(sorted_output, final_sorted_output)

    def test_sort_by_postcode(self):
        final_sorted_output = [{"name": "St_Albans", "postcode": "AL1 2RJ"},
                               {"name": "Hatfield", "postcode": "AL9 5JP"},
                               {"name": "Worthing", "postcode": "BN14 9GB"},
                               {"name": "Rustington", "postcode": "BN16 3RT"},
                               {"name": "Eastbourne", "postcode": "BN23 6QD"}, {"name": "Hove", "postcode": "BN3 7PN"},
                               {"name": "Newhaven", "postcode": "BN9 0AG"},
                               {"name": "Orpington", "postcode": "BR5 3RP"},
                               {"name": "Chelmsford", "postcode": "CM2 6XE"},
                               {"name": "Harlow", "postcode": "CM20 2SX"}, {"name": "Croydon", "postcode": "CR0 4NX"},
                               {"name": "Canterbury_Sturry_Road", "postcode": "CT1 1DX"},
                               {"name": "Canterbury", "postcode": "CT1 3TQ"},
                               {"name": "Broadstairs", "postcode": "CT10 2RQ"},
                               {"name": "Dover", "postcode": "CT16 3PS"},
                               {"name": "Folkestone", "postcode": "CT19 5SY"},
                               {"name": "Crayford", "postcode": "DA1 4LD"},
                               {"name": "Gravesend", "postcode": "DA11 0DQ"},
                               {"name": "Chingford", "postcode": "E4 8JA"}, {"name": "Beckton", "postcode": "E6 6LG"},
                               {"name": "Enfield", "postcode": "EN1 1TH"},
                               {"name": "Waltham_Abbey", "postcode": "EN9 1BY"},
                               {"name": "Farnborough", "postcode": "GU14 7QL"},
                               {"name": "Bagshot", "postcode": "GU19 5DG"}, {"name": "Woking", "postcode": "GU22 8BD"},
                               {"name": "Alton", "postcode": "GU34 2QS"}, {"name": "Godalming", "postcode": "GU7 1DR"},
                               {"name": "Farnham", "postcode": "GU9 9QJ"}, {"name": "Ruislip", "postcode": "HA4 0LN"},
                               {"name": "High_Wycombe", "postcode": "HP11 1FY"},
                               {"name": "Aylesbury", "postcode": "HP20 1DH"},
                               {"name": "Hemel_Hempstead", "postcode": "HP3 9AA"},
                               {"name": "Ilford", "postcode": "IG2 6BE"},
                               {"name": "Walton_On_Thames", "postcode": "KT12 2SS"},
                               {"name": "Byfleet", "postcode": "KT14 7NP"}, {"name": "Luton", "postcode": "LU1 3JH"},
                               {"name": "Dunstable", "postcode": "LU5 4XZ"},
                               {"name": "Sittingbourne", "postcode": "ME10 2XD"},
                               {"name": "Maidstone", "postcode": "ME20 7TP"},
                               {"name": "Chatham", "postcode": "ME5 9SQ"},
                               {"name": "Gillingham", "postcode": "ME8 0PU"},
                               {"name": "Bletchley", "postcode": "MK1 1BN"},
                               {"name": "Buckingham", "postcode": "MK18 1TB"},
                               {"name": "Friern_Barnet", "postcode": "N11 3PW"},
                               {"name": "Camden", "postcode": "NW1 9EX"}, {"name": "Hendon", "postcode": "NW9 7TH"},
                               {"name": "Chichester", "postcode": "PO19 7YH"},
                               {"name": "Bognor_Regis", "postcode": "PO22 9NF"},
                               {"name": "Portsmouth", "postcode": "PO3 5LZ"}, {"name": "Havant", "postcode": "PO9 1ND"},
                               {"name": "Bracknell", "postcode": "RG12 1EN"},
                               {"name": "Reading", "postcode": "RG2 0HB"},
                               {"name": "Basingstoke", "postcode": "RG22 4TT"},
                               {"name": "Tilehurst", "postcode": "RG30 1PR"},
                               {"name": "Wokingham", "postcode": "RG40 2NU"},
                               {"name": "Winnersh", "postcode": "RG41 5HH"}, {"name": "Redhill", "postcode": "RH1 6QL"},
                               {"name": "Crawley", "postcode": "RH11 7ST"}, {"name": "Horsham", "postcode": "RH12 1HR"},
                               {"name": "Burgess_Hill", "postcode": "RH15 9QT"},
                               {"name": "East_Grinstead", "postcode": "RH19 1QL"},
                               {"name": "Dorking", "postcode": "RH4 1RU"}, {"name": "Thurrock", "postcode": "RM20 3LP"},
                               {"name": "Romford", "postcode": "RM7 0AN"}, {"name": "Dagenham", "postcode": "RM9 6SJ"},
                               {"name": "Old_Kent_Road", "postcode": "SE1 5BA"},
                               {"name": "Blackheath", "postcode": "SE10 8DA"},
                               {"name": "Sydenham", "postcode": "SE26 4PU"},
                               {"name": "Thamesmead", "postcode": "SE28 8RD"},
                               {"name": "Charlton", "postcode": "SE7 7TZ"}, {"name": "Eltham", "postcode": "SE9 5LT"},
                               {"name": "Hertford", "postcode": "SG13 7RQ"}, {"name": "Slough", "postcode": "SL1 4XB"},
                               {"name": "Maidenhead", "postcode": "SL6 1AY"},
                               {"name": "Southend_Victoria", "postcode": "SS1 1PA"},
                               {"name": "Basildon", "postcode": "SS13 3BY"},
                               {"name": "Basildon_Pipps_Hill", "postcode": "SS14 3AF"},
                               {"name": "Southend-on-Sea", "postcode": "SS2 6FW"},
                               {"name": "Rayleigh", "postcode": "SS67UP"},
                               {"name": "Battersea", "postcode": "SW11 3RX"},
                               {"name": "Wimbledon", "postcode": "SW17 0BW"},
                               {"name": "New_Malden", "postcode": "SW20 0JQ"},
                               {"name": "Sevenoaks", "postcode": "TN14 5EW"},
                               {"name": "Tunbridge_Wells", "postcode": "TN2 3FB"},
                               {"name": "Ashford", "postcode": "TN23 7DH"},
                               {"name": "Hastings", "postcode": "TN37 7PB"},
                               {"name": "Bexhill", "postcode": "TN40 2JS"}, {"name": "Feltham", "postcode": "TW13 4EX"},
                               {"name": "Brentford", "postcode": "TW8 8JW"},
                               {"name": "Richmond", "postcode": "TW9 1YB"}, {"name": "Hayes", "postcode": "UB4 0TU"},
                               {"name": "Greenford", "postcode": "UB6 0UW"},
                               {"name": "West_Drayton", "postcode": "UB8 2TE"},
                               {"name": "Watford", "postcode": "WD17 2SF"},
                               {"name": "Borehamwood", "postcode": "WD6 4PR"}]
        sorted_output = copy.deepcopy(self.middleware.sort_array_alphabetically_by_postcode())
        self.assertEqual(sorted_output, final_sorted_output)

    def test_postcodes_lookup_correct(self):
        expected_output = [
            {"name": "St_Albans", "postcode": "AL1 2RJ", "postcode_validity": True, "longitude": -0.341337,
             "latitude": 51.741753},
            {"name": "Hatfield", "postcode": "AL9 5JP", "postcode_validity": True, "longitude": -0.222034,
             "latitude": 51.776142},
            {"name": "Worthing", "postcode": "BN14 9GB", "postcode_validity": True, "longitude": -0.36701,
             "latitude": 50.834955},
            {"name": "Rustington", "postcode": "BN16 3RT", "postcode_validity": True, "longitude": -0.498092,
             "latitude": 50.817576},
            {"name": "Eastbourne", "postcode": "BN23 6QD", "postcode_validity": True, "longitude": 0.303047,
             "latitude": 50.787017},
            {"name": "Hove", "postcode": "BN3 7PN", "postcode_validity": True, "longitude": -0.17436,
             "latitude": 50.837916},
            {"name": "Newhaven", "postcode": "BN9 0AG", "postcode_validity": True, "longitude": 0.059491,
             "latitude": 50.798205},
            {"name": "Orpington", "postcode": "BR5 3RP", "postcode_validity": True, "longitude": 0.112496,
             "latitude": 51.392983},
            {"name": "Chelmsford", "postcode": "CM2 6XE", "postcode_validity": True, "longitude": 0.495698,
             "latitude": 51.732632},
            {"name": "Harlow", "postcode": "CM20 2SX", "postcode_validity": True, "longitude": 0.121821,
             "latitude": 51.785111},
            {"name": "Croydon", "postcode": "CR0 4NX", "postcode_validity": True, "longitude": -0.118057,
             "latitude": 51.368721},
            {"name": "Canterbury_Sturry_Road", "postcode": "CT1 1DX", "postcode_validity": True, "longitude": 1.099587,
             "latitude": 51.291295},
            {"name": "Canterbury", "postcode": "CT1 3TQ", "postcode_validity": True, "longitude": 1.063353,
             "latitude": 51.271737},
            {"name": "Broadstairs", "postcode": "CT10 2RQ", "postcode_validity": True, "longitude": 1.398326,
             "latitude": 51.361584},
            {"name": "Dover", "postcode": "CT16 3PS", "postcode_validity": True, "longitude": 1.29854,
             "latitude": 51.153865},
            {"name": "Folkestone", "postcode": "CT19 5SY", "postcode_validity": True, "longitude": 1.166973,
             "latitude": 51.09503},
            {"name": "Crayford", "postcode": "DA1 4LD", "postcode_validity": True, "longitude": 0.181438,
             "latitude": 51.451253},
            {"name": "Gravesend", "postcode": "DA11 0DQ", "postcode_validity": True, "longitude": 0.360659,
             "latitude": 51.444994},
            {"name": "Chingford", "postcode": "E4 8JA", "postcode_validity": True, "longitude": -0.032249,
             "latitude": 51.613179},
            {"name": "Beckton", "postcode": "E6 6LG", "postcode_validity": True, "longitude": 0.070889,
             "latitude": 51.521308},
            {"name": "Enfield", "postcode": "EN1 1TH", "postcode_validity": True, "longitude": -0.054651,
             "latitude": 51.653761},
            {"name": "Waltham_Abbey", "postcode": "EN9 1BY", "postcode_validity": True, "longitude": -0.009966,
             "latitude": 51.68602},
            {"name": "Farnborough", "postcode": "GU14 7QL", "postcode_validity": True, "longitude": -0.760255,
             "latitude": 51.290186},
            {"name": "Bagshot", "postcode": "GU19 5DG", "postcode_validity": False, "longitude": None,
             "latitude": None},
            {"name": "Woking", "postcode": "GU22 8BD", "postcode_validity": True, "longitude": -0.542921,
             "latitude": 51.32359},
            {"name": "Alton", "postcode": "GU34 2QS", "postcode_validity": True, "longitude": -0.956537,
             "latitude": 51.157421},
            {"name": "Godalming", "postcode": "GU7 1DR", "postcode_validity": True, "longitude": -0.606494,
             "latitude": 51.187514},
            {"name": "Farnham", "postcode": "GU9 9QJ", "postcode_validity": True, "longitude": -0.783878,
             "latitude": 51.218514},
            {"name": "Ruislip", "postcode": "HA4 0LN", "postcode_validity": True, "longitude": -0.390474,
             "latitude": 51.555701},
            {"name": "High_Wycombe", "postcode": "HP11 1FY", "postcode_validity": True, "longitude": -0.719697,
             "latitude": 51.618643},
            {"name": "Aylesbury", "postcode": "HP20 1DH", "postcode_validity": True, "longitude": -0.805149,
             "latitude": 51.818086},
            {"name": "Hemel_Hempstead", "postcode": "HP3 9AA", "postcode_validity": True, "longitude": -0.474067,
             "latitude": 51.739299},
            {"name": "Ilford", "postcode": "IG2 6BE", "postcode_validity": True, "longitude": 0.084461,
             "latitude": 51.574762},
            {"name": "Walton_On_Thames", "postcode": "KT12 2SS", "postcode_validity": True, "longitude": -0.41812,
             "latitude": 51.387939},
            {"name": "Byfleet", "postcode": "KT14 7NP", "postcode_validity": True, "longitude": -0.477112,
             "latitude": 51.340225},
            {"name": "Luton", "postcode": "LU1 3JH", "postcode_validity": True, "longitude": -0.398002,
             "latitude": 51.87339},
            {"name": "Dunstable", "postcode": "LU5 4XZ", "postcode_validity": True, "longitude": -0.514047,
             "latitude": 51.890604},
            {"name": "Sittingbourne", "postcode": "ME10 2XD", "postcode_validity": True, "longitude": 0.735686,
             "latitude": 51.345021},
            {"name": "Maidstone", "postcode": "ME20 7TP", "postcode_validity": True, "longitude": 0.469822,
             "latitude": 51.293972},
            {"name": "Chatham", "postcode": "ME5 9SQ", "postcode_validity": True, "longitude": 0.507228,
             "latitude": 51.350979},
            {"name": "Gillingham", "postcode": "ME8 0PU", "postcode_validity": True, "longitude": 0.576371,
             "latitude": 51.367403},
            {"name": "Bletchley", "postcode": "MK1 1BN", "postcode_validity": True, "longitude": -0.724652,
             "latitude": 52.002562},
            {"name": "Buckingham", "postcode": "MK18 1TB", "postcode_validity": True, "longitude": -0.991638,
             "latitude": 51.989192},
            {"name": "Friern_Barnet", "postcode": "N11 3PW", "postcode_validity": True, "longitude": -0.143116,
             "latitude": 51.611571},
            {"name": "Camden", "postcode": "NW1 9EX", "postcode_validity": True, "longitude": -0.13693,
             "latitude": 51.543913},
            {"name": "Hendon", "postcode": "NW9 7TH", "postcode_validity": True, "longitude": -0.245101,
             "latitude": 51.580711},
            {"name": "Chichester", "postcode": "PO19 7YH", "postcode_validity": True, "longitude": -0.757297,
             "latitude": 50.841461},
            {"name": "Bognor_Regis", "postcode": "PO22 9NF", "postcode_validity": True, "longitude": -0.667151,
             "latitude": 50.798685},
            {"name": "Portsmouth", "postcode": "PO3 5LZ", "postcode_validity": True, "longitude": -1.054632,
             "latitude": 50.81583},
            {"name": "Havant", "postcode": "PO9 1ND", "postcode_validity": True, "longitude": -0.986896,
             "latitude": 50.850524},
            {"name": "Bracknell", "postcode": "RG12 1EN", "postcode_validity": True, "longitude": -0.755313,
             "latitude": 51.414577},
            {"name": "Reading", "postcode": "RG2 0HB", "postcode_validity": True, "longitude": -0.970504,
             "latitude": 51.434117},
            {"name": "Basingstoke", "postcode": "RG22 4TT", "postcode_validity": True, "longitude": -1.141485,
             "latitude": 51.233957},
            {"name": "Tilehurst", "postcode": "RG30 1PR", "postcode_validity": True, "longitude": -1.014177,
             "latitude": 51.461326},
            {"name": "Wokingham", "postcode": "RG40 2NU", "postcode_validity": True, "longitude": -0.837922,
             "latitude": 51.405767},
            {"name": "Winnersh", "postcode": "RG41 5HH", "postcode_validity": True, "longitude": -0.894323,
             "latitude": 51.435581},
            {"name": "Redhill", "postcode": "RH1 6QL", "postcode_validity": True, "longitude": -0.169423,
             "latitude": 51.235174},
            {"name": "Crawley", "postcode": "RH11 7ST", "postcode_validity": True, "longitude": -0.190845,
             "latitude": 51.134507},
            {"name": "Horsham", "postcode": "RH12 1HR", "postcode_validity": True, "longitude": -0.325105,
             "latitude": 51.061363},
            {"name": "Burgess_Hill", "postcode": "RH15 9QT", "postcode_validity": True, "longitude": -0.149078,
             "latitude": 50.950564},
            {"name": "East_Grinstead", "postcode": "RH19 1QL", "postcode_validity": True, "longitude": -0.035134,
             "latitude": 51.137408},
            {"name": "Dorking", "postcode": "RH4 1RU", "postcode_validity": True, "longitude": -0.32926,
             "latitude": 51.233309},
            {"name": "Thurrock", "postcode": "RM20 3LP", "postcode_validity": True, "longitude": 0.271413,
             "latitude": 51.485804},
            {"name": "Romford", "postcode": "RM7 0AN", "postcode_validity": True, "longitude": 0.18457,
             "latitude": 51.569209},
            {"name": "Dagenham", "postcode": "RM9 6SJ", "postcode_validity": True, "longitude": 0.145621,
             "latitude": 51.530577},
            {"name": "Old_Kent_Road", "postcode": "SE1 5BA", "postcode_validity": True, "longitude": -0.068434,
             "latitude": 51.484387},
            {"name": "Blackheath", "postcode": "SE10 8DA", "postcode_validity": True, "longitude": -0.018139,
             "latitude": 51.473071},
            {"name": "Sydenham", "postcode": "SE26 4PU", "postcode_validity": True, "longitude": -0.033935,
             "latitude": 51.429857},
            {"name": "Thamesmead", "postcode": "SE28 8RD", "postcode_validity": True, "longitude": 0.104076,
             "latitude": 51.506662},
            {"name": "Charlton", "postcode": "SE7 7TZ", "postcode_validity": True, "longitude": 0.020724,
             "latitude": 51.488666},
            {"name": "Eltham", "postcode": "SE9 5LT", "postcode_validity": True, "longitude": 0.033341,
             "latitude": 51.451065},
            {"name": "Hertford", "postcode": "SG13 7RQ", "postcode_validity": True, "longitude": -0.069212,
             "latitude": 51.797063},
            {"name": "Slough", "postcode": "SL1 4XB", "postcode_validity": True, "longitude": -0.616201,
             "latitude": 51.522666},
            {"name": "Maidenhead", "postcode": "SL6 1AY", "postcode_validity": True, "longitude": -0.717543,
             "latitude": 51.518569},
            {"name": "Southend_Victoria", "postcode": "SS1 1PA", "postcode_validity": True, "longitude": 0.705174,
             "latitude": 51.541837},
            {"name": "Basildon", "postcode": "SS13 3BY", "postcode_validity": True, "longitude": 0.505725,
             "latitude": 51.564192},
            {"name": "Basildon_Pipps_Hill", "postcode": "SS14 3AF", "postcode_validity": True, "longitude": 0.443534,
             "latitude": 51.581143},
            {"name": "Southend-on-Sea", "postcode": "SS2 6FW", "postcode_validity": True, "longitude": 0.703482,
             "latitude": 51.567778},
            {"name": "Rayleigh", "postcode": "SS67UP", "postcode_validity": True, "longitude": 0.602318,
             "latitude": 51.575831},
            {"name": "Battersea", "postcode": "SW11 3RX", "postcode_validity": True, "longitude": -0.176813,
             "latitude": 51.470125},
            {"name": "Wimbledon", "postcode": "SW17 0BW", "postcode_validity": True, "longitude": -0.185911,
             "latitude": 51.429853},
            {"name": "New_Malden", "postcode": "SW20 0JQ", "postcode_validity": True, "longitude": -0.238117,
             "latitude": 51.405065},
            {"name": "Sevenoaks", "postcode": "TN14 5EW", "postcode_validity": True, "longitude": 0.193667,
             "latitude": 51.298772},
            {"name": "Tunbridge_Wells", "postcode": "TN2 3FB", "postcode_validity": True, "longitude": 0.28795,
             "latitude": 51.155923},
            {"name": "Ashford", "postcode": "TN23 7DH", "postcode_validity": True, "longitude": 0.870721,
             "latitude": 51.135177},
            {"name": "Hastings", "postcode": "TN37 7PB", "postcode_validity": True, "longitude": 0.55329,
             "latitude": 50.887953},
            {"name": "Bexhill", "postcode": "TN40 2JS", "postcode_validity": True, "longitude": 0.501216,
             "latitude": 50.844874},
            {"name": "Feltham", "postcode": "TW13 4EX", "postcode_validity": True, "longitude": -0.412804,
             "latitude": 51.442892},
            {"name": "Brentford", "postcode": "TW8 8JW", "postcode_validity": True, "longitude": -0.314343,
             "latitude": 51.482172},
            {"name": "Richmond", "postcode": "TW9 1YB", "postcode_validity": True, "longitude": -0.288602,
             "latitude": 51.463437},
            {"name": "Hayes", "postcode": "UB4 0TU", "postcode_validity": True, "longitude": -0.397889,
             "latitude": 51.51461},
            {"name": "Greenford", "postcode": "UB6 0UW", "postcode_validity": True, "longitude": -0.34005,
             "latitude": 51.541836},
            {"name": "West_Drayton", "postcode": "UB8 2TE", "postcode_validity": True, "longitude": -0.478082,
             "latitude": 51.517916},
            {"name": "Watford", "postcode": "WD17 2SF", "postcode_validity": True, "longitude": -0.389487,
             "latitude": 51.649103},
            {"name": "Borehamwood", "postcode": "WD6 4PR", "postcode_validity": True, "longitude": -0.27754,
             "latitude": 51.65656}]
        self.assertEqual(self.middleware.postcodes_io_lookup(), expected_output)

    def test_nearest_store_lookup_correct(self):
        expected_output = [{"name": "Godalming", "postcode": "GU7 1DR", "postcode_validity": True, "longitude": -0.606494, "latitude": 51.187514, "distance_to_store_in_km": 48.07}, {"name": "Dorking", "postcode": "RH4 1RU", "postcode_validity": True, "longitude": -0.32926, "latitude": 51.233309, "distance_to_store_in_km": 40.73}, {"name": "Redhill", "postcode": "RH1 6QL", "postcode_validity": True, "longitude": -0.169423, "latitude": 51.235174, "distance_to_store_in_km": 43.06}, {"name": "Farnborough", "postcode": "GU14 7QL", "postcode_validity": True, "longitude": -0.760255, "latitude": 51.290186, "distance_to_store_in_km": 42.85}, {"name": "Woking", "postcode": "GU22 8BD", "postcode_validity": True, "longitude": -0.542921, "latitude": 51.32359, "distance_to_store_in_km": 32.33}, {"name": "Byfleet", "postcode": "KT14 7NP", "postcode_validity": True, "longitude": -0.477112, "latitude": 51.340225, "distance_to_store_in_km": 29.3}, {"name": "Croydon", "postcode": "CR0 4NX", "postcode_validity": True, "longitude": -0.118057, "latitude": 51.368721, "distance_to_store_in_km": 31.58}, {"name": "Walton_On_Thames", "postcode": "KT12 2SS", "postcode_validity": True, "longitude": -0.41812, "latitude": 51.387939, "distance_to_store_in_km": 23.42}, {"name": "Orpington", "postcode": "BR5 3RP", "postcode_validity": True, "longitude": 0.112496, "latitude": 51.392983, "distance_to_store_in_km": 41.44}, {"name": "New_Malden", "postcode": "SW20 0JQ", "postcode_validity": True, "longitude": -0.238117, "latitude": 51.405065, "distance_to_store_in_km": 23.8}, {"name": "Wokingham", "postcode": "RG40 2NU", "postcode_validity": True, "longitude": -0.837922, "latitude": 51.405767, "distance_to_store_in_km": 37.77}, {"name": "Bracknell", "postcode": "RG12 1EN", "postcode_validity": True, "longitude": -0.755313, "latitude": 51.414577, "distance_to_store_in_km": 32.59}, {"name": "Wimbledon", "postcode": "SW17 0BW", "postcode_validity": True, "longitude": -0.185911, "latitude": 51.429853, "distance_to_store_in_km": 23.31}, {"name": "Sydenham", "postcode": "SE26 4PU", "postcode_validity": True, "longitude": -0.033935, "latitude": 51.429857, "distance_to_store_in_km": 30.79}, {"name": "Reading", "postcode": "RG2 0HB", "postcode_validity": True, "longitude": -0.970504, "latitude": 51.434117, "distance_to_store_in_km": 44.24}, {"name": "Winnersh", "postcode": "RG41 5HH", "postcode_validity": True, "longitude": -0.894323, "latitude": 51.435581, "distance_to_store_in_km": 39.42}, {"name": "Feltham", "postcode": "TW13 4EX", "postcode_validity": True, "longitude": -0.412804, "latitude": 51.442892, "distance_to_store_in_km": 17.31}, {"name": "Eltham", "postcode": "SE9 5LT", "postcode_validity": True, "longitude": 0.033341, "latitude": 51.451065, "distance_to_store_in_km": 33.39}, {"name": "Crayford", "postcode": "DA1 4LD", "postcode_validity": True, "longitude": 0.181438, "latitude": 51.451253, "distance_to_store_in_km": 42.61}, {"name": "Tilehurst", "postcode": "RG30 1PR", "postcode_validity": True, "longitude": -1.014177, "latitude": 51.461326, "distance_to_store_in_km": 45.91}, {"name": "Richmond", "postcode": "TW9 1YB", "postcode_validity": True, "longitude": -0.288602, "latitude": 51.463437, "distance_to_store_in_km": 16.43}, {"name": "Battersea", "postcode": "SW11 3RX", "postcode_validity": True, "longitude": -0.176813, "latitude": 51.470125, "distance_to_store_in_km": 20.35}, {"name": "Blackheath", "postcode": "SE10 8DA", "postcode_validity": True, "longitude": -0.018139, "latitude": 51.473071, "distance_to_store_in_km": 29.08}, {"name": "Brentford", "postcode": "TW8 8JW", "postcode_validity": True, "longitude": -0.314343, "latitude": 51.482172, "distance_to_store_in_km": 13.82}, {"name": "Old_Kent_Road", "postcode": "SE1 5BA", "postcode_validity": True, "longitude": -0.068434, "latitude": 51.484387, "distance_to_store_in_km": 25.43}, {"name": "Thurrock", "postcode": "RM20 3LP", "postcode_validity": True, "longitude": 0.271413, "latitude": 51.485804, "distance_to_store_in_km": 47.25}, {"name": "Charlton", "postcode": "SE7 7TZ", "postcode_validity": True, "longitude": 0.020724, "latitude": 51.488666, "distance_to_store_in_km": 30.74}, {"name": "Thamesmead", "postcode": "SE28 8RD", "postcode_validity": True, "longitude": 0.104076, "latitude": 51.506662, "distance_to_store_in_km": 35.48}, {"name": "Hayes", "postcode": "UB4 0TU", "postcode_validity": True, "longitude": -0.397889, "latitude": 51.51461, "distance_to_store_in_km": 9.27}, {"name": "West_Drayton", "postcode": "UB8 2TE", "postcode_validity": True, "longitude": -0.478082, "latitude": 51.517916, "distance_to_store_in_km": 10.85}, {"name": "Maidenhead", "postcode": "SL6 1AY", "postcode_validity": True, "longitude": -0.717543, "latitude": 51.518569, "distance_to_store_in_km": 24.44}, {"name": "Beckton", "postcode": "E6 6LG", "postcode_validity": True, "longitude": 0.070889, "latitude": 51.521308, "distance_to_store_in_km": 32.82}, {"name": "Slough", "postcode": "SL1 4XB", "postcode_validity": True, "longitude": -0.616201, "latitude": 51.522666, "distance_to_store_in_km": 17.86}, {"name": "Dagenham", "postcode": "RM9 6SJ", "postcode_validity": True, "longitude": 0.145621, "latitude": 51.530577, "distance_to_store_in_km": 37.62}, {"name": "Greenford", "postcode": "UB6 0UW", "postcode_validity": True, "longitude": -0.34005, "latitude": 51.541836, "distance_to_store_in_km": 7.04}, {"name": "Camden", "postcode": "NW1 9EX", "postcode_validity": True, "longitude": -0.13693, "latitude": 51.543913, "distance_to_store_in_km": 18.34}, {"name": "Ruislip", "postcode": "HA4 0LN", "postcode_validity": True, "longitude": -0.390474, "latitude": 51.555701, "distance_to_store_in_km": 4.68}, {"name": "Romford", "postcode": "RM7 0AN", "postcode_validity": True, "longitude": 0.18457, "latitude": 51.569209, "distance_to_store_in_km": 39.67}, {"name": "Ilford", "postcode": "IG2 6BE", "postcode_validity": True, "longitude": 0.084461, "latitude": 51.574762, "distance_to_store_in_km": 32.72}, {"name": "Hendon", "postcode": "NW9 7TH", "postcode_validity": True, "longitude": -0.245101, "latitude": 51.580711, "distance_to_store_in_km": 10.03}, {"name": "Friern_Barnet", "postcode": "N11 3PW", "postcode_validity": True, "longitude": -0.143116, "latitude": 51.611571, "distance_to_store_in_km": 16.96}, {"name": "Chingford", "postcode": "E4 8JA", "postcode_validity": True, "longitude": -0.032249, "latitude": 51.613179, "distance_to_store_in_km": 24.61}, {"name": "High_Wycombe", "postcode": "HP11 1FY", "postcode_validity": True, "longitude": -0.719697, "latitude": 51.618643, "distance_to_store_in_km": 23.04}, {"name": "Watford", "postcode": "WD17 2SF", "postcode_validity": True, "longitude": -0.389487, "latitude": 51.649103, "distance_to_store_in_km": 5.71}, {"name": "Enfield", "postcode": "EN1 1TH", "postcode_validity": True, "longitude": -0.054651, "latitude": 51.653761, "distance_to_store_in_km": 23.82}, {"name": "Borehamwood", "postcode": "WD6 4PR", "postcode_validity": True, "longitude": -0.27754, "latitude": 51.65656, "distance_to_store_in_km": 10.03}, {"name": "Waltham_Abbey", "postcode": "EN9 1BY", "postcode_validity": True, "longitude": -0.009966, "latitude": 51.68602, "distance_to_store_in_km": 27.85}, {"name": "Hemel_Hempstead", "postcode": "HP3 9AA", "postcode_validity": True, "longitude": -0.474067, "latitude": 51.739299, "distance_to_store_in_km": 16.83}, {"name": "St_Albans", "postcode": "AL1 2RJ", "postcode_validity": True, "longitude": -0.341337, "latitude": 51.741753, "distance_to_store_in_km": 16.33}, {"name": "Hatfield", "postcode": "AL9 5JP", "postcode_validity": True, "longitude": -0.222034, "latitude": 51.776142, "distance_to_store_in_km": 22.89}, {"name": "Harlow", "postcode": "CM20 2SX", "postcode_validity": True, "longitude": 0.121821, "latitude": 51.785111, "distance_to_store_in_km": 40.84}, {"name": "Hertford", "postcode": "SG13 7RQ", "postcode_validity": True, "longitude": -0.069212, "latitude": 51.797063, "distance_to_store_in_km": 31.19}, {"name": "Aylesbury", "postcode": "HP20 1DH", "postcode_validity": True, "longitude": -0.805149, "latitude": 51.818086, "distance_to_store_in_km": 37.78}, {"name": "Luton", "postcode": "LU1 3JH", "postcode_validity": True, "longitude": -0.398002, "latitude": 51.87339, "distance_to_store_in_km": 30.66}, {"name": "Dunstable", "postcode": "LU5 4XZ", "postcode_validity": True, "longitude": -0.514047, "latitude": 51.890604, "distance_to_store_in_km": 33.71}]
        # must run postcodes_io_lookup before
        self.middleware.postcodes_io_lookup()
        self.assertEqual(self.middleware.nearest_store_lookup("HA5 3LF", 50), expected_output)

    def test_verify_stores_data_invalid_name(self):
        self.middleware.json_stores = [{"names": "incorrect_key", "postcode": "HA5 3LF"}]
        self.assertRaises(middleware.MiddlewareInternalError, self.middleware.verify_stores_data)

    def test_verify_stores_data_invalid_postcode(self):
        self.middleware.json_stores = [{"name": "correct_key", "postcodes": "invalid_key"}]
        self.assertRaises(middleware.MiddlewareInternalError, self.middleware.verify_stores_data)

    def test_import_json_stores_invalid_location(self):
        self.middleware.json_location = "non_existent.json"
        self.assertEqual(self.middleware.import_json_stores(), [])
        self.middleware.json_location = "stores-test.json"

    def test_sort_array_alphabetically_by_name_bad_stores(self):
        self.middleware.json_stores = [{"names": "incorrect_key", "postcode": "HA5 3LF"}]
        self.assertRaises(middleware.MiddlewareInputError, self.middleware.sort_array_alphabetically_by_name)

    def test_sort_array_alphabetically_by_postcode_bad_stores(self):
        self.middleware.json_stores = [{"name": "correct_key", "postcodes": "invalid_key"}]
        self.assertRaises(middleware.MiddlewareInputError, self.middleware.sort_array_alphabetically_by_postcode)

    def test_lat_long_already_fetched_postcodes_io_lookup(self):
        self.middleware.json_stores = [{"name": "Battersea", "postcode": "SW11 3RX", "postcode_validity": True, "longitude": -0.176813,"latitude": 51.470125}]
        self.assertEqual(self.middleware.postcodes_io_lookup(), self.middleware.json_stores)