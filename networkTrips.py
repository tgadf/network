# coding: utf-8

import pandas as pd
import igraph as ig
from timeUtils import clock, elapsed, getTimeSuffix, getDateTime, addDays, printDateTime, getFirstLastDay
from pandasUtils import castDateTime, castInt64, cutDataFrameByDate, convertToDate, isSeries, isDataFrame, getColData
from sparkUtils import isSparkDataFrame
try:
    import pygeohash as geohash
except:
    import geohash
from haversine import haversine
from geoClustering import geoClusters, geoCluster


#############################################################################################################################
# Geohash
#############################################################################################################################
def getGeo(x):
    prec=7
    try:
        lat    = x[0]
        long   = x[1]
        retval = geohash.encode(lat, long, precision=prec)
    except:
        retval = None
    return retval



#############################################################################################################################
# Overnight Stays
#############################################################################################################################
def checkStartingLocation(startGeo, prevGeo, gc, debug=False): 
    if not all([startGeo, prevGeo]):
        return False
    
    if startGeo != prevGeo:
        comPrevGeo  = gc.getClusterCoM(prevGeo)
        comStartGeo = gc.getClusterCoM(startGeo)
        dist        = gc.getDist(comPrevGeo, comStartGeo)
        if dist > 500:
            return False
    
    return True
            
    

def getOvernightStays(trips, gc, debug=False):
    from pandas import Series
    overnightStays = {}
    trips = trips.sort_values(by="Start", ascending=True, inplace=False)
    trips['start']    = convertToDate(castDateTime(trips['Start']))
    trips['end']      = convertToDate(castDateTime(trips['End']))
    trips['startGeo'] = trips["geo0"]
    trips['endGeo']   = trips["geo1"]

    from collections import Counter
    overnightStays = Counter()
    
    prevGeo = None
    prevEnd = None
    for tripno, trip in trips.iterrows():
        startGeo = trip['startGeo']
        endGeo   = trip['endGeo']
            
        if debug:
            print("\nTripNo: {0} -----> {1} , {2}, {3}, {4}".format(tripno, startGeo, endGeo, trip['start'], trip['end']))

        if not checkStartingLocation(startGeo, prevGeo, gc, debug):
            prevGeo = endGeo
            prevEnd = trip['end']
            if debug:
                print("  Last Geo and Start Geo are too far apart or one is not recognized. Will not use this data.")
            continue
            
        dTime = trip['start'] - prevEnd
        days  = dTime.days
        if days >= 1:
            overnightStays[startGeo] += 1
        if debug:
            print("  Overnight Stays at {0} is {1} w/ Days = {2}".format(startGeo, dTime, days))
                    
        prevGeo = endGeo
        prevEnd = trip['end']

    retval = {"Global": len(overnightStays)}
    for geo,cnts in overnightStays.most_common():
        retval[geo] = cnts
        
    return retval



#############################################################################################################################
# Dwell Time
#############################################################################################################################
def getDwellTimes(trips, gc, debug=False):
    from pandas import Series
    dwellTimes = {}
    trips = trips.sort_values(by="Start", ascending=True, inplace=False)
    trips['start']    = castDateTime(trips['Start'])
    trips['end']      = castDateTime(trips['End'])
    trips['startGeo'] = trips["geo0"]
    trips['endGeo']   = trips["geo1"]

    dwellData = []
    
    prevGeo = None
    prevEnd = None
    for tripno, trip in trips.iterrows():
        startGeo = trip['startGeo']
        endGeo   = trip['endGeo']
            
        if debug:
            print("\nTripNo: {0} -----> {1} , {2}, {3}, {4}".format(tripno, startGeo, endGeo, trip['start'], trip['end']))

        if not checkStartingLocation(startGeo, prevGeo, gc, debug):
            prevGeo = endGeo
            prevEnd = trip['end']
            if debug:
                print("  Last Geo and Start Geo are too far apart or one is not recognized. Will not use this data.")
            continue
            
        dTime = trip['start'] - prevEnd
        hours = dTime.seconds/3600
        if hours < 24:
            if dwellTimes.get(startGeo) is None:
                dwellTimes[startGeo] = []            
            dwellTimes[startGeo].append(hours)
            dwellData.append(hours)

            if debug:
                print("  Dwell Time at {0} is {1} w/ Hours = {2}".format(startGeo, dTime, hours))
            
        prevGeo = endGeo
        prevEnd = trip['end']

    retval = {"Global": Series(dwellData).mean()}
    sigval = {}
    for geo in dwellTimes.keys():
        if len(dwellTimes[geo]) >= 1:
            dts = Series(dwellTimes[geo])
            dwellTimes[geo] = [dts.size, dts.mean(), dts.std()]
            retval[geo]     = dwellTimes[geo][1]
        else:
            dwellTimes[geo] = [None, None, None]
            retval[geo]     = None
    
    return retval


#############################################################################################################################
# Get Daily Visits
#############################################################################################################################
def getDailyVisits(trips, debug=False):
    trips['start'] = castDateTime(trips['Start'])
    trips['end']   = castDateTime(trips['End'])
    trips['date']  = convertToDate(trips['start'])
    dmm = trips.groupby('date').agg({'start': min, 'end': max})
    dfStart = dmm.merge(trips, on=['start'])
    dfEnd   = dmm.merge(trips, on=['end'])
    
    startGeo = dfStart["geo0"]
    endGeo   = dfEnd["geo1"]
    from pandas import concat
    try:
        visits = concat([startGeo, endGeo], axis=0).reset_index(drop=True).value_counts()
        visits = dict(visits)
    except:
        visits = None
        raise ValueError("Could not create ordered list of geos for last place/first place")

    retval = visits
    return retval


#############################################################################################################################
# Guess Home
#############################################################################################################################
def getHome(dailyVisits, overnightStays, dwellTimes, debug=False):
    if debug:
        print("Deriving Home From Daily Visits, Overnight Stays, and Dwell Times")
    
    ## Possible clusters come from overnight stays
    if debug:
        print("There are {0} possible home clusters".format(len(overnightStays)))
    
    ## Require at least two overnight stays for home
    possibleOSCls = [k for k,v in overnightStays.items() if v >= 2]
    if debug:
        print("There are {0} possible home clusters with at least two overnight stays".format(len(possibleOSCls)))
        
    ## Require at least ten daily visits for home
    possibleDVCls = [k for k,v in dailyVisits.items() if v >= 10]
    if debug:
        print("There are {0} possible home clusters with at least ten daily visits".format(len(possibleDVCls)))
        
    ## Rank remaining cluster dwell times
    dts = {}
    for cl,dt in dwellTimes.items():
        if cl in possibleOSCls and cl in possibleDVCls:
            dts[cl] = dt
            
    from pandas import Series
    dts = Series(dts)
    dts.sort_values(ascending=False, inplace=True)
    if debug:
        print("There are {0} possible home clusters with active dwell times".format(dts.count()))
        
    possibleHomes  = dts.count()
    try:
        homeCl     = dts.index[0]
    except:
        homeCl     = None
        
    try:
        nextCl     = dts.index[1]
        homeRatio  = round(dts[homeCl]/dts[nextCl],1)
    except:
        homeRatio  = None

    if debug:
        print("Selecting {0} as the home cluster with significance {1}, {2} overnight stays, {3} daily visits, and {4} dwell time hours.".format(homeCl, homeRatio, overnightStays[homeCl], dailyVisits[homeCl], round(dwellTimes[homeCl],1)))
    retval = {"Geo": homeCl, "Vtx": None, "Ratio": homeRatio, "Days": dailyVisits[homeCl], "Possible": possibleHomes}
    return retval




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

def getTripStartTime(trip):
    try:
        startTime = getDateTime(trip['Start'])
    except:
        try:
            startTime = getDateTime(trip['start'])
        except:
            raise ValueError("Could not get trip start for {0}".format(trip))
            startTime = None
    return startTime


def getTripEndTime(trip):
    try:
        endTime = getDateTime(trip['End'])
    except:
        try:
            endTime = getDateTime(trip['end'])
        except:
            raise ValueError("Could not get trip end for {0}".format(trip))
            endTime = None
    return endTime


def getTripWeekend(trip):
    startTime = getTripStartTime(trip)
    try:
        isWeekend = int(startTime.isoweekday() >= 6)
    except:
        raise ValueError("Could not get weekend info for {0}".format(trip))
    return isWeekend


def getTripDuration(trip):
    try:
        startTime = getTripStartTime(trip)
        endTime = getTripEndTime(trip)
        duration  = (endTime - startTime).seconds
    except:
        try:
            duration  = trip['Duration']
        except:
            raise ValueError("Could not get trip duration for {0}".format(trip))
            duration = None
    return duration



def getTripsFromPandas(df, gc, prec=7, requireGood=True, debug=False, showTrips=False, saveTrips=False, collectMetrics=True):
    """
    getTripsFromPandas():
    
    Notes: Geohashs are already set for this data. If this is called from network.py then the 'geo' values
            are actually the cluster IDs.
    
    Inputs:
      > df: a pandas dataframe
      > prec: geohash precision (7 by default)
      > debug (False)
      > showTrips (False): show all trips (noisy)
      > collectMetrics (True): required if computing features
    Outputs:
      > dictionary with device, vertices, names, and edges
    """
    try:
        current_device = str(df['device'].unique()[0])
    except:
        current_device = None

    from pandas import Series
    from collections import Counter
    
    if debug:
        print("All Trips:     {0}".format(df.shape[0]))
        
    geoIDtovtxID = {}
    vtxIDtogeoID = {}
    edgesVtxID   = {}

    kmconv = 1.60934
    
    edgeMetrics = {}
    vtxMetrics  = {}
    
    ## Vertex Metrics leading to Home Assignment
    dailyVisits    = getDailyVisits(df, debug=False)
    overnightStays = getOvernightStays(df, gc, debug=False)
    dwellTimes     = getDwellTimes(df, gc, debug=False)
    homeMetrics    = getHome(dailyVisits, overnightStays, dwellTimes, debug=debug)
    
    goodTrips = 0
    failedDuration = 0
    failedDistance = 0
    
    #trips = group.sort_values(by='Start').drop(['device', 'Start', 'End', 'heading0', 'heading1'], axis=1).reset_index(drop=True)
    try:
        trips = df.drop(['device'], axis=1).reset_index(drop=True)
    except:
        trips = df.reset_index(drop=True)
        
    if saveTrips is True:
        try:
            from os import remove
            remove("{0}_trips.csv".format(current_device))
        except:
            pass
        

    startDate = None
    endDate   = None
    interval  = None
    maxTrip   = 0.0

    if debug:
        start = clock("Looping over trips")
    ntrips = trips.shape[0]
    for tripno, trip in trips.iterrows():
        
        if debug:
            if tripno % 50000 == 0 or tripno == 10000 or tripno == 1000 or tripno == 100:
                print("Processing trip {0}/{1}".format(tripno, ntrips))
            
        ##
        ## Basic Trip Identifier
        ##
        tripKey  = getTripKey(trip)
        geo0     = tripKey[0]
        geo1     = tripKey[1]
        
            
        ##
        ## Internal Data
        ##
        
        # Get weekend information
        duration = getTripDuration(trip)
        
        # Get weekend information
        isWeekend = getTripWeekend(trip)
        
        # Get haversine distance
        geoDistance = getTripGeoDistance(trip)
        
        # Get driving distance
        drivingDistance = getTripDrivingDistance(trip)*kmconv
        
        # Get distance ratio        
        geoDistanceRatio = getTripDistanceRatio(drivingDistance, geoDistance)
        
        # Start/End Time
        startTime = getTripStartTime(trip)
        endTime   = getTripEndTime(trip)

        # Track First/Last
        if not all([startDate,endDate]):
            startDate = startTime.date()
            endDate   = endTime.date()
        else:
            startDate = min(startDate, startTime.date())
            endDate   = max(endDate, endTime.date())

        
        ##
        ## Check if trip is good
        ##
        if requireGood is True:
            if duration is not None:
                if duration < 60:
                    failedDuration += 1
                    continue                   
            if drivingDistance is not None:
                if drivingDistance < 0.1:
                    failedDistance += 1
                    continue
                
                
        # Augment good trips counter
        goodTrips += 1
        
        
        
        ###################################################################################################################
        ## Fill external data
        ###################################################################################################################
        extData = {}
        # Get Census information
        extData['Census']   = getTripCensusData(trip)
        
        # Get HERE information
        extData['HEREPOI']  = getTripHEREData(trip)
        
        # Get HERE information
        extData['OSM']      = getTripOSMData(trip)
        
        # Get Road information
        extData['Road']     = getTripRoadData(trip)
        
        # Get Terminal information
        extData['Terminal'] = getTripTerminalData(trip)
        
        # Get Road information
        extData['POI']      = getTripPOIData(trip)

       
    
        ###################################################################################################################
        ## vertex metrics
        ###################################################################################################################  
        vtxIDs=[]
        for clID, geoID in enumerate(tripKey):
            
            if geoIDtovtxID.get(geoID) is None:                
                vtxID = len(geoIDtovtxID)
                geoIDtovtxID[geoID] = vtxID
                vtxIDtogeoID[vtxID] = geoID
            else:
                vtxID = geoIDtovtxID[geoID]
            vtxIDs.append(vtxID)

            if vtxMetrics.get(vtxID) is None:
                vtxMetrics[vtxID] = {"DayOfWeek": [], "DrivingDistance": [], "GeoDistanceRatio": [], "N": 0, "First": startTime.date(), "Last": endTime.date()}
                vtxMetrics[vtxID]["CoM"]            = gc.getClusterCoM(geoID)
                vtxMetrics[vtxID]["POI"]            = getGeo(vtxMetrics[vtxID]["CoM"])
                vtxMetrics[vtxID]["Geo"]            = getGeo(vtxMetrics[vtxID]["CoM"])
                vtxMetrics[vtxID]["Radius"]         = gc.getClusterRadius(geoID)
                vtxMetrics[vtxID]["Cells"]          = gc.getClusterCells(geoID)
                vtxMetrics[vtxID]["Quantiles"]      = gc.getClusterQuantiles(geoID)
                vtxMetrics[vtxID]["Geohashs"]       = gc.getClusterCellNames(geoID)              
                vtxMetrics[vtxID]["DwellTime"]      = dwellTimes.get(geoID)
                vtxMetrics[vtxID]["DailyVisits"]    = dailyVisits.get(geoID)
                vtxMetrics[vtxID]["OvernightStays"] = overnightStays.get(geoID)
                
            ## Fill running counters
            vtxMetrics[vtxID]["DayOfWeek"].append(isWeekend)
            vtxMetrics[vtxID]["DrivingDistance"].append(drivingDistance)
            vtxMetrics[vtxID]["GeoDistanceRatio"].append(geoDistanceRatio)
            vtxMetrics[vtxID]["N"] += 1
            vtxMetrics[vtxID]["First"] = min(startTime.date(), vtxMetrics[vtxID]["First"])
            vtxMetrics[vtxID]["Last"]  = max(endTime.date(), vtxMetrics[vtxID]["Last"])

            ## Fill external data
            for extKey,extVal in extData.items():
                vtxMetrics[vtxID][extKey] = {}
                for key, value in extVal.items():
                    if vtxMetrics[vtxID][extKey].get(key) is None:
                        vtxMetrics[vtxID][extKey][key] = Counter()
                    if geoID == geo0:
                        vtxMetrics[vtxID][extKey][key][value[0]] += 1
                    elif geoID == geo1:
                        vtxMetrics[vtxID][extKey][key][value[1]] += 1
                    else:
                        raise ValueError("Not sure how this happened!!!! {0}".format(tripKey))


    
        ###################################################################################################################
        ## edge metrics
        ################################################################################################################### 
        edgeGeoID = tripKey
        edgeID    = tuple(sorted(vtxIDs))
        vtx0      = vtxIDs[0]
        vtx1      = vtxIDs[1]
        
        if edgesVtxID.get(edgeID) is None:
            edgesVtxID[edgeID] = 0
        edgesVtxID[edgeID] += 1
        
        if edgeMetrics.get(edgeID) is None:
            edgeMetrics[edgeID] = {"Duration": [], "First": startTime.date(), "Last": endTime.date(), "DayOfWeek": [], "ITA": [],
                                   "Distance": [],"DrivingDistance": [],"GeoDistanceRatio": [],
                                   "Weight": 0, "Geos": [geo0, geo1], "Locations": [vtxMetrics[vtx0]["CoM"], vtxMetrics[vtx1]["CoM"]]}
            
        ## Fill running counters
        edgeMetrics[edgeID]["Duration"].append(duration)
        edgeMetrics[edgeID]["DrivingDistance"].append(drivingDistance)
        edgeMetrics[edgeID]["GeoDistanceRatio"].append(geoDistanceRatio)
        edgeMetrics[edgeID]["Distance"].append(geoDistance)
        edgeMetrics[edgeID]["DayOfWeek"].append(isWeekend)
        edgeMetrics[edgeID]["ITA"].append(startTime.date())
        edgeMetrics[edgeID]["First"] = min(startTime.date(), edgeMetrics[edgeID]["First"])
        edgeMetrics[edgeID]["Last"]  = max(endTime.date(), edgeMetrics[edgeID]["Last"])
        edgeMetrics[edgeID]["Weight"] += 1
        
        
        if showTrips is True:
            print("Trip {0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}".format(tripno,geo0,vtx1,geo1,vtx1,duration,distance))

        if saveTrips is True:
            print("{0},{1},{2},{3},{4},{5},{6},{7},{8}".format(tripno,geo0,geo1,trip["lat0"], trip["long0"],trip["lat1"], trip["long1"], duration, distance), file=open("{0}_trips.csv".format(current_device), "a"))        
            

    if debug:
        elapsed(start, "Finished looping over trips")
    ##########################################################################################################################
    ## Done with trip loop
    ##########################################################################################################################
            
        
    ##########################################################################################################################
    ## global metrics
    ##########################################################################################################################
    totalDays = (endDate - startDate).days + 1
        

    ##########################################################################################################################
    ## summarize vtxMetrics
    ##########################################################################################################################
    for vtxID,vtxMetricData in vtxMetrics.items():
        day     = Series(vtxMetricData["DayOfWeek"])
        day_std = day.std()
        day_avg = day.mean()
        vtxMetrics[vtxID]["DayOfWeek"] = {"Avg": day_avg, "Std": day_std}
        distance     = Series(vtxMetricData["DrivingDistance"])
        distance_std = distance.std()
        distance_avg = distance.mean()
        vtxMetrics[vtxID]["DrivingDistance"] = {"Avg": distance_std, "Std": distance_avg}
        ratio     = Series(vtxMetricData["GeoDistanceRatio"])
        ratio_std = distance.std()
        ratio_avg = distance.mean()
        vtxMetrics[vtxID]["GeoDistanceRatio"] = {"Avg": ratio_std, "Std": ratio_avg}
        vtxMetrics[vtxID]["Interval"]  = (vtxMetrics[vtxID]["Last"] - vtxMetrics[vtxID]["First"]).days + 1
        try:
            vtxMetrics[vtxID]["FractionalActive"]  = vtxMetrics[vtxID]["Interval"] / float(totalDays)
        except:
            vtxMetrics[vtxID]["FractionalActive"]  = None
            
        
        
    ##########################################################################################################################
    ## Set Home
    ##########################################################################################################################
    homeCl = homeMetrics["Geo"]
    try:
        homeMetrics["Vtx"] = geoIDtovtxID[homeCl]
        homeMetrics["Location"] = gc.getClusterCoM(homeCl)
    except:
        homeMetrics["Vtx"] = None
        homeMetrics["Location"] = [None, None]
            

    ##########################################################################################################################
    ## summarize edgeMetrics
    ###########################################################################################################################
    for edgeID,edgeMetricData in edgeMetrics.items():
        day     = Series(edgeMetricData["DayOfWeek"])
        day_std = day.std()
        day_avg = day.mean()
        edgeMetrics[edgeID]["DayOfWeek"] = {"Avg": day_avg, "Std": day_std}
        dur     = Series(edgeMetricData["Duration"])
        dur_std = day.std()
        dur_avg = day.mean()
        edgeMetrics[edgeID]["Duration"] = {"Avg": dur_avg, "Std": dur_std}
        dist     = Series(edgeMetricData["Distance"])
        dist_std = dist.std()
        dist_avg = dist.mean()
        edgeMetrics[edgeID]["GeoDistance"] = {"Avg": dist_avg, "Std": dist_std}
        dist     = Series(edgeMetricData["DrivingDistance"])
        dist_std = dist.std()
        dist_avg = dist.mean()
        edgeMetrics[edgeID]["DrivingDistance"] = {"Avg": dist_avg, "Std": dist_std}
        ratio     = Series(edgeMetricData["GeoDistanceRatio"])
        ratio_std = dist.std()
        ratio_avg = dist.mean()
        edgeMetrics[edgeID]["GeoDistanceRatio"] = {"Avg": ratio_avg, "Std": ratio_std}
        ita     = sorted(edgeMetricData["ITA"])
        itas    = []
        for i in range(1, len(ita)):
            itas.append((ita[i]-ita[i-1]).days)
        ita_avg = 0
        ita_std = 0
        if len(itas) > 1:
            itas = Series(itas)
            ita_avg = itas.mean()
            ita_std = itas.std()
        edgeMetrics[edgeID]["ITA"] = {"Avg": ita_avg, "Std": ita_std}
        edgeMetrics[edgeID]["Interval"] = (edgeMetrics[edgeID]["Last"] - edgeMetrics[edgeID]["First"]).days + 1
        try:
            edgeMetrics[edgeID]["FractionalActive"]  = edgeMetrics[edgeID]["Interval"] / float(totalDays)
        except:
            edgeMetrics[edgeID]["FractionalActive"]  = None
        
        
        
    if debug:
        print("Good Trips:            {0}".format(goodTrips))
        print("  Failed Duration Req: {0}".format(failedDuration))
        print("  Failed Distance Req: {0}".format(failedDistance))
        
    retval = {"device": current_device, "prec": prec, "vertexNameToID": geoIDtovtxID, "edgesVtxID": edgesVtxID, "vertexIDToName": vtxIDtogeoID, "activeDays": totalDays,
              "edgeMetrics": edgeMetrics, "vertexMetrics": vtxMetrics, "homeMetrics": homeMetrics}

    return retval


def getDeviceDir():
    import os
    gpspath = "/home/tgadf/astro_research_data/futuremiles/gpsData"
    mypath  = "/home/tgadf/pol"
    if os.access(gpspath, os.W_OK):
        return gpspath
    if os.access(mypath, os.W_OK):
        return mypath
    else:
        raise ValueError("Can not write to any directory!")
        return None

def loadDeviceTrips(name):
    from modelio import loadJoblib
    from os.path import exists, join
    filename = join(getDeviceDir(), "{0}.p".format(name))
    if exists(filename):
        pdDataFilter = loadJoblib(filename=filename)
        return pdDataFilter
    else:
        print("Could not find {0}".format(filename))
        return None
    
    
def saveDeviceTrips(spData, touse=None, name="df", savePandas=True):
    from os.path import join
    if not isSparkDataFrame(spData):
        print("spData is not a Spark DataFrame!")
        return None,None
    
    if touse is not None:
        start = clock("Subselecting {0} Devices".format(len(touse)))
        print("Saving these devices: {0}...".format(touse[:50]))
        use_devs = "','".join([str(x) for x in touse])
        use_devs = "('"+use_devs+"')"
        spDataFilter = spData.filter('device in '+use_devs)
        print("There are {0} entries in the table".format(spDataFilter.count()))
    else:
        start = clock("Not subselecting any devices")
        spDataFilter = spData
        
    if savePandas is True:
        start1 = clock("Converting to Pandas")
        pdDataFilter = spDataFilter.toPandas()
        elapsed(start1, "Converted to Pandas")
        print("Pandas DataFrame is {0}".format(pdDataFilter.shape))

        from modelio import saveJoblib
        filename = join(getDeviceDir(), "{0}.p".format(name))
        print("Saving {0}".format(filename))
        saveJoblib(pdDataFilter, filename=filename, compress=True)
    else:
        pdDataFilter = None

    elapsed(start, "Got Subselection of Devices")
    
    return spDataFilter, pdDataFilter