import requests
from flask import Flask
# from flask_app import create_app


class Flight(object):
    def __init__(self, flight_json, country, originplace, destinationplace, carriers, places, airports):
        # self.country = country
        originplace = originplace.upper()
        destinationplace = destinationplace.upper()
        self.country = "US"
        self.originplace = originplace
        print(self.originplace)
        # originplace
        self.destinationplace = destinationplace
        self.minprice = flight_json["MinPrice"]
        self.outboundpartialdate = flight_json["OutboundLeg"]["DepartureDate"][:-9]
        self.carrierid = flight_json["OutboundLeg"]["CarrierIds"][0]
        self.origincity = places[originplace]
        self.originairport = airports[originplace]
        self.destinationcity = places[destinationplace]
        self.destinationairport = airports[destinationplace]
        self.carrier = carriers[flight_json["OutboundLeg"]["CarrierIds"][0]]


class FlightClient(object):
    def __init__(self, api_key):
        self.sess = requests.Session()
        self.headers = {
            'x-rapidapi-key': f"{api_key}",
            'x-rapidapi-host': "skyscanner-skyscanner-flight-search-v1.p.rapidapi.com"
        }
        self.base_url = f"https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/browseroutes/v1.0/"

    def search(self, country, originplace, destinationplace, outboundpartialdate):
        """
        Searches the API for the supplied search_string, and returns
        a list of Media objects if the search was successful, or the error response
        if the search failed.

        Only use this method if the user is using the search bar on the website.
        """

        search_url = f"US/USD/en-US/{originplace}-sky/{destinationplace}-sky/{outboundpartialdate}"

        final_url = search_url[:-15]
        # print(type(search_url))
        # print("final url ", final_url)
        # print(self.headers)

        url = self.base_url + final_url
        resp = requests.request("GET", url, headers=self.headers)

        if resp.status_code != 200:
            raise ValueError(
                "Search request failed; Please make sure that all your inputs are correct"
            )

        data = resp.json()

        quote_results_json = data["Quotes"]
        carriers = {}
        for carrier in data["Carriers"]:
            id = carrier["CarrierId"]
            carriers[id] = carrier["Name"]

        places = {}
        for place in data["Places"]:
            target = place["SkyscannerCode"]
            places[target] = place["CityName"]

        airports = {}
        for airport in data["Places"]:
            target = airport["SkyscannerCode"]
            airports[target] = airport["Name"]

        result = []

        # We may have more results than are first displayed
        for item_json in quote_results_json:
            result.append(Flight(item_json, country,
                                 originplace, destinationplace, carriers, places, airports))

        return result


## -- Example usage -- ###
if __name__ == "__main__":
    import os

    app = Flask(__name__)

    headers = {
        'x-rapidapi-key': "f511e4e457mshbb220780db8fe47p1fd209jsnd4a2de0f8ae8",
        'x-rapidapi-host': "skyscanner-skyscanner-flight-search-v1.p.rapidapi.com"
    }

    client = FlightClient("f511e4e457mshbb220780db8fe47p1fd209jsnd4a2de0f8ae8")

    flights = client.search("US", "IAD", "ICN", "2020-12-10")

    for flight in flights:
        print(flight.country + " " + flight.originplace + " -> " + flight.destinationplace + ": "
              "$" + str(flight.minprice) + flight.origincity + " -> " + flight.destinationcity + " " + flight.carrier)
