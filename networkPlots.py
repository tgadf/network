
# coding: utf-8

# # Visualize Networks

# In[78]:

import pandas as pd
import igraph as ig
from timeUtils import clock, elapsed, getTimeSuffix, getDateTime, addDays, printDateTime, getFirstLastDay
from pandasUtils import castDateTime, castInt64, cutDataFrameByDate, convertToDate, isSeries, isDataFrame, getColData
from network import makeNetworkDir, distHash
#import geohash
import pygeohash as geohash
from haversine import haversine
from vertexData import vertex
from edgeData import edge
from networkCategories import categories

def getLoc(ghash):
    loc = geohash.decode_exactly(ghash)[:2]
    loc = [round(x, 4) for x in loc]
    return loc


def getVertexViews(dn, vtxmetrics, homeMetrics, metric='HubScore'):
    from numpy import tanh, amax
    from pandas import Series
    from seaborn import cubehelix_palette
    from seaborn import color_palette, light_palette
    
    g = dn.getNetwork()

    if metric == "HubScore":
        vertexData           = Series(g.hub_score())
    elif metric == "Centrality":
        vertexData           = Series(g.centrality())
    elif metric == "Degree":
        vertexData           = Series(g.degree())
    else:
        raise ValueError("metric {0} was not recognized".format(metric))
            
    qvals   = vertexData.quantile([0, 0.687, 0.955, 0.997, 1])

    cols  = cubehelix_palette(n_colors=7, start=2.8, rot=.1)
    #cols  = color_palette("OrRd", 7)

    #cols  = cubehelix_palette(7)
    vcols = Series(vertexData.shape[0]*[0])
    for i in range(1, len(qvals)):
        idx = (vertexData <= qvals.iloc[i]) & (vertexData > qvals.iloc[i-1])
        vcols[idx] = i-1
    vcols = [cols[i] for i in vcols.values]
    
    vtx0ID = dn.getVertexID(0)
    vcols[vtx0ID] = cols[5]
    if metric == "HubScore":
        vsize = [amax([30*x,1]) for x in vertexData]
    else:
        vsize = [30*tanh(x/(0.5*vertexData.max())) for x in vertexData]
        
    
    vshape = ['circle' for i in range(len(vsize))]
    for v in g.vs:
        vtxID  = v.index
        vertex = dn.vertices[vtxID]
        try:
            if vertex.getAttrDataByKey("POI") != "Normal":
                vshape[vtxID] = 'triangle-down'
        except:
            pass
            
    homeID = homeMetrics['Vtx']
    vshape[homeID] = 'rectangle'
    vsize[homeID] = max(10, vsize[homeID])
    
    return vcols, vsize, vshape


def getEdgeViews(dn, edgemetrics):    
    
    from numpy import tanh, amax, linspace, power, log1p, log10, tanh
    from pandas import Series
    from seaborn import color_palette, light_palette
    from seaborn import cubehelix_palette, hls_palette

    g = dn.getNetwork()
    edgeData  = Series(g.es['weight'])
    nEdges    = edgeData.shape[0]
    if nEdges <= 0:
        return None, None
    
    minmaxWeight = [0.0, 2.5]
    print("Number of Edges: {0}".format(nEdges))
    nRange=5
    if nEdges > 100000:
        minmaxWeight[1] = 2
        nRange=6
        weightSize = [power(x,11) for x in linspace(minmaxWeight[0], minmaxWeight[1], nRange)]
    elif nEdges > 50000:
        minmaxWeight[1] = 2
        weightSize = [power(x,9) for x in linspace(minmaxWeight[0], minmaxWeight[1], 5)]
    elif nEdges > 25000:
        weightSize = [power(x,8) for x in linspace(minmaxWeight[0], minmaxWeight[1], 5)]
    elif nEdges > 10000:
        weightSize = [power(x,7) for x in linspace(minmaxWeight[0], minmaxWeight[1], 5)]
    elif nEdges > 2000:
        weightSize = [power(x,6) for x in linspace(minmaxWeight[0], minmaxWeight[1], 5)]
    elif nEdges > 1000:
        weightSize = [power(x,5) for x in linspace(minmaxWeight[0], minmaxWeight[1], 5)]
    elif nEdges > 500:
        weightSize = [power(x,4) for x in linspace(minmaxWeight[0], minmaxWeight[1], 5)]
    elif nEdges > 100:
        weightSize = [power(x,3) for x in linspace(minmaxWeight[0], minmaxWeight[1], 5)]
    else:
        weightSize = [power(x,2) for x in linspace(minmaxWeight[0], minmaxWeight[1], 5)]
    scale = 2.5/amax(weightSize)
    weightSize = [x*scale for x in weightSize]
    
    #print(edgeData)
    if nRange == 5:
        qvals = edgeData.quantile([0, 0.687, 0.955, 0.997, 1])
    elif nRange == 6:
        qvals = edgeData.quantile([0, 0.687, 0.955, 0.997, 0.999, 1])
    else:
        raise ValueError("Did not reconigze range {0}".format(nRange))
        
    #cols  = cubehelix_palette(n_colors=5, start=2.8, rot=.1)
    cols   = color_palette("OrRd", 5)
    cols_d = color_palette("OrRd_d", 5)
    maxCol = hls_palette(8, l=.3, s=.8)

    ecols = Series(edgeData.shape[0]*[0])
    esize = Series(edgeData.shape[0]*[weightSize[0]])
    for i in range(1, len(qvals)):
        idx = (edgeData <= qvals.iloc[i]) & (edgeData > qvals.iloc[i-1])
        ecols[idx] = i-1
        esize[idx] += weightSize[i]
        
    ecurve = []
    ecols = [cols[i] for i in ecols.values]
    for edgeIdx in range(dn.numEdges):
        edgeID  = dn.getEdgeIDByIdx(edgeIdx)
        edgeNum = dn.getEdgeNumByIdx(edgeIdx)
        edge    = dn.edges[edgeID]
        
        distance = edge.getAttrDataByKey("GeoDistance")
        day      = edge.getAttrDataByKey("DayOfWeek")
        edata = edgemetrics.get(edgeID)
        
        ld = None
        if distance == "VeryHigh":
            ld = 0.3
        elif distance == "High":
            ld = 0.2
        elif distance == "Mid":
            ld = 0.1
        elif distance == "Low":
            ld = 0.05
        elif distance == "VeryLow":
            ld = 0.0
        else:
            ecurve.append(0.0)
        
    edge0Idx = dn.getEdgeIdx(0)
    ecols[edge0Idx] = maxCol[0]
    esize[edge0Idx] = amax(esize)+1
    #ecols[edge0ID] = cols[4]

    median = edgeData.quantile(.687)
    #print(median)
    #print(edgeData.max())
    #try:
    #    esize = [3*tanh(x/median) for x in edgeData]
    #except:
    #    esize = [3*tanh(x) for x in edgeData]
    #esize[edge0ID] += 1
    #print(esize)
    
    return ecols, esize, ecurve


def zeroEdgeVertex(g, vsize, esize, minDegree=None, minWeight=None, debug=False):

    # Zero vertices
    vdgs = g.degree()
    if minDegree is not None:
        vtxIDs = [v.index for v in g.vs if v.degree() < minDegree]
        if debug: print("   Removing {0} vertices".format(len(vtxIDs)))
        for i,v in enumerate(g.vs):
            if v.index in vidx:
                vsize[i] = 0.0
                vdgs[i] = 0.0

                
    # Zero edges (and vertices if not enough trips)
    if minWeight is not None:
        nVtxExtra = 0
        edgeIDs = [e.index for e in g.es if e['weight'] < minWeight]
        if debug: print("   Removing {0} edges".format(len(edgeIDs)))
        for i,e in enumerate(g.es):
            if e.index in edgeIDs:
                esize[i] = 0.0
                vdgs[e.source] -= 1
                if minDegree is not None:
                    if vdgs[e.source] < minDegree:
                        vsize[e.source] = 0.0
                    vdgs[e.target] -= 1
                    if vdgs[e.target] < minDegree:
                        vsize[e.target] = 0.0

        if debug: print("   Removed {0} additional vertices".format(nVtxExtra))
    
    
    # Go back and zero out trips if the vertex was zeroed
    if minDegree is not None:
        egone = 0    
        for i,e in enumerate(g.es):
            if amin([vsize[e.source],vsize[e.target]]) <= 0.0:
                esize[i] = 0.0
                egone += 1
                continue
            if e.source in vtxIDs or e.target in vtxIDs:
                esize[i] = 0.0
                egone += 1
        if debug: print("   Removing {0} edges".format(egone))

    return vsize,esize
    


def plotNetworkAttribute(gdata, prec, device, name, color, suffix, eq=None, retax=True):    
    from matplotlib import pyplot as plt
    #bins = getBestBinning(gdata, maxBins=100)
    bins = 100
    if gdata.shape[0] <= 1:
        print("There is no data for {0} and device {1}".format(name, device))
        return
    ax   = gdata.plot(kind='hist', grid=False, bins=bins, color=color, title='{0} {1}'.format(device, name))
    ax.set_yscale('log')

    left, width = .15, .70
    bottom, height = .15, .70
    right = left + width
    top = bottom + height
    
    #$\sum_{i=0}^\infty x_i$
    
    #eq = r'$\sum_{i,j} \frac{g_{ivj},g_{ij}}$'
    #eq = r'$\mathcal{A}\mathrm{sin}(2 \omega t)$'
    if eq is not None:
        ax.text(right, top, eq, horizontalalignment='right', verticalalignment='top', transform=ax.transAxes)
        
        
    fname = "plots/{0}/{1}_Len{2}.png".format(device, suffix, prec)
    try:
        plt.savefig(fname)
        ax.clear()
    except:
        print("Could not save {0}".format(fname))
    
    

def plotNetworkAttributes(g, device, prec):

    networkProperties = getNetworkAttributes(g)

    
    vertexdata            = networkProperties['Vertex']['Degree']
    betweennessdata       = networkProperties['Vertex']['Betweenness']
    closenessdata         = networkProperties['Vertex']['Closeness']
    #corenessdata          = networkProperties['Vertex']['Coreness']
    #constraintdata        = networkProperties['Vertex']['Constraint']
    eccentricitydata      = networkProperties['Vertex']['Eccentricity']
    hubscoredata          = networkProperties['Vertex']['HubScore']
    pagerankdata          = networkProperties['Vertex']['PageRank']
    vertextripsdata       = networkProperties['Vertex']['Trips']
    centralitydata        = networkProperties['Vertex']['Centrality']
    edgebetweennessdata   = networkProperties['Edge']['Betweenness']
    edgedata              = networkProperties['Edge']['Weight']

    
    #print("  Plotting Vertex Degree")
    plotNetworkAttribute(vertexdata, prec, device, "Vertex Degree", 'blue', "vertex_degree")

    #print("  Plotting Vertex Trips")
    plotNetworkAttribute(vertextripsdata, prec, device, "Vertex Trips", 'violet', "vertex_trips")

    #print("  Plotting Vertex Centrality")
    plotNetworkAttribute(centralitydata, prec, device, "Vertex Centrality", 'brown', "vertex_centrality")

    #print("  Plotting Vertex Coreness")
    #plotNetworkAttribute(corenessdata, prec, device, "Vertex Coreness", 'black', "vertex_coreness")

    #print("  Plotting Edge Weight")
    plotNetworkAttribute(edgedata, prec, device, "Edge Weight", 'orange', "edge_weight")

    #print("  Plotting Vertex Closeness")
    plotNetworkAttribute(closenessdata, prec, device, "Vertex Closeness", 'pink', "vertex_closeness")

    #print("  Plotting Vertex Betweeness")
    plotNetworkAttribute(betweennessdata, prec, device, "Vertex Betweeness", 'green', "vertex_betweenness")

    #print("  Plotting Vertex HubScore")
    plotNetworkAttribute(hubscoredata, prec, device, "Vertex HubScore", 'magenta', "vertex_hubscore")

    #print("  Plotting Edge Betweenness")
    plotNetworkAttribute(edgebetweennessdata, prec, device, "Edge Betweeness", 'red', "edge_betweenness")


    
def networkSummaryFile(dn, device, prec, vtxmetrics, edgemetrics, names, vtxDegreeQuant=0.5, edgeWeightQuant=0.75, debug=False):
    g = dn.getNetwork()
    
    sumFile = "plots/{0}/summary{1}.dat".format(device, prec)
    try:
        from os import remove
        remove(sumFile)
    except:
        if debug: print("Could not remove {0}".format(sumFile))
        pass

    print("Device:   {0}".format(device), file=open(sumFile, "a"))
    print("Geohash:  {0}".format(prec), file=open(sumFile, "a"))
    print("Vertices: {0}".format(g.vcount()), file=open(sumFile, "a"))
    print("Edges:    {0}".format(g.ecount()), file=open(sumFile, "a"))
        
    
        
    locsForMap={}
    ## Vertices
    first    = True
    vtxQuant = max([25, int(0.1*dn.numVertices)])
    for vertexNum in range(dn.numVertices):
        vertexID = dn.getVertexID(vertexNum)
        vertex   = dn.vertices[vertexID]
        if vertexNum >= vtxQuant:
            if vertexID != dn.homeVertexID:
                continue
        
        if first is True:
            first = False
            print("============= Vertices (> {0}) =============".format(round(vtxQuant,2)), file=open(sumFile, "a"))
            print("   {0:<5}{1:<5}{2:<9}{3:<9}{4:<9}{5:<10}{6:<10}{7:<10}{8:<10}{9:<10}{10:<30}".format("#", "ID", "Degree", "Trips", "Central", "POI", "Dwell", "State", "County", "Place", "Attrs"), file=open(sumFile, "a"))

        degree   = vertex.getAttrDataByKey('Degree')
        trips    = vertex.getAttrDataByKey('Trips')
        central  = vertex.getAttrDataByKey('Centrality')
        poi      = vertex.getAttrDataByKey("POIUniqueVisits")
        place    = vertex.getAttrDataByKey("CensusPlace")
        county   = vertex.getAttrDataByKey("CensusCounty")
        if county is not None:
            county   = county.replace("County", "").strip()
        state    = vertex.getAttrDataByKey("CensusState")
        dwell    = vertex.getAttrDataByKey("DwellTime")
        com      = vertex.getFeatureDataByKey("CoM")
        attrs    = vertex.getAttrsList()
        attrsMod = [x for x in attrs if x.startswith("Census") is False]
        attrsMod = [x for x in attrsMod if x.startswith("DwellTime") is False]
        attrsMod = [x for x in attrsMod if x.startswith("CoM") is False]
        attrsMod = [x for x in attrsMod if x.startswith("DayOfWeek") is False]
        attrsMod = [x.replace("ROADS", "") for x in attrsMod]
        attrsMod = [x.replace("OSM", "") for x in attrsMod]
        attrsMod = [x.replace("Terminals", "") for x in attrsMod]
        attrsMod = [x.replace("UniqueVisits", "") for x in attrsMod]
        attrsMod = [x.replace("HEREPOI", "") for x in attrsMod]

        attrsStr = ", ".join(attrsMod)
        try:
            com = com["Name"]
        except:
            com = (None, None)
        radius   = vertex.getAttrDataByKey("Radius")
        
        locdata = {"CoM": com, "Radius": radius, "POI": poi, "Degree": degree, "Dwell": dwell, "Place": place, "Trips": trips}
        if vertexNum < 10:
            if vertexID != dn.homeVertexID:
                locsForMap[vertexNum] = locdata
        if vertexID == dn.homeVertexID:
            locsForMap["Home"] = locdata
                
        
        if vertexID == dn.homeVertexID:
            print(" * ", end="", file=open(sumFile, "a"))
        else:
            print("   ", end="", file=open(sumFile, "a"))
        showLoc=False

        print("{0:<5}{1:<5}{2:<9}{3:<9}{4:<9}{5:<10}{6:<10}{7:<10}{8:<10}{9:<10}{10:<30}".format(str(vertexNum),
                                                                              str(vertexID),
                                                                              str(round(degree,2)),
                                                                              str(round(trips,2)),
                                                                              str(round(central,2)),
                                                                              str(poi),
                                                                              str(dwell),
                                                                              str(state)[:9],
                                                                              str(county)[:9],
                                                                              str(place)[:9],
                                                                              str(attrsStr)[:29]),
                                                                              end="", file=open(sumFile, "a"))
        print("", file=open(sumFile, "a"))
        
    ## Edges
    first = True    
    edgeQuant = min([25, int(0.1*dn.numEdges)])
    for edgeNum in range(dn.numEdges):
        edgeID  = dn.getEdgeID(edgeNum)
        edgeIdx = dn.getEdgeIdx(edgeNum)
        edge    = dn.edges[edgeID]
        if edgeNum >= edgeQuant:
            continue              

        if first is True:
            first = False
            print("\n============= Edges =============", file=open(sumFile, "a"))
            print("   {0:<5}{1:<10}{2:<5}{3:<10}{4:<10}{5:<10}{6:<10}{7:<10}".format("#", "ID", "Idx", "Weight", "DOW", "ITA", "Distance", "Attrs"), file=open(sumFile, "a"))                

        weight = edge.getAttrDataByKey('Weight')
        dow    = edge.getAttrDataByKey("DayOfWeek")
        ita    = edge.getAttrDataByKey("ITA")
        dist   = edge.getAttrDataByKey("Distance")
        poi    = edge.getAttrDataByKey("POI")
        attrs    = edge.getAttrsList()
        attrsMod = [x for x in attrs if x.startswith("Census") is False]
        attrsMod = [x for x in attrsMod if x.startswith("DwellTime") is False]
        attrsMod = [x for x in attrsMod if x.startswith("CoM") is False]
        attrsMod = [x for x in attrsMod if x.startswith("DayOfWeek") is False]
        attrsMod = [x for x in attrsMod if x.startswith("DrivingDistance") is False]
        attrsMod = [x for x in attrsMod if x.startswith("ITA") is False]
        attrsMod = [x for x in attrsMod if x.startswith("Duration") is False]
        attrsMod = [x for x in attrsMod if x.startswith("Interval") is False]
        attrsMod = [x for x in attrsMod if x.startswith("Distance") is False]
        attrsMod = [x.replace("ROADS", "") for x in attrsMod]
        attrsMod = [x.replace("OSM", "") for x in attrsMod]
        attrsMod = [x.replace("Terminals", "") for x in attrsMod]
        attrsMod = [x.replace("UniqueVisits", "") for x in attrsMod]
        attrsMod = [x.replace("HEREPOI", "") for x in attrsMod]
        attrsStr = ", ".join(attrsMod)

        print("   {0:<5}{1:<10}{2:<5}{3:<10}{4:<10}{5:<10}{6:<10}{7:<10}".format(str(edgeNum),
                                                                                 str(edgeID),
                                                                                 str(edgeIdx),
                                                                                 str(round(weight,2)),
                                                                                 str(dow),
                                                                                 str(ita),
                                                                                 str(dist),
                                                                                 str(attrsStr)),
                                                                                 end="", file=open(sumFile, "a"))
        print("", file=open(sumFile, "a"))
            
    print("\n============= Folium Text =============", file=open(sumFile, "a"))
    for vertexNum in range(10):
        if locsForMap.get(vertexNum) is not None:
            locdata = locsForMap[vertexNum]
            com     = locdata["CoM"]
            radius = locdata["Radius"]
            poi = locdata["POI"]
            dwell = locdata["Dwell"]
            degree = locdata["Degree"]
            trips = locdata["Trips"]
            popup = "Node {0}, Dwell: {1}, Radius: {2}, Degree: {3}, Trips: {4}, POI: {5}".format(vertexNum, dwell, radius, str(degree), str(trips), poi)
            if vertexNum > 5:
                color = "icon=folium.Icon(color='blue')"
            else:
                color = "icon=folium.Icon(color='orange')"                
            print("folium.Marker(location=[{0}, {1}], popup='{2}', {3}).add_to(m)".format(com[0], com[1], popup, color), file=open(sumFile, "a"))
            #print("location=[{0}, {1}], radius={2}, popup='{3}'".format(com[0], com[1], rad, vertexNum), file=open(sumFile, "a"))
    locdata = locsForMap["Home"]
    com = locdata["CoM"]
    radius = locdata["Radius"]
    poi = locdata["POI"]
    degree = locdata["Degree"]
    dwell = locdata["Dwell"]
    trips = locdata["Trips"]
    popup = "Home, Dwell: {0}, Radius: {1}, Degree: {2}, Trips: {3}, POI: {4}".format(dwell, radius, str(degree), str(trips), poi)
    print("folium.Marker(location=[{0}, {1}], popup='{2}', icon=folium.Icon(color='green',icon='home')).add_to(m)".format(com[0], com[1], popup), file=open(sumFile, "a"))
        #print("location=[{0}, {1}], radius={2}, popup='{3}'".format(com[0], com[1], rad, "Home"), file=open(sumFile, "a"))

        

def dropVertices(g, names, minDegree=None, minTrips=None, debug=False):
    if minDegree is None and minTrips is None:
        return g
    
    if minDegree is not None:
        degrees = g.degree()
        if isinstance(minDegree, (float,int)):
            vtxIDs = [v.index for v in g.vs if v.degree() < minDegree]
            if debug:
                print("Dropping {0}/{1} vertices from network with degree < {2}".format(len(vtxIDs), len(degrees), minDegree))
            g.delete_vertices(vtxIDs)
            if debug:
                print("There are now {0} vertices in this network".format(len(g.degree())))
        if len(g.degree()) == 0:
            raise ValueError("There are no vertices after the degree ({0}) cut".format(minDegree))
                
    if minTrips is not None:
        vtxTrips = getVertexTrips(g, None)
        if isinstance(minTrips, (float,int)):
            vtxIDs = []
            for vtxID,vtxTripCnt in getVertexTrips(g, None).items():
                if vtxTripCnt < minTrips:
                    vtxIDs.append(vtxID)
            if debug:
                print("Dropping {0}/{1} vertices from network with trips < {2}".format(len(vtxIDs), len(vtxTrips), minTrips))
            g.delete_vertices(vtxIDs)
            if debug:
                print("There are now {0} vertices in this network".format(len(g.degree())))
        if len(g.degree()) == 0:
            raise ValueError("There are no vertices after the trips ({0}) cut".format(minTrips))

    return g


        
def plotNetworkGraph(dn, device, prec, drops=None, cuts=[{'minV': 2 , 'minE': 2}], names=None, vtxmetrics=None,
                     edgemetrics=None, homemetrics=None, bbox=None, layoutname="rt_circular", saveit=True, plotIndiv=True, debug=False):
    from numpy import amax, amin, mean, std, percentile
    from pandas import Series
    from matplotlib import pyplot as plt
    from modelPlots import getBestBinning
    from collections import Counter
    
    g = dn.getNetwork()
    
    layout = g.layout(layoutname)
    if bbox is None:
        bbox = [0.5*x for x in (1000,1000)]
    
    
    makeNetworkDir(device, rm=False)


    from pandas import qcut
    from seaborn import color_palette

        
    ## Get Vertex,Edge Views
    vcols, vsize, vshape = getVertexViews(dn, vtxmetrics, homemetrics)    
    if vcols is None or vsize is None:
        return
    ecols, esize, ecurve = getEdgeViews(dn, edgemetrics)
    if ecols is None or esize is None:
        return
    
    
    
    
    ## Drop vertices
    visual_style = {}
    visual_style["layout"]       = layout
    visual_style["margin"]       = 10
    if drops is not None:
        ## Plot the dropped network
        g = dropVertices(g, drops.get('minDegree'), drops.get('minTrips'))    
    ## Plot the network
    vcols, vsize, vshape = getVertexViews(dn, vtxmetrics, homemetrics)
    ecols, esize, ecurve = getEdgeViews(dn, edgemetrics)
    visual_style["vertex_color"] = vcols
    visual_style["vertex_size"]  = vsize
    visual_style["vertex_shape"] = vshape
    visual_style["edge_color"]   = ecols
    visual_style["edge_width"]   = esize
    visual_style["edge_curved"]  = ecurve
    fname = "plots/{0}/network_Len{1}_{2}.png".format(device, prec, layoutname)
    igplot = ig.plot(g, bbox=bbox, background="white", **visual_style) #, layout = layout)
    print("   ---> Saving {0}".format(fname))
    igplot.save(fname)
    

    networkSummaryFile(dn, device, prec, vtxmetrics, edgemetrics, names)

    if isinstance(cuts, dict):
        icut=0
        vidx = []
        eidx = []
        vdgs = Counter()

        vsize,esize = zeroEdgeVertex(g, vsize, esize, minDegree=cuts.get('minDegree'), minWeight=cuts.get('minWeight'), debug=debug)
        visual_style["vertex_size"]  = vsize
        visual_style["edge_width"]   = esize
        visual_style["vertex_shape"] = vshape
        visual_style["edge_curved"]  = ecurve


        fname = "plots/{0}/network_Len{1}_{2}_cut{3}.png".format(device, prec, layoutname, icut)
        igplot = ig.plot(g, bbox=bbox, background="white", **visual_style) #, layout = layout)
        print("   ---> Saving {0}".format(fname))
        igplot.save(fname)