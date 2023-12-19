#1-5-2023

from FlightRadar24.api import FlightRadar24API
from PythonMETAR import *
from Adafruit_CharLCD import Adafruit_CharLCD
from time import sleep
import RPi.GPIO as GPIO

# ZONE - Creates a zone to look for flights inside. tl is top left corner of box, br is bottom right.
ZONE = {"tl_y": 29.754081, "tl_x": -82.511874, "br_y": 29.535365, "br_x": -82.147178 }

# Time to wait in between switching info screens (seconds)
DELAY = 3.5

# Counts how many times button has been pressed to toggle modes
counter = 0;

# GPIO Setup
GPIO.setmode(GPIO.BCM)
redPin = 12
bluePin = 20
greenPin = 16
GPIO.setup(redPin, GPIO.OUT)
GPIO.setup(greenPin, GPIO.OUT)
GPIO.setup(bluePin, GPIO.OUT)




# Declaring the LCD
lcd = Adafruit_CharLCD (rs = 26, en = 19, d4 = 13, d5 = 6, d6 = 5, d7 = 21, cols = 16, lines = 2)



fr = FlightRadar24API()
airports = fr.get_airports()
airlines = fr.get_airlines()
flights = fr.get_flights()

# Declare bounds using ZONE defined earlier
bounds = fr.get_bounds(ZONE)

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

def updateWx():
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

# RGB LED Functions
def ledOff():
    GPIO.output(redPin, GPIO.HIGH)
    GPIO.output(greenPin, GPIO.HIGH)
    GPIO.output(bluePin, GPIO.HIGH)
    
def ledRed():
    GPIO.output(redPin, GPIO.LOW)
    GPIO.output(greenPin, GPIO.HIGH)
    GPIO.output(bluePin, GPIO.HIGH)
    
def ledGreen():
    GPIO.output(redPin, GPIO.HIGH)
    GPIO.output(greenPin, GPIO.LOW)
    GPIO.output(bluePin, GPIO.HIGH)
    
def ledBlue():
    GPIO.output(redPin, GPIO.HIGH)
    GPIO.output(greenPin, GPIO.HIGH)
    GPIO.output(bluePin, GPIO.LOW)
    
def ledPink():
    GPIO.output(redPin, GPIO.LOW)
    GPIO.output(greenPin, GPIO.HIGH)
    GPIO.output(bluePin, GPIO.LOW)
    
# Function to change led color based on wx conditions
def changeLEDColor(flightCat):
    if (flightCat == "VFR"):
        ledGreen()
    elif (flightCat == "MVFR"):
        ledBlue()
    elif (flightCat == "IFR"):
        ledRed()
    elif (flightCat == "LIFR"):
        ledPink()
    else:
        ledOff()

# Turn off LED at start
ledOff()
ledBlue()
lcd.clear()

while (counter == 0):

    # Find flights within zone
    flightsInZone = fr.get_flights(bounds = bounds)
    
    # Checks if any flights exist in zone
    if (len(flightsInZone) > 0):
    # Gets details of  flight for printing
        for flight in flightsInZone:
            
            lcd.clear()
            
            details = fr.get_flight_details(flight.id)
            flight.set_flight_details(details)
            callsign = flight.callsign.upper()
            alt = flight.altitude
            if (alt <=0):
                continue
            model = flight.aircraft_model
            code = flight.aircraft_code
            origin = flight.origin_airport_icao.upper()
            destination = flight.destination_airport_icao.upper()
            gs = flight.ground_speed
            airline = flight.airline_name
            status = flight.status_text

            
            #print(callsign + "|" +  str(alt) + "|" + model + "|" + code + "|" + origin + "|" + destination)
            #print("\n" + str(gs) + "|" + airline + "|" + status)
            
            # Print first two screens of information
            lcd.message(callsign + "   " + code + "\n")
            lcd.message(str(gs) + " KT " + str(alt) + " FT\n")
            sleep(DELAY)
            lcd.clear()
            lcd.message(status + "\n")
            lcd.message(origin + " > " + destination)
            sleep(DELAY)
            lcd.clear()

            # Print airline and model info, scrolling if necessary
            if (len(model) > 16 or len(airline) > 16):
                diff = max(len(model), len(airline)) - 16
                for x in range (0, diff):
                    # TODO: FIX BUG WHERE SHORTER LINE JUST SHOWS TEST FROM LONGER LINE AFTER IT IS DONE SCROLLING for bottom line
                    lcd.message(airline + "\n")
                    lcd.message(model + "\n")
                    sleep(0.75)
                    lcd.move_left()      
            else:
                lcd.message(airline + "\n")
                lcd.message(model)
            sleep(DELAY)
            

    else:
        lcd.message("No Flights\nIn Zone")
        #print("No flights in zone")
        # Sleep so don't keep pollingserver
        sleep(20)

    # Get the current flight rules from wx update and set LED to that color
    updateWx()
    lcd.clear()
    changeLEDColor(getFlightRules(tpaCld))
    lcd.message("KTPA:   " + getFlightRules(tpaCld))
    sleep(5)
    lcd.clear()
    changeLEDColor(getFlightRules(ordCld))
    lcd.message("KORD:   " + getFlightRules(ordCld))
    sleep(5)
    lcd.clear()
    changeLEDColor(getFlightRules(tpaCld))
    lcd.message("KGNV:   " + getFlightRules(gnvCld))
    sleep(5)
    lcd.clear()
#         
#     lcd.clear()
#     changeLEDColor(getFlightRules(ordCld))
#     scrollVal = len(wxORD) - 16
#     for x in range (0, scrollVal):
#         lcd.message(str(wxORD))
#         sleep(0.75)
#         lcd.move_left()
#         
#     lcd.clear()
#     changeLEDColor(getFlightRules(gnvCld))
#     scrollVal = len(wxGNV) - 16
#     for x in range (0, scrollVal):
#         lcd.message(str(wxGNV))
#         sleep(0.75)
#         lcd.move_left()
'''
print(wxTPA)
print(wxORD)
print(wxGNV)
print("TPA: " + getFlightRules(tpaCld) + "\n" + "ORD: " + getFlightRules(ordCld) + "\n" + "GNV: " + getFlightRules(gnvCld))
'''
