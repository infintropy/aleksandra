import os
import sys

import logging

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

COLORS = {  "red"       : (165, 66, 61),
            "orange"    : (194, 115, 59),
            "yellow"    : (226, 184, 67),
            "olive"     : (192, 201, 81),
            "green"     : (87, 178, 98),
            "teal"      : (75, 206, 192),
            "blue"      : (78, 131, 168),
            "violet"    : (99, 72, 143),
            "purple"    : (136, 75, 147),
            "pink"      : (161, 65, 112)
}

def icon(name):
    ics = os.listdir( os.path.join( ROOT_DIR, "icons" )   )
    request = "%s.png" %name
    if request in ics:
        return os.path.join( ROOT_DIR, "icons", request )
