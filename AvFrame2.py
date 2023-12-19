# Version 2, going to attempt with RPi and LCD
# Made 12/17/2023

from FlightRadar24.api import FlightRadar24API
import PySimpleGUI as gui

# ZONE - Creates a zone to look for flights inside. tl is top left corner of box, br is bottom right.
ZONE = {"tl_y": 29.754081, "tl_x": -82.511874, "br_y": 29.535365, "br_x": -82.147178 }

# Time to wait in between switching info screens (seconds)
DELAY = 3.5

fr = FlightRadar24API()
# allAirports = fr.get_airports()
# allAirlines = fr.get_airlines()
# allFlights = fr.get_flights()

# Declare bounds using ZONE defined earlier
bounds = fr.get_bounds(ZONE)

# Find flights within zone
flightsInZone = fr.get_flights(bounds = bounds)

if (len(flightsInZone) > 0):
    for flight in flightsInZone:
        details = fr.get_flight_details(flight.id)
        flight.set_flight_details(details)
        
        callsign = flight.callsign.upper()
        altitude = flight.altitude
        model = flight.aircraft_model
        code = flight.aircraft_code
        origin = flight.origin_airport_icao.upper()
        destination = flight.destination_airport_icao.upper()
        gs = flight.ground_speed
        airline = flight.airline_name
        status = flight.status_text

        print(airline)
        
else:
    print("No flights in zone!")

# GUI Code

gui.theme('BluePurple')
layout = [ [gui.Text("Test")],
           [gui.Text("Test2")] ]

window = gui.Window("Title", layout)

while True:
    event, values = window.read()
    if event == gui.WIN_CLOSED or event == 'Cancel':
        break
    print("Entered: ", values[0])
    
window.close()