from FlightRadar24 import FlightRadar24API
import json
fr_api = FlightRadar24API(...)

bounds = fr_api.get_bounds_by_point(52.567967, 13.282644, 200000)
flights = fr_api.get_flights(bounds = bounds)
print(flights)
#flights = fr_api.get_flights()
flight_strings = [str(flight) for flight in flights]

# Writing list contents as a single line in a text file
with open('out_getFlights.json', 'w') as file:
    file.write('\n'.join(flight_strings))

flight_radar_api = FlightRadar24API()
flight_details = flight_radar_api.get_flight_details("A306")
# Writing list contents as a single line in a text file
print(flight_details)
with open('out_getFlightsDetails.json', 'w') as file:
    file.write('\n'.join(flight_details))
