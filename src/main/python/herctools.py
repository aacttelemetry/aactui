import math

def pressure_to_height(pressure, places=2):
    '''
    Converts pressure in pascals (as sent by the Fitbit) to height in meters.
    Uses the (inverse of the) formula found here: https://www.math24.net/barometric-formula/
    '''
    return round(math.log((float(pressure)/1000)/101.325)/-0.00012,places)