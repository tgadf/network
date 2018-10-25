
# coding: utf-8

# # Visualize Networks

# In[78]:

import pandas as pd
import igraph as ig
from timeUtils import clock, elapsed, getTimeSuffix, getDateTime, addDays, printDateTime, getFirstLastDay
from pandasUtils import castDateTime, castInt64, castFloat64, cutDataFrameByDate, convertToDate, isSeries, isDataFrame, getColData
from networkTrips import getTripsFromPandas
import geohash
from haversine import haversine
from geoClustering import geoClusters, geoCluster

from pyspark.sql.window import Window
from pyspark.sql.functions import avg, sum, udf, countDistinct, col, datediff, max, min, stddev, count, skewness, asc
from pyspark.sql.functions import kurtosis, corr, hour, date_format, desc, sqrt, weekofyear, month, dayofyear, pow
from pyspark.sql.types import IntegerType, BooleanType, DateType, StringType, LongType, Row
import pyspark.sql.types as T


def rows_to_pandas_df(rows):
    """Converts an iterable of rows to a pandas dataframe"""
    return pd.DataFrame([row.asDict() for row in rows])

def pandas_df_to_rows(df):
    """Converts a pandas dataframe to an iterable of rows"""
    for index, *values in df.itertuples():
        yield Row(**{k:v for k, v in zip(df.columns.values, values)})
        
        
def computeNetworkFeatures(dn, numFeats, useExternal=True, debug=False):
    from modelio import loadJoblib
    if debug is True:
        startnf, cmtnf = clock("Getting network features")
    from networkFeatures import networkFeatures
    nf = networkFeatures(network=dn, expectedFeatures=numFeats)
        
    ## Fill Data
    nf.fillInternalData(debug)
    nf.fillExternalNetworkData(debug=debug)
    nf.fillExternalGeospatialData(debug=debug)
    
    ## Fill Census Data
    nf.fillExternalCensusData(debug=debug)
    
    ## Fill Features/Attrs
    nf.fillVertexFeatureData(debug=debug)
    nf.fillEdgeFeatureData(debug=debug)

    ## Vertices
    nf.setVertexExternalDataCounts(debug=debug)    
    nf.setVertexFractions(debug=debug)
    nf.setVertexRatios(debug=debug)
    #nf.setVertexFeatures(debug=debug)
    nf.setVertexCorrelations(debug=debug)    

    ## Edges    
    nf.setEdgeExternalDataCounts(debug=debug)
    nf.setEdgeFractions(debug=debug)
    nf.setEdgeRatios(debug=debug)
    #nf.setEdgeFeatures(debug=debug)
    nf.setEdgeCorrelations(debug=debug)

    ## Global
    nf.setGlobalNetworkFeatures(debug=debug)
    #nf.setCliqueStructure(debug=debug)
    nf.setCommunityStructure(debug=debug)
    nf.setDyadCensus(debug=debug)
    nf.setArticulationStructure(debug=debug)

    ## Home
    nf.setHomeFeatures(debug=debug)

    if debug is True:
        elapsed(startnf, cmtnf)
        
    return nf

            
        
def extract_features(df,prec=7,collectMetrics=True,debug=False,calcFeatures=True,
                     returnNetwork=False,useExternal=True,reqGood=True,numFeats=3067):
    """Takes in a Pandas dataframe containing all of the trip-gps data
    from a single device and extracts relevant features from it
    
    Input:
    input_df: (Pandas DataFrame) The input, gps-point level dataframe
    containing raw data
    Output:
    output_df: (Pandas DataFrame) The output, day level dataframe
    containing extracted features
    """
    import pandas as pd
    import geohash
    from numpy import amax, nan
    
    
    ## Make sure everything has the correct type
    df['lat0']  = castFloat64(df['lat0'])
    df['long0'] = castFloat64(df['long0'])
    df['lat1']  = castFloat64(df['lat1'])
    df['long1'] = castFloat64(df['long1'])
    df['total_miles'] = castFloat64(df['total_miles'])
    df = df.replace('nan', nan)
    
    
    
    ## Make sure everything is sorted by time
    if debug is True:
        start = clock("Sorting data by time")
    df.sort_values(by="Start", ascending=True, inplace=True)
    if debug is True:
        elapsed(start, "Done sorting data by time")
    
    devices = list(df['device'].unique())
    current_device = str(devices[0])
    if len(devices) > 1:
        raise ValueError("There are [{0}] multiple devices".format(devices))
    

    #######################################################################################
    # Cluster Geo Data (Lat, Long)
    #######################################################################################
    points         = df[["lat0", "long0"]]
    points.columns = ["lat", "long"]
    pnts           = df[["lat1", "long1"]]
    pnts.columns   = ["lat", "long"]    
    points         = points.append(pnts)
    
    
    
    #######################################################################################
    # Create Clusters
    #######################################################################################
    gc   = geoClusters(device=current_device, points=points, distMax=300, debug=debug)
    tmp  = gc.getGeoDataFrame()
    tmp2 = gc.getGeoCntsSeries()    
    gc.findClusters(seedMin=2, debug=debug)
    if debug:
        print("Found {0} clusters using {1} cells and {2} counts".format(gc.getNClusters(), gc.getNCells(), gc.getNCounts()))

    
    
    #######################################################################################
    # Set Nearest Clusters
    #######################################################################################
    if debug:
        start, cmt = clock("Finding Nearest Clusters for Start of Trips")
    geoResults = df[['lat0', 'long0']].apply(gc.getNearestClusters, axis=1).values
    df["geo0"] = [x[0] for x in geoResults]
    if debug:
        elapsed(start, cmt)
        start, cmt = clock("Finding Nearest Clusters for End of Trips")
    geoResults = df[['lat1', 'long1']].apply(gc.getNearestClusters, axis=1).values
    df["geo1"] = [x[0] for x in geoResults]    
    if debug:
        elapsed(start, cmt)
        

        
    #######################################################################################
    # Network Trips
    #######################################################################################
    if debug is True:
        start, cmt = clock("Getting trips for network")
    trips   = getTripsFromPandas(df, gc, prec=7, debug=debug, collectMetrics=collectMetrics, requireGood=reqGood)
    if debug is True:
        elapsed(start, cmt)
        
        
        
    #######################################################################################
    # Driver Network
    #######################################################################################
    if debug is True:
        startdn, cmtdn = clock("Creating driver network")        
    from driverNetwork import driverNetwork
    dn = driverNetwork(trips)
    dn.createNetwork(debug=debug)
    dn.setVertexOrder(debug=debug)
    dn.setEdgeOrder(debug=debug)
    dn.setNetworkAttributes(debug=debug)
    if debug is True:
        elapsed(startdn, cmtdn)
        
        
    #######################################################################################
    # Network Features
    #######################################################################################
    if calcFeatures is True:
        nf = computeNetworkFeatures(dn, numFeats, useExternal, debug)
    else:
        nf = None

    if returnNetwork is True or nf is None:
        return nf, dn, trips
    else:
        df = nf.getFeatureDataFrame(debug=debug) 
        return df



def makeNetworkDir(device, rm=False):
    from os import mkdir
    from os.path import exists, isdir
    dirname = "plots/{0}".format(device)
    if isdir(dirname) and rm is True:
        import shutil
        shutil.rmtree(dirname)
        
    
    try:
        mkdir(dirname)
    except:
        if rm is True:
            raise ValueError("Could not make ".format(dirname))
    return False


# In[68]:
    

def distHash(gcode1, gcode2):
    """
    distHash(gcode1, gcode2)
    
    inputs: gcode1 (geohash), gcode2 (geohash)
    outputs: distance (km)
    """
    pnt1 = geohash.decode_exactly(gcode1)[:2]
    pnt2 = geohash.decode_exactly(gcode2)[:2]
    dist = haversine(pnt1, pnt2)
    return dist


def createNetworkGraph(trips):
    """
    createNetworkGraph():
    
    Inputs:
      > trips: a dictionary of vertices, edges, and metrics produced by getTripsFromPandas()
      
    Outputs:
      > igraph object
    """
    import igraph
    stats = {}
        
    g = ig.Graph()
    try:
        g.add_vertices(len(trips['vertexNameToID']))
        stats['Vertices'] = len(trips['vertexNameToID'])
    except:
        print("Could not add vertices to graph!")
        return None
    
    try:
        edgList = list(trips['edgesVtxID'].keys())
        stats['Edges'] = len(edgList)
        g.add_edges(edgList)
    except:
        print("Could not add edges to graph!")
        return None

    stats['Trips']    = 0
    stats['MaxTrip'] = {"Trip": None, "Weight": 0}
    for idx, e in enumerate(g.es):
        try:
            e["weight"] = trips['edgesVtxID'][e.tuple]
        except:
            e['weight'] = 1

        stats['Trips'] += e['weight']
        if e['weight'] > stats['MaxTrip']["Weight"]:
            stats['MaxTrip'] = {"Trip": e.tuple, "Weight": e['weight']}
            
    vertex_id, vertex = getVertex(g, 0)
    stats['CentralVtx'] = {"ID": vertex_id}
            
    return g, stats


def getNetworkGraph(df, gc, prec=7, debug=False, collectMetrics=True):
    trips   = getTripsFromPandas(df, gc, prec=7, debug=debug, collectMetrics=collectMetrics)
    g,stats = createNetworkGraph(trips)   
    return g, trips, stats