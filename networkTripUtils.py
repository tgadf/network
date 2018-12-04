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
        key  = [trip["Geo0{0}".format(name)], trip["Geo1{0}".format(name)]]
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
    keys=['CBSA', 'CSA', 'MetDiv', 'Place', 'CouSub']
    retval = {}
    for key in keys:
        keyval = "{0}{1}".format("CENSUS", key.title())
        retval[keyval] = getTripGeoID(keyval, trip)
        
    ## Add County and State
    key = 'County'
    keyval = "{0}{1}".format("CENSUS", key.title())
    cousub = retval['CENSUSCousub']
    try:
        retval[keyval] = [int(str(x)[:5]) for x in cousub]
    except:
        retval[keyval] = [0, 0]
        
    key = 'State'
    keyval = "{0}{1}".format("CENSUS", key.title())
    cousub = retval['CENSUSCousub']
    try:
        retval[keyval] = [int(str(x)[:2]) for x in cousub]
    except:
        retval[keyval] = [0, 0]
    
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
        keyval = "{0}{1}".format("POIHERE", key.title())
        tids = getTripGeoID(keyval, trip)
        retval[keyval] = getInteger(tids)
    return retval



################################################################################################################
#
# Road Data
#
################################################################################################################
def getTripRailData(trip):
    from math import isnan
    keys=['Rail']
    retval = {}
    for key in keys:
        keyval = "{0}{1}".format("RAIL", key)
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
    keys=['Interstate', 'Usrte', 'Staterte', 'Highway', 'MajorRd', 'Road']
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
    
    keys=['Beach', 'CaveEntrance', 'Cliff', 'Glacier', 'Peak', 'Spring', 'Tree', 'Volcano', '4101', '4111', '4113', '4112', '4121', '4141', '4132', '4103', 'City', 'County', 'Hamlet', 'Island', 'Locality', 'Region', 'Suburb', 'Town', 'Village', '1003', '1004', '1050', '1001', '1002', '1041', '1010', 'FarmPlace', '1020', '1030', 'NationalCapital', 'Allotments', 'Cemetery', 'Commercial', 'Farm', 'Forest', 'Grass', 'Heath', 'Industrial', 'Meadow', 'Military', 'NatureReserve', 'Orchard', 'Park', 'Quarry', 'RecreationGround', 'Residential', 'Retail', 'Scrub', 'Vineyard', 'Canal', 'Dock', 'Drain', 'GlacierWater', 'Reservoir', 'River', 'Stream', 'Water', 'Wetland', 'Fuel', 'Parking', 'Buddhist', 'Christian', 'Hindu', 'Jewish', 'Muslim', 'Sikh', 'Taoist', 'Bus', 'Ferry', 'Rail', 'Taxi', 'Tram', 'Attraction', 'Auto', 'Building', 'College', 'Business', 'Entertainment', 'Fastfood', 'Grocery', 'Manufacturing', 'Lodging', 'Medical', 'Municipal', 'Public', 'Recreation', 'Religious', 'Restaurant', 'School', 'Sport']
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
        keyval = "{0}{1}".format("TERMINALS", key)
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
        keyval = "{0}{1}".format("POIASDW", key)
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
        key  = [str(trip["geo0"]),str(trip["geo1"])]
    except:
        trip['geo0'] = getGeo([trip["lat0"], trip["long0"]], 8)
        trip['geo1'] = getGeo([trip["lat1"], trip["long1"]], 8)
        key  = [str(trip["geo0"]),str(trip["geo1"])]
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