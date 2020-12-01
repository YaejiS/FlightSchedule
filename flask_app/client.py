import requests


class Flight(object):
    def __init__(self, flight_json, country, originplace, destinationplace):
        self.country = country
        self.originplace = originplace
        self.destinationplace = destinationplace
        self.minprice = flight_json["MinPrice"]
        self.departuredate = flight_json["OutboundLeg"]["DepartureDate"]


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

        search_url = f"{country}/USD/en-US/{originplace}-sky/{destinationplace}-sky/{outboundpartialdate}"

        url = self.base_url + search_url
        resp = requests.request("GET", url, headers=self.headers)

        if resp.status_code != 200:
            raise ValueError(
                "Search request failed; make sure your API key is correct and authorized"
            )

        data = resp.json()

        quote_results_json = data["Quotes"]

        result = []

        # We may have more results than are first displayed
        for item_json in quote_results_json:
            result.append(Flight(item_json, country,
                                 originplace, destinationplace))

        return result


## -- Example usage -- ###
if __name__ == "__main__":
    import os

    headers = {
        'x-rapidapi-key': "f511e4e457mshbb220780db8fe47p1fd209jsnd4a2de0f8ae8",
        'x-rapidapi-host': "skyscanner-skyscanner-flight-search-v1.p.rapidapi.com"
    }

    client = FlightClient("f511e4e457mshbb220780db8fe47p1fd209jsnd4a2de0f8ae8")

    flights = client.search("US", "SFO", "ORD", "2020-12-01")

    for flight in flights:
        print(flight.country + " " + flight.originplace + " -> " + flight.destinationplace + ": "
              "$" + str(flight.minprice))
