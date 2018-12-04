# coding: utf-8

import pandas as pd
from timeUtils import clock, elapsed, getTimeSuffix, getDateTime, addDays, printDateTime, getFirstLastDay
from pandasUtils import castDateTime, castInt64, cutDataFrameByDate, convertToDate, isSeries, isDataFrame, getColData
import geohash


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
    if 'Start' not in trips.columns:
        return None
        
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
        overnightStays[startGeo] += 0
        overnightStays[endGeo] += 0
            
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
    if 'Start' not in trips.columns:
        return None
        
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
    if 'Start' not in trips.columns:
        return None
        
    dvData = {}
    from pandas import to_datetime
    trips['Date'] = to_datetime(trips['Start']).dt.date
    for tripno, trip in trips.iterrows():
        startGeo = trip['geo0']
        endGeo   = trip['geo1']
        if dvData.get(startGeo) is None:
            dvData[startGeo] = set()
        if dvData.get(endGeo) is None:
            dvData[endGeo] = set()
            

        sData = trip['Date']
        dvData[startGeo].add(sData)
        dvData[endGeo].add(sData)
        
    dvData = {k: len(v) for k,v in dvData.items()}
    return dvData


#############################################################################################################################
# Get Common Location
#############################################################################################################################
def getCommonLocation(trips, debug=False):
    startGeo = trips["geo0"]
    endGeo   = trips["geo1"]
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
def getHome(dailyVisits, overnightStays, dwellTimes, commonLocation, debug=False, verydebug=False):
    if debug:
        print("Deriving Home From Daily Visits, Overnight Stays, Dwell Times, and Common Location")
        
    if all([dailyVisits, overnightStays, dwellTimes]):
        ## Possible clusters come from overnight stays
        possibleDTCls = [k for k,v in dwellTimes.items() if v > 0]
        if debug:
            print("There are {0} possible home clusters".format(len(dwellTimes)))
            if verydebug:
                print("  CLs: {0}".format(possibleDTCls))
                
        ## Require at least two overnight stays for home
        possibleDTCls = [k for k,v in dwellTimes.items() if v >= 2]
        if debug:
            print("There are {0} possible home clusters with at least two hours of dwell time".format(len(possibleDTCls)))
            if verydebug:
                print("  CLs: {0}".format(possibleDTCls))

        ## Require at least ten daily visits for home
        possibleDVCls = [k for k,v in dailyVisits.items() if v >= 10]
        if debug:
            print("There are {0} possible home clusters with at least ten daily visits".format(len(possibleDVCls)))
            if verydebug:
                print("  CLs: {0}".format(possibleDVCls))

        ## Rank remaining cluster dwell times
        dts = {}
        for cl,dt in overnightStays.items():
            if cl in possibleDTCls and cl in possibleDVCls and dt > 0:
                dts[cl] = dt
            
        from pandas import Series
        dts = Series(dts)
        dts.sort_values(ascending=False, inplace=True)
        if debug:
            print("There are {0} possible home clusters with overnight stays".format(dts.count()))
            if verydebug:
                print("  CLs: {0}".format(possibleDVCls))

        if verydebug:
            print("  Ranked List:")
            print("{0}".format(dts))
               
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
        retval = {"GeoID": homeCl, "Vtx": None, "Ratio": homeRatio, "Days": dailyVisits[homeCl], "Possible": possibleHomes}
    
    else:
        from pandas import Series
        dts = Series(commonLocation)
        dts.sort_values(ascending=False, inplace=True)
        
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
            print("Selecting {0} as the home cluster with the most common location.".format(homeCl))
        retval = {"GeoID": homeCl, "Vtx": None, "Ratio": homeRatio, "Days": None, "Possible": 1}
   
    
    return retval