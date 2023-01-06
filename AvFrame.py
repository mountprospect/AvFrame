#1-5-2023

from FlightRadar24.api import FlightRadar24API
from PythonMETAR import *

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

# Checks if any flights exist in zone
if (len(flightsInZone) > 0):
# Gets details of  flight for printing
    for flight in flightsInZone:
        details = fr.get_flight_details(flight.id)
        flight.set_flight_details(details)
        callsign = flight.callsign.upper()
        alt = flight.altitude
        model = flight.aircraft_model
        code = flight.aircraft_code
        origin = flight.origin_airport_icao.upper()
        destination = flight.destination_airport_icao.upper()

        print(callsign + "|" +  str(alt) + "|" + model + "|" + code + "|" + origin + "|" + destination)
        print("\n")

else:
    print("No flights in zone")
    
    
# METAR Reports for airports of interest
wxTPA = Metar('KTPA')
wxGNV = Metar('KGNV')
wxORD = Metar('KORD')

# Get properties for all airports of interest
wxTPAProperties = wxTPA.getAll()
wxGNVProperties = wxGNV.getAll()
wxORDProperties = wxORD.getAll()
#print(wxTPAProperties.keys())

# Get cloud properties 
tpaCld = wxTPAProperties["cloud"]
ordCld = wxORDProperties["cloud"]
gnvCld = wxGNVProperties["cloud"]

# TODO: PARSE METAR TEXT FOR VIS

# Function to return flight rules as string
def getFlightRules(cldID): # Use second param for vis
    # TODO : Add visibility parameter
    if (not cldID):
        flightRules = "VFR"
    else:
        for i in range(len(cldID)):
            code = cldID[i]["code"]
            base = cldID[i]["altitude"]
            vis = 0
            if (code == "BKN" or code == "OVC"):
                if (base < 500):
                    flightRules = "LIFR"
                elif (base >= 500 and base < 1000):
                    flightRules = "IFR"
                elif (base >= 1000 and base <= 3000):
                    flightRules = "MVFR"
                elif (base > 3000):
                    flightRules = "VFR"
                else:
                    flightRules = "UNKN"
            elif (code == "CLR"):
                flightRules = "VFR"
            else:
                flightRules = "UNKN"
    return flightRules

print(wxTPA)
print(wxORD)
print(wxGNV)
print("TPA: " + getFlightRules(tpaCld) + "\n" + "ORD: " + getFlightRules(ordCld) + "\n" + "GNV: " + getFlightRules(gnvCld))

