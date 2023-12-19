# Version 2, going to attempt with RPi and LCD
# Made 12/17/2023

from FlightRadar24.api import FlightRadar24API

# ZONE - Creates a zone to look for flights inside. tl is top left corner of box, br is bottom right.
ZONE = {"tl_y": 29.754081, "tl_x": -82.511874, "br_y": 29.535365, "br_x": -82.147178 }

# Time to wait in between switching info screens (seconds)
DELAY = 3.5