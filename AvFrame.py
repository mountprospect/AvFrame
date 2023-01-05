#1-5-2023

from FlightRadar24.api import FlightRadar24API

# ZONE - Creates a zone to look for flights inside. tl is top left corner of box, br is bottom right.
ZONE = {"tl_y": 29.754081, "tl_x": -82.511874, "br_y": 29.535365, "br_x": -82.147178 }

fr = FlightRadar24API()
airports = fr.get_airports()
airlines = fr.get_airlines()
flights = fr.get_flights()

# Declare bounds using ZONE defined earlier
bounds = fr.get_bounds(ZONE)

# Find flights within zone
flightsInZone = fr.get_flights(bounds = bounds)

print(flightsInZone)
