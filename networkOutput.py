from numpy import log10

class printNetwork():
    def __init__(self, dn):
        self.dn = dn
        
        
    #################################################################################################################
    # Print/Show Network
    #################################################################################################################
    def printFrequencies(self, debug=False):
        vertices = self.dn.getVertices()
        
        geoCategories = {}
        for vertexNum,vertexName in enumerate(vertices):
            vertexData = self.dn.getVertexByName(vertexName, 'feat')                        
            internal   = vertexData["Internal"]
            network    = vertexData["Network"]
            geospatial = vertexData["GeoSpatial"]
            for key,value in geospatial.items():
                if geoCategories.get(key) is None:
                    geoCategories[key] = []
                if value > 0:
                    geoCategories[key].append(vertexName)
                
        print('{cmt: <{width}}'.format(cmt="Category", width=20), end="")
        print('{cmt: <{width}}'.format(cmt="Counts", width=5), end="")
        print('{cmt: <{width}}'.format(cmt="Clusters", width=50), end="")
        print("")
        for category in sorted(geoCategories.keys()):
            counts = geoCategories[category]
            print('{cmt: <{width}}'.format(cmt=category, width=20), end="")
            print('{cmt: <{width}}'.format(cmt=len(counts), width=5), end="")
            print('{cmt: <{width}}'.format(cmt=",".join(counts), width=50), end="")
            print("")
            
        
        
    #################################################################################################################
    # Print/Show Network
    #################################################################################################################
    def printVertices(self, minN=5, debug=False):
        vertices = self.dn.getVertices()
        print("\n\n======================================== {0} Vertices (min {1}) ========================================\n".format(len(vertices), minN))
        from collections import OrderedDict
        header = OrderedDict({"#": 4, "Cl": 6, "N": 6, "Home": 5, "Active": 10, "DayWeek": 10, "Dwell": 10, "Place": 25, "Cliques": 8, "Cluster": 8, "Degree": 8, "Centrality": 12, "ShortPath": 12, "Spectral": 12, "PageRank": 10, "Spectral": 10, "POIs": 50})
        for k,v in header.items():
            print('{cmt: <{width}}'.format(cmt=k, width=v), end="")
        print("")
        for k,v in header.items():
            print('{cmt: <{width}}'.format(cmt='---', width=v), end="")
        print("")
        stop = False
        for vertexNum,vertexName in enumerate(vertices):
            vertexData = self.dn.getVertexByName(vertexName, 'feat')
            internal   = vertexData["Internal"]
            census     = vertexData["Census"]
            network    = vertexData["NetworkRank"]
            geospatial = vertexData["GeoSpatial"]
            
            if internal['N'] < minN:
                continue
                
            #widths = iter(header.values())
            
            for name,width in header.items():
                if name == "#":
                    ## #
                    print('{cmt: <{width}}'.format(cmt=vertexNum, width=width), end="")

                if name == "Cl":
                    ## Cl
                    print('{cmt: <{width}}'.format(cmt=vertexName, width=width), end="")
            
                if name == "N":
                    ## N
                    n = internal['N']
                    print('{cmt: <{width}}'.format(cmt=n, width=width), end="")    

                if name == "Home":
                    if internal['IsHome'] == 1:
                        home = "***"
                    else:
                        home = ""
                    ## Home
                    print('{cmt: <{width}}'.format(cmt=home, width=width), end="")

                if name == "Active":            
                    ## Active
                    active = internal['FractionalVisits']
                    print('{cmt: <{width}}'.format(cmt=active, width=width), end="")    
                
                if name == "DayWeek":            
                    ## Day
                    dow = internal['DayOfWeek']
                    print('{cmt: <{width}}'.format(cmt=dow, width=width), end="")     
            
                if name == "Dwell":
                    ## Dwell
                    dwell = internal['DwellTime']
                    print('{cmt: <{width}}'.format(cmt=dwell, width=width), end="")    
                
                if name == "Place":
                    ## Place
                    try:
                        place=str(census["Place"])[:width-2]
                    except:
                        place="N/A"
                    try:
                        state=str(census["State"])[:width-2]
                    except:
                        state="N/A"
                    place = ", ".join([place, state])
                    print('{cmt: <{width}}'.format(cmt=place, width=width), end="") 

                if name == "Cliques":
                    nocliques = round(network["NumberOfCliques"],3)
                    print('{cmt: <{width}}'.format(cmt=nocliques, width=width), end="")

                if name == "Cluster":
                    clustering = round(network["Clustering"],3)
                    print('{cmt: <{width}}'.format(cmt=clustering, width=width), end="")

                if name == "Degree":
                    degree = round(network["AverageNeighborDegree"],2)
                    print('{cmt: <{width}}'.format(cmt=degree, width=width), end="")

                if name == "Centrality":
                    degree = round(network["EigenvectorCentrality"],2)
                    print('{cmt: <{width}}'.format(cmt=degree, width=width), end="")
                    
                if name == "DCentral":
                    degree = round(network["DegreeCentrality"],3)
                    print('{cmt: <{width}}'.format(cmt=degree, width=width), end="")

                if name == "ECentral":
                    degree = round(network["EigenvectorCentrality"],3)
                    print('{cmt: <{width}}'.format(cmt=degree, width=width), end="")
                        
                if name == "ShortPath":
                    degree = round(network["ShortestPath"],3)
                    print('{cmt: <{width}}'.format(cmt=degree, width=width), end="")
                        
                if name == "Spectral":
                    degree = round(network["SpectralOrdering"],3)
                    print('{cmt: <{width}}'.format(cmt=degree, width=width), end="")
                    
                if name == "PageRank":
                    degree = network["Pagerank"]
                    print('{cmt: <{width}}'.format(cmt=degree, width=width), end="")
            
                if name == "POIs":
                    pois   = ", ".join([k for k,v in geospatial.items() if v > 0])
                    print('{cmt: <{width}}'.format(cmt=pois, width=width), end="")

        
            print("") 

            """
            HomeNetworkAverageNeighborDegree	3.75
            HomeNetworkDegreeCentrality	0.0106
            HomeNetworkEigenvectorCentrality	3.96e-10
            HomeNetworkEigenvectorCentralityNumpy	3.96e-10
            HomeNetworkKatzCentralityNumpy	0.0278
            HomeNetworkClosenessCentrality	0.123
            HomeNetworkCurrentFlowClosenessCentrality	0.000599
            HomeNetworkBetweennessCentrality	0.00265
            HomeNetworkCurrentFlowBetweennessCentrality	0.0226
            HomeNetworkApproximateCurrentFlowBetweennessCentrality	3.02e-17
            HomeNetworkCommunicabilityBetweennessCentrality	0.00299
            HomeNetworkNewmanBetweennessCentrality	0.00265
            HomeNetworkSubgraphCentrality	6.12
            HomeNetworkSubgraphCentralityExp	6.12
            HomeNetworkHarmonicCentrality	51.1
            HomeNetworkNodeCliqueNumber	2
            HomeNetworkNumberOfCliques	2
            HomeNetworkTriangles	0
            HomeNetworkClustering	0
            HomeNetworkSquareClustering	0.125
            HomeNetworkCenter	0
            HomeNetworkEccentricity	13
            HomeNetworkPeriphery	0
            HomeNetworkDominatingSet	0
            HomeNetworkPagerank	0.00289
            HomeNetworkMaximalMatching	12
            HomeNetworkMaxWeightMatching	19
            HomeNetworkMaximalIndependentSet	0
            HomeNetworkShortestPath	9.12
            HomeNetworkSpectralOrdering	373            
            """
        
    #################################################################################################################
    # Print/Show Network
    #################################################################################################################
    def printEdges(self, minW=5, debug=False):
        edges = self.dn.getEdges()
        print("\n\n======================================== {0} Edges (min {1}) ========================================\n".format(len(edges), minW))
        from collections import OrderedDict
        header = OrderedDict({"#": 4, "ID": 18, "N": 5, "Active": 10, "DayWeek": 10, "Distance": 10, "Place": 20}) #, "State": 20, "Cliques": 8, "Cluster": 8, "Degree": 8, "DCentral": 9, "ECentral": 9, "ShortPath": 10, "PageRank": 8})
        for k,v in header.items():
            print('{cmt: <{width}}'.format(cmt=k, width=v), end="")
        print("")
        for k,v in header.items():
            print('{cmt: <{width}}'.format(cmt='---', width=v), end="")
        print("")
        for edgeNum,edgeName in enumerate(edges):
            edgeData = self.dn.getEdgeByName(edgeName, 'feat')
            internal = edgeData["Internal"]
            census   = edgeData["Census"]
            network  = edgeData["Network"]
            
            if network['EdgeWeight'] < minW:
                continue
            
            
            for name,width in header.items():
                if name == "#":
                    ## #
                    print('{cmt: <{width}}'.format(cmt=edgeNum, width=width), end="")
                    
                if name == "ID":
                    ## Cl
                    ID = str(edgeName)
                    print('{cmt: <{width}}'.format(cmt=ID, width=width), end="")

                if name == "N":
                    ## Active
                    n = int(network['EdgeWeight'])
                    print('{cmt: <{width}}'.format(cmt=n, width=width), end="")    
            
                if name == "Active":
                    ## Active
                    active = internal['FractionalActive']
                    print('{cmt: <{width}}'.format(cmt=active, width=width), end="")    
            
                if name == "DayWeek":
                    ## Day
                    dow = internal['DayOfWeek']
                    print('{cmt: <{width}}'.format(cmt=dow, width=width), end="")     
            
                if name == "Distance":
                    ## dist
                    dist = internal['DrivingDistance']
                    print('{cmt: <{width}}'.format(cmt=dist, width=width), end="")    

                if name == "Place":
                    try:
                        place=str(census["Place"])
                    except:
                        place=""
                    print('{cmt: <{width}}'.format(cmt=place, width=width), end="") 
                
            print("")
            
            