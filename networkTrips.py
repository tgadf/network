# coding: utf-8

from timeUtils import clock, elapsed, getTimeSuffix, getDateTime, addDays, printDateTime, getFirstLastDay
from pandasUtils import castDateTime, castInt64, cutDataFrameByDate, convertToDate, isSeries, isDataFrame, getColData
from haversine import haversine
from networkTimeUtils import getDailyVisits, getDwellTimes, getOvernightStays, getHome, getCommonLocation
from networkTripUtils import getInteger, getTripGeoID, getTripCensusData, getTripHEREData, getTripRoadData
from networkTripUtils import getTripOSMData, getTripTerminalData, getTripPOIData, getTripPOIID, getTripKey
from networkTripUtils import getTripHeading, getTripDrivingDistance, getTripGeoDistance, getTripDistanceRatio
from networkTripUtils import getTripStartTime, getTripEndTime, getTripWeekend, getTripDuration, getTripRailData



def organizeTrips(df, gc, prec=7, requireGood=True, debug=False, showTrips=False, saveTrips=False, collectMetrics=True):
    """
    organizeTrips():
    
    Notes: Geohashs are already set for this data. If this is called from network.py then the 'geo' values
            are actually the cluster IDs.
    
    Inputs:
      > df: a pandas dataframe
      > gc: geocluster class object
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
    commonLocation = getCommonLocation(df, debug=False)
    homeMetrics    = getHome(dailyVisits, overnightStays, dwellTimes, commonLocation, debug=debug, verydebug=False)
    
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
            try:
                startDate = startTime.date()
                endDate   = endTime.date()
            except:
                startDate = None
                endDate = None
        else:
            try:
                startDate = min(startDate, startTime.date())
                endDate   = max(endDate, endTime.date())
            except:
                startDate = None
                endDate = None
                

        
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
        extData['Census']    = getTripCensusData(trip)
        
        # Get HERE information
        extData['HEREPOI']   = getTripHEREData(trip)
        
        # Get HERE information
        extData['OSM']       = getTripOSMData(trip)
        
        # Get Road information
        extData['Roads']     = getTripRoadData(trip)
        
        # Get Rail information
        extData['Rail']     = getTripRailData(trip)
        
        # Get Terminal information
        extData['Terminals'] = getTripTerminalData(trip)
        
        # Get Road information
        extData['POI']       = getTripPOIData(trip)
 
        if False:
            for k,v in extData.items():
                print("")
                print(k)
                print(v)
            print("")
            print(list(trip.index))
            1/0
    
        ###################################################################################################################
        ## vertex metrics
        ###################################################################################################################  
        vtxIDs=[]
        geoIDs=[]
        for clID, geoID in enumerate(tripKey):
            
            if geoIDtovtxID.get(geoID) is None:                
                vtxID = len(geoIDtovtxID)
                geoIDtovtxID[geoID] = vtxID
                vtxIDtogeoID[vtxID] = geoID
            else:
                vtxID = geoIDtovtxID[geoID]
            geoIDs.append(geoID)
            vtxIDs.append(vtxID)

            if vtxMetrics.get(geoID) is None:                
                vtxMetrics[geoID] = {"DayOfWeek": [], "DrivingDistance": [], "GeoDistanceRatio": [], "N": 0, "First": startTime.date(), "Last": endTime.date()}
                vtxMetrics[geoID]["CoM"]            = gc.getClusterCoM(geoID)
                vtxMetrics[geoID]["Radius"]         = gc.getClusterRadius(geoID)
                vtxMetrics[geoID]["Cells"]          = gc.getClusterCells(geoID)
                vtxMetrics[geoID]["Quantiles"]      = gc.getClusterQuantiles(geoID)
                vtxMetrics[geoID]["Geohashs"]       = gc.getClusterCellNames(geoID)
                try:
                    vtxMetrics[geoID]["DwellTime"]      = dwellTimes.get(geoID)
                except:
                    vtxMetrics[geoID]["DwellTime"]      = None
                try:
                    vtxMetrics[geoID]["DailyVisits"]    = dailyVisits.get(geoID)
                except:
                    vtxMetrics[geoID]["DailyVisits"]    = None
                try:
                    vtxMetrics[geoID]["OvernightStays"] = overnightStays.get(geoID)
                except:
                    vtxMetrics[geoID]["OvernightStays"] = None
                try:
                    vtxMetrics[geoID]["IsHome"]         = int(geoID == homeMetrics["GeoID"])
                except:
                    vtxMetrics[geoID]["IsHome"]         = None
                    
                
            ## Fill running counters
            vtxMetrics[geoID]["DayOfWeek"].append(isWeekend)
            vtxMetrics[geoID]["DrivingDistance"].append(drivingDistance)
            vtxMetrics[geoID]["GeoDistanceRatio"].append(geoDistanceRatio)
            vtxMetrics[geoID]["N"] += 1
            vtxMetrics[geoID]["First"] = min(startTime.date(), vtxMetrics[geoID]["First"])
            vtxMetrics[geoID]["Last"]  = max(endTime.date(), vtxMetrics[geoID]["Last"])

            ## Fill external data
            for extKey,extVal in extData.items():
                vtxMetrics[geoID][extKey] = {}
                for key, value in extVal.items():
                    if vtxMetrics[geoID][extKey].get(key) is None:
                        vtxMetrics[geoID][extKey][key] = Counter()
                    if geoID == geo0:
                        vtxMetrics[geoID][extKey][key][value[0]] += 1
                    elif geoID == geo1:
                        vtxMetrics[geoID][extKey][key][value[1]] += 1
                    else:
                        raise ValueError("Not sure how this happened!!!! {0}".format(tripKey))


    
        ###################################################################################################################
        ## edge metrics
        ################################################################################################################### 
        edgeGeoID = tripKey
        edgeID    = tuple(sorted(geoIDs))
        vtx0      = geoIDs[0]
        vtx1      = geoIDs[1]
        
        if edgesVtxID.get(edgeID) is None:
            edgesVtxID[edgeID] = 0
        edgesVtxID[edgeID] += 1
        
        if edgeMetrics.get(edgeID) is None:
            edgeMetrics[edgeID] = {"Duration": [], "First": startTime.date(), "Last": endTime.date(), "DayOfWeek": [], "ITA": [],
                                   "GeoDistance": [],"DrivingDistance": [],"GeoDistanceRatio": [],
                                   "Weight": 0, "Geos": vtxIDs, "Locations": [vtxMetrics[vtx0]["CoM"], vtxMetrics[vtx1]["CoM"]]}
            
        ## Fill running counters
        edgeMetrics[edgeID]["Duration"].append(duration)
        edgeMetrics[edgeID]["DrivingDistance"].append(drivingDistance)
        edgeMetrics[edgeID]["GeoDistanceRatio"].append(geoDistanceRatio)
        edgeMetrics[edgeID]["GeoDistance"].append(geoDistance)
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
           
        try:
            vtxMetrics[vtxID]["FractionalVisits"]  = vtxMetrics[vtxID]["DailyVisits"] / float(totalDays)
        except:
            vtxMetrics[vtxID]["FractionalVisits"]  = None
            
        #print(vtxID,'\t',vtxMetrics[vtxID]["DailyVisits"] / float(totalDays),'\t',vtxMetrics[vtxID]["FractionalVisits"])
        
        
    ##########################################################################################################################
    ## Set Home
    ##########################################################################################################################
    homeGeoID = homeMetrics["GeoID"]
    try:
        homeMetrics["Location"] = gc.getClusterCoM(homeGeoID)
    except:
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
        dist     = Series(edgeMetricData["GeoDistance"])
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