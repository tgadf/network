from haversine import haversine
from timeUtils import getDateTime


################################################################################################################
#
# Generic Trip Data
#
################################################################################################################
def getInteger(tids):
    from math import isnan    
    for i in range(len(tids)):
        try:
            tids[i] = float(tids[i])
            if isnan(tids[i]):
                tids[i] = 0
        except:
            tids[i] = None
    return tids
            
def getTripGeoID(name, trip, debug=False):
    try:
        key  = [trip["Geo0{0}ID".format(name)], trip["Geo1{0}ID".format(name)]]
    except:
        if debug:
            print("Could not create trip {0}ID for {1}".format(name))
        key  = [None,None]
    return key




################################################################################################################
#
# Census Data
#
################################################################################################################
def getTripCensusData(trip):
    keys=['CBSA', 'CSA', 'County', 'MetDiv', 'Place', 'State', 'Tract', 'ZCTA']
    retval = {}
    for key in keys:
        keyval = "{0}{1}".format("Census", key.title())
        retval[keyval] = getTripGeoID(keyval, trip)
    return retval



################################################################################################################
#
# HERE Data
#
################################################################################################################
def getTripHEREData(trip):
    keys=['Attraction', 'Auto', 'Building', 'College', 'Commercial', 'Cycling', 'Entertainment', 'Fastfood', 'Fuel', 'Grocery', 'Industrial', 'Lodging', 'Medical', 'Municipal', 'Parking', 'Recreation', 'Restaurant', 'School', 'Sport', 'Transit']
    retval = {}
    for key in keys:
        keyval = "{0}{1}".format("HEREPOI", key.title())
        tids = getTripGeoID(keyval, trip)
        retval[keyval] = getInteger(tids)
    return retval



################################################################################################################
#
# Road Data
#
################################################################################################################
def getTripRoadData(trip):
    from math import isnan
    keys=['Interstate', 'Usrte', 'Staterte', 'Highway', 'MajorRd']    
    retval = {}
    for key in keys:
        keyval = "{0}{1}".format("ROADS", key)
        tids = getTripGeoID(keyval, trip)
        retval[keyval] = getInteger(tids)
    return retval



################################################################################################################
#
# OSM Data
#
################################################################################################################
def getTripOSMData(trip):
    from math import isnan
    keys=['Fuel', 'Parking', 'Bus', 'Ferry', 'Rail', 'Taxi', 'Tram', 'Buddhist', 'Christian', 'Hindu', 'Jewish', 'Muslim', 'Sikh', 'Taoist', 'Attraction', 'Auto', 'Building', 'College', 'Commercial', 'Entertainment', 'Fastfood', 'Grocery', 'Industrial', 'Lodging', 'Medical', 'Municipal', 'Public', 'Recreation', 'Religious', 'Restaurant', 'School', 'Sport']
    retval = {}
    for key in keys:
        keyval = "{0}{1}".format("OSM", key)
        tids = getTripGeoID(keyval, trip)
        retval[keyval] = getInteger(tids)
    return retval





################################################################################################################
#
# Terminal Data
#
################################################################################################################
def getTripTerminalData(trip):
    from math import isnan
    keys=['Airport', 'Amtrak']
    retval = {}
    for key in keys:
        keyval = "{0}{1}".format("Terminals", key)
        tids = getTripGeoID(keyval, trip)
        retval[keyval] = getInteger(tids)
    return retval



################################################################################################################
#
# POI Data
#
################################################################################################################
def getTripPOIData(trip):
    from math import isnan
    keys=['POIVisits', 'POIUniqueVisits']
    keys=['UniqueVisits']
    retval = {}
    for key in keys:
        keyval = "{0}{1}".format("POI", key)
        tids = getTripGeoID(keyval, trip)
        retval[keyval] = getInteger(tids)
    return retval




################################################################################################################
#
# Trip Details
#
################################################################################################################
def getTripPOIID(trip):
    print(trip)
    #print("POI --> ",trip['geo0'], trip['geo0'][:7])    
    coms = gc.getClusterCoM(geoID)
    #print(coms)
    print("POI --> ",trip['geo0'], trip['geo0'][:7])
    try:
        key  = [trip["geo0"][:7],trip["geo1"][:7]]
    except:
        x = (trip["lat0"], trip["long0"])
        g0 = getGeo(x)
        x = (trip["lat1"], trip["long1"])
        g1 = getGeo(x)
        key  = [g0,g1]
    print(key)
    return key


def getTripKey(trip):
    try:
        key  = [trip["geo0"],trip["geo1"]]
    except:
        trip['geo0'] = getGeo([trip["lat0"], trip["long0"]], 8)
        trip['geo1'] = getGeo([trip["lat1"], trip["long1"]], 8)
        key  = [trip["geo0"],trip["geo1"]]
        #raise ValueError("Could not create trip key for {0}".format(trip))
        #key  = [None,None]
    return key


def getTripHeading(trip):
    try:
        headings = [trip["heading0"], trip["heading1"]]
    except:
        raise ValueError("Could not create trip headings for {0}".format(trip))
        headings = None
    return headings


def getTripDrivingDistance(trip):
    try:
        distance = trip["total_miles"]
    except:
        raise ValueError("Could not get trip distance for {0}".format(trip))
        distance = None
    return distance


def getTripGeoDistance(trip):
    distance  = haversine((trip["lat0"], trip["long0"]), (trip["lat1"], trip["long1"])) # returns in km
    return distance


def getTripDistanceRatio(drivingDistance, geoDistance):
    try:
        ratio = geoDistance/drivingDistance
    except:
        ratio = None
    return ratio

def getTripStartTime(trip, raiseError=True):
    try:
        startTime = getDateTime(trip['Start'])
    except:
        try:
            startTime = getDateTime(trip['start'])
        except:
            if raiseError:
                raise ValueError("Could not get trip start for {0}".format(trip))
            startTime = None
    return startTime


def getTripEndTime(trip, raiseError=False):
    try:
        endTime = getDateTime(trip['End'])
    except:
        try:
            endTime = getDateTime(trip['end'])
        except:
            if raiseError:
                raise ValueError("Could not get trip end for {0}".format(trip))
            endTime = None
    return endTime


def getTripWeekend(trip):
    startTime = getTripStartTime(trip)
    if startTime is None:
        return None
    try:
        isWeekend = int(startTime.isoweekday() >= 6)
    except:
        raise ValueError("Could not get weekend info for {0}".format(trip))
    return isWeekend


def getTripDuration(trip, raiseError=False):
    try:
        startTime = getTripStartTime(trip)
        endTime = getTripEndTime(trip)
        duration  = (endTime - startTime).seconds
    except:
        try:
            duration  = trip['Duration']
        except:
            try:
                duration  = trip['duration']
            except:
                if raiseError:
                    raise ValueError("Could not get trip duration for {0}".format(trip))
                duration = None
    return duration