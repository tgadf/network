from edgeData import edge
from vertexData import vertex
import igraph as ig

class driverNetwork():
    def __init__(self, trips, debug=False):
        self.g                = None
        
        self.trips            = trips
        self.vertexNamesToIDs = trips['vertexNameToID']
        self.vertexIDsToNames = trips['vertexIDToName']
        self.numVertices      = None
        self.edgeWeights      = trips['edgesVtxID']
        self.numEdges         = None
        
        self.vertexMetrics    = trips['vertexMetrics']
        self.edgeMetrics      = trips['edgeMetrics']
        self.homeMetrics      = trips['homeMetrics']
        self.homeVertexID     = self.homeMetrics['Vtx']
        self.homeCluster      = self.homeMetrics['Geo']

        self.vertexIDToNum    = None
        self.vertexNumToID    = None        
        self.vertexTrips      = None
        self.vertexAttributes = None
        self.vertexAttributeProperites = None
        
        self.edgeIDToNum      = None
        self.edgeIDToIdx      = None
        self.edgeNumToID      = None
        self.edgeNumToIdx     = None
        self.edgeIdxToID      = None
        self.edgeIdxToNum     = None
        self.edgeAttributes   = None
        self.edgeAttributeProperites = None
        
        self.networkStats     = {}
        
        self.vertexExternalData  = None
        self.edgeExternalData    = None
        self.networkExternalData = None
        
        self.vertexAttrKeys = ["Degree", "Betweenness", "Closeness", "HubScore", "PageRank", "Trips", "Coreness", "Eccentricity", "Centrality", "TripsRatio"]
        self.edgeAttrKeys   = ["Weight", "Betweenness"]
        
        self.edges    = {}
        self.vertices = {}
        
        self.device           = trips['device']
        
        if debug is True:
            print("Driver Network for {0}".format(self.device))
        
        
    ####################################################################################
    #
    # Getters
    #
    ####################################################################################
    def getNetwork(self):
        return self.g
    
    def getDevice(self):
        return self.device
        
        
    ####################################################################################
    #
    # Setters
    #
    ####################################################################################
    def setEdge(self, edgeID, edge):
        self.edges[edgeID] = edge
    
    def setVertex(self, vertexID, vertex):
        self.vertices[vertexID] = vertex
    
        
    ####################################################################################
    #
    # Map Functions
    #
    ####################################################################################
    def getVertexID(self, vertexNum, debug=False):
        if self.vertexNumToID is None:
            setVertexOrder(debug)
        try:
            vertexID = self.vertexNumToID[vertexNum]
        except:
            vertexID = None
            if debug:
                print("Could not get vertex ID using num {0} from list of {1} vertices".format(vertexNum, self.numVertices))
        return vertexID
    
    
    def getVertexNum(self, vertexID, debug=False):
        if self.vertexIDToNum is None:
            setVertexOrder(debug)
        try:
            vertexNum = self.vertexIDToNum[vertexID]
        except:
            vertexNum = None
            if debug:
                print("Could not get vertex num using ID {0} from list of {1} vertices".format(vertexNum, self.numVertices))
        return vertexNum
    
        
    def getEdgeID(self, edgeNum, debug=False):
        if self.edgeNumToID is None:
            self.setEdgeOrder(debug)
        try:
            edgeID = self.edgeNumToID[edgeNum]
        except:
            edgeID = None
            if debug:
                print("Could not get edge ID from num {0} from list of {1} edges".format(edgeNum, self.numEdges))
        return edgeID
    
    
    def getEdgeIdx(self, edgeNum, debug=False):
        if self.edgeIDToIdx is None:
            self.setEdgeOrder(debug)
        try:
            edgeIdx = self.edgeNumToIdx[edgeNum]
        except:
            edgeIdx = None
            if debug:
                print("Could not get edge Idx from num {0} from list of {1} edges".format(edgeNum, self.numEdges))
        return edgeIdx
    
        
    def getEdgeNumByID(self, edgeID, debug=False):
        if self.edgeIDToNum is None:
            self.setEdgeOrder(debug)
        try:
            edgeNum = self.edgeIDToNum[edgeID]
        except:
            edgeNum = None
            if debug:
                print("Could not get edge num from ID {0} from list of {1} edges".format(edgeID, self.numEdges))
        return edgeNum
    
        
    def getEdgeIdxByID(self, edgeID, debug=False):
        if self.edgeIDToIdx is None:
            self.setEdgeOrder(debug)
        try:
            edgeIdx = self.edgeIDToIdx[edgeID]
        except:
            edgeIdx = None
            if debug:
                print("Could not get edge Idx from ID {0} from list of {1} edges".format(edgeID, self.numEdges))
        return edgeIdx
    
        
    def getEdgeNumByIdx(self, edgeIdx, debug=False):
        if self.edgeIdxToNum is None:
            self.setEdgeOrder(debug)
        try:
            edgeNum = self.edgeIdxToNum[edgeIdx]
        except:
            edgeNum = None
            if debug:
                print("Could not get edge num from Idx {0} from list of {1} edges".format(edgeIdx, self.numEdges))
        return edgeNum
    
        
    def getEdgeIDByIdx(self, edgeIdx, debug=False):
        if self.edgeIdxToID is None:
            self.setEdgeOrder(debug)
        try:
            edgeID = self.edgeIdxToID[edgeIdx]
        except:
            edgeID = None
            if debug:
                print("Could not get edge ID from Idx {0} from list of {1} edges".format(edgeIdx, self.numEdges))
        return edgeID
    
        
        
    ####################################################################################
    #
    # Print
    #
    ####################################################################################
    def printVertices(self):
        print("#\tID\tNum\tDegree")
        for i,v in enumerate(self.g.vs):
            print("{0}\t{1}\t{2}\t{3}".format(i,v.index, self.vertexIDToNum[v.index], v.degree()))

    def printEdges(self):
        print("#\tID\tIdx\tNum\tWeight")
        for i,e in enumerate(self.g.es):
            edgeID  = self.edgeIdxToID[i]
            edgeNum = self.edgeIDToNum[edgeID]
            edgeIdx = self.edgeIDToIdx[edgeID]
            
            print("{0}\t{1}\t{2}\t{3}\t{4}".format(i, edgeID, edgeIdx, edgeNum, e['weight']))


            
    ####################################################################################
    #
    # External Information
    #
    ####################################################################################
    def getVertexExternalDataByID(self, vertexID, debug=False):
        try:
            externalData = self.vertexExternalData[vertexID]
        except:
            if debug:
                print("Could not find external data for vertex ID {0}".format(vertexID))
            externalData = None
        return externalData
            
    def getVertexExternalData(self, vertexNum, debug=False):
        vertexID = self.vertexNumToID[vertexNum]
        return self.getVertexExternalDataByID(vertexID, debug)
            
    def getVertexExternalDataByIDByKey(self, vertexID, key, debug=False):
        externalData = self.getVertexExternalDataByID(vertexID, debug)
        try:
            value = externalData[key]
        except:
            if debug:
                print("Could not find key {0} in external data for vertex ID {1}.".format(key, vertexID))
            value = None
        return value
            
    def getVertexExternalDataByKey(self, vertexNum, key, debug=False):
        vertexID = self.vertexNumToID[vertexNum]
        return self.getVertexExternalDataByIDByKey(vertexID, key, debug)
    
    def setVertexExternalData(self, vertexNum, key, value, debug=False):
        if self.vertexExternalData is None:
            if debug:
                print("Creating external data dictionary for vertices")
            self.vertexExternalData = {}
            for i,v in enumerate(self.g.vs):
                self.vertexExternalData[v.index] = {}
           
        try:
            vertexID = self.vertexNumToID[vertexNum]
        except:
            raise ValueError("Could not find vertex ID from vertex num {0}".format(vertexNum))
        
        try:
            self.vertexExternalData[vertexID][key] = value
        except:
            print("Could not set key {0} and value {1} for vertex ID {2}".format(key, value, vertexID))
            
    def getEdgeExternalDataByIDByKey(self, edgeID, key, debug=False):
        externalData = self.getEdgeExternalDataByID(edgeID, debug)
        try:
            value = externalData[key]
        except:
            if debug:
                print("Could not find key {0} in external data for edge ID {1}.".format(key, edgeID))
            value = None
        return value
            
    def getEdgeExternalDataByKey(self, edgeNum, key, debug=False):
        edgeID = self.edgeNumToID[edgeNum]
        return self.getEdgeExternalDataByIDByKey(edgeID, key, debug)


    def getEdgeExternalDataByID(self, edgeID, debug=False):
        try:
            externalData = self.edgeExternalData[edgeID]
        except:
            if debug:
                print("Could not find external data for edge ID {0}".format(edgeID))
            externalData = None
        return externalData
    
    def getEdgeExternalData(self, edgeNum, debug=False):
        edgeID = self.edgeNumToID[edgeNum]
        return self.getEdgeExternalDataByID(edgeID, debug)
    
    def setEdgeExternalData(self, edgeNum, key, value, debug=False):
        if self.edgeExternalData is None:
            if debug:
                print("Creating external data dictionary for edges")
            self.edgeExternalData = {}
            for i,e in enumerate(self.g.es):
                edgeID = self.getEdgeID(i)
                self.edgeExternalData[edgeID] = {}
           
        try:
            edgeID = self.edgeNumToID[edgeNum]
        except:
            raise ValueError("Could not find vertex ID from edge num {0}".format(edgeNum))
        
        try:
            self.edgeExternalData[edgeID][key] = value
        except:
            print("Could not set key {0} and value {1} for edge ID {2}".format(key, value, edgeID))


    def getNetworkExternalData(self, debug=False):
        try:
            externalData = self.networkExternalData
        except:
            if debug:
                print("Could not find external data for network")
            externalData = None
        return externalData
    
    def setNetworkExternalData(self, key, value, debug=False):
        if self.networkExternalData is None:
            if debug:
                print("Creating external data dictionary for network")
            self.networkExternalData = {}
           
        try:
            self.networkExternalData[key] = value
        except:
            print("Could not set key {0} and value {1} for network".format(key, value))
            
            
            
            
    ####################################################################################
    #
    # Create Network
    #
    ####################################################################################
    def createNetwork(self, debug = False):
        self.g = ig.Graph()
        
        try:
            vtxList = self.vertexNamesToIDs
            self.numVertices = len(vtxList)
            self.g.add_vertices(self.numVertices)
            if debug:
                print("  Created {0} vertices for the network".format(self.numVertices))
            self.networkStats['Vertices'] = self.numVertices
        except:
            raise ValueError("Could not add vertices to graph!")

            
        try:
            self.edgeIdxToID = {}
            self.edgeIDToIdx = {}
            edgeList = list(self.edgeWeights.keys())
            for edgeIdx,edgeID in enumerate(edgeList):
                self.edgeIdxToID[edgeIdx] = edgeID
                self.edgeIDToIdx[edgeID]  = edgeIdx
            self.numEdges = len(edgeList)
            self.g.add_edges(edgeList)
            if debug:
                print("  Created {0} edges for the network".format(self.numEdges))
            self.networkStats['Edges'] = self.numEdges
        except:
            raise ValueError("Could not add edges to graph!")

            
        self.networkStats['Trips']    = 0
        self.networkStats['MaxTrip'] = {"Trip": None, "Weight": 0}
        for idx, e in enumerate(self.g.es):
            try:
                e["weight"] = self.edgeWeights[e.tuple]
            except:
                print("Error getting weight for edge {0}".format(e.tuple))
                e['weight'] = 1

            self.networkStats['Trips'] += e['weight']
            if e['weight'] > self.networkStats['MaxTrip']["Weight"]:
                self.networkStats['MaxTrip'] = {"Trip": e.tuple, "Weight": e['weight']}
            
        if debug:
            print("  Created driver network graph with {0} vertices and {1} edges.".format(self.numVertices, self.numEdges))
            print("  There are a total of {0} trips in this network".format(self.networkStats['Trips']))



            

    ####################################################################################
    #
    # Edge
    #
    ####################################################################################
    def setEdgeOrder(self, metric='Weight', debug=False):
        from pandas import Series
        try:
            if metric == "Weight":
                edgetuples         = list(self.edgeWeights.keys())
                try:
                    edgedata           = Series(self.g.es['weight'])
                    edgedata.index     = edgetuples
                except:
                    edgedata           = None
            else:
                raise ValueError("metric {0} was not recognized".format(metric))
        except:
            raise ValueError("Could not get edge data for metric {0}".format(metric))

        if edgedata is not None:
            ordereddata = edgedata.sort_values(ascending=False)
            self.edgeNumToID = dict(zip(range(len(ordereddata)), list(ordereddata.index)))
            self.edgeIDToNum = dict([[v,k] for k,v in self.edgeNumToID.items()])
        else:
            self.edgeNumToID = {}
            self.edgeIDToNum = {}
        self.edgeIdxToNum = {}
        self.edgeNumToIdx = {}
        for edgeID,edgeNum in self.edgeIDToNum.items():
            edgeIdx = self.edgeIDToIdx[edgeID]
            self.edgeIdxToNum[edgeIdx] = edgeNum
            self.edgeNumToIdx[edgeNum] = edgeIdx
        if debug:
            print("Created edge order with {0} metric".format(metric))
    
    
    def getEdgeByIdx(self, edgeIdx, debug=False):
        try:
            edge = self.g.es[edgeIdx]
        except:
            edge = None
            if debug:
                print("Could not get edge with Idx {0} from list of {1} edges".format(edgeIdx, self.numEdges))
        return edge
    
    
    def getEdge(self, edgeNum, debug=False):
        edgeIdx = self.getEdgeIdx(edgeNum, debug)
        try:
            edge   = self.getEdgeByIdx(edgeIdx)
        except:
            edge   = None
            if debug:
                print("Could not get edge number {0} and Idx {1} from list of {2} edges".format(edgeNum, edgeIdx, self.numEdges))            
        return edge
    
    
    def getEdgeByID(self, edgeID, debug=False):
        edgeIdx = self.getEdgeIdxByID(edgeID, debug)
        try:
            edge   = self.getEdgeByIdx(edgeIdx)
        except:
            edge   = None
            if debug:
                print("Could not get edge number {0} and ID {1} from list of {2} edges".format(edgeNum, edgeID, self.numEdges))            
        return edge
    
    
    def getEdgeVerticesByEdge(self, edge, debug=False):
        try:
            vertexIDs = [self.g.vs[edge.source].index, self.g.vs[edge.target].index]
        except:
            if debug:
                print("Could not get vertex IDs from edge")
            vertexIDs = [None, None]
        return vertexIDs
    

    def getEdgeVertexIDsByID(self, edgeID, debug=False):
        edge      = self.getEdgeByID(edgeID, debug)
        vertexIDs = self.getEdgeVerticesByEdge(edge, debug)
        return vertexIDs
    

    def getEdgeVerticesByID(self, edgeID, debug=False):
        edge      = self.getEdgeByID(edgeID, debug)
        vertexIDs = self.getEdgeVerticesByEdge(edge, debug)
        try:
            vertexIDs = [self.vertexIDToNum[x] for x in vertexIDs]
        except:
            if debug:
                print("Could not get vertex IDs from vertex Num when using the edge ID {0}".format(edgeID))
            vertexIDs = [None, None]        
        return vertexIDs
    

    def getEdgeVertices(self, edgeNum, debug=False):
        edgeID    = self.getEdgeID(edgeNum, debug)
        vertexIDs = self.getEdgeVerticesByID(edgeID, debug)
        return vertexIDs

    
            

    ####################################################################################
    #
    # Vertex
    #
    ####################################################################################
    def setVertexOrder(self, metric="HubScore", debug=False):
        from pandas import Series
        try:
            if metric == "HubScore":
                vertexdata           = Series(self.g.hub_score())
            elif metric == "Centrality":
                vertexdata           = Series(self.g.centrality())
            elif metric == "Degree":
                vertexdata           = Series(self.g.degree())
            else:
                if debug:
                    print("metric {0} was not recognized".format(metric))
                vertexData = None
        except:
            if debug:
                print("Could not get vertex data for metric {0}".format(metric))
            return None

        ordereddata = vertexdata.sort_values(ascending=False)
        self.vertexNumToID = dict(zip(range(len(ordereddata)), list(ordereddata.index)))
        self.vertexIDToNum = dict([[v,k] for k,v in self.vertexNumToID.items()])
        
        
        if debug:
            print("Created vertex order with {0} metric".format(metric))
    
    
    def getVertexByID(self, vertexID, debug=False):
        try:
            vertex = self.g.vs[vertexID]
        except:
            vertex = None
            if debug:
                print("Could not get vertex with ID [{0}]".format(vertexID))

        return vertex
        
        
    def getVertex(self, vertexNum, debug=False):
        if self.vertexNumToID is None:
            self.setVertexOrder(debug)
        try:
            vertexID = self.getVertexID(vertexNum, debug)
        except:
            if debug:
                print("Could not get vertex ID for num {0}".format(vertexNum))
            return None
        
        try:
            vertex   = self.getVertexByID(vertexID, debug)
        except:
            vertex   = None
            if debug:
                print("Could not get vertex number {0} and ID {1} from list of {2} vertices".format(vertexNum, vertexID, self.numVertices))
            
        return vertex
            

    def setVertexTrips(self, debug=False):
        from collections import Counter
        self.vertexTrips = Counter()
        for i,e in enumerate(self.g.es):
            for vertexID in [e.source, e.target]:
                self.vertexTrips[vertexID] += e['weight']

        if debug:
            print("Set trips for each of the {0} vertices in the network".format(len(self.vertexTrips)))
            
        
        

    ####################################################################################
    #
    # Network Attributes
    #
    ####################################################################################
    def setVertexAttributes(self, debug=False):
        if self.vertexAttributes is not None:
            return
        else:
            self.vertexAttributes = {}
            for attr in self.vertexAttrKeys:
                self.vertexAttributes[attr] = None
                
        
        from pandas import Series
        from numpy import log1p
        try:
            degreedata           = Series(self.g.degree())
            closenessdata        = Series(self.g.closeness())
            betweenessdata       = Series(log1p(self.g.betweenness()))
            hubscoredata         = Series(self.g.hub_score())
            pagerankdata         = Series(self.g.pagerank())
            constraintdata       = Series(self.g.constraint())  
            corenessdata         = Series(self.g.coreness())
            eccentricitydata     = Series(self.g.eccentricity())
            centralitydata       = Series(self.g.eigenvector_centrality())
        except:
            degreedata           = None
            closenessdata        = None
            betweenessdata       = None
            hubscoredata         = None
            pagerankdata         = None
            constraintdata       = None
            corenessdata         = None
            eccentricitydata     = None
            centralitydata       = None

        try:
            self.setVertexTrips(debug)
            tripsdata            = Series(self.vertexTrips)
            tripsratiodata       = tripsdata/degreedata
        except:
            tripsdata            = None
            tripsratiodata       = None

        self.vertexAttributes = {"Degree": degreedata, "Betweenness": betweenessdata, "Closeness": closenessdata,
                                 "HubScore": hubscoredata, "PageRank": pagerankdata, "Trips": tripsdata, "Coreness": corenessdata,
                                 "Eccentricity": eccentricitydata, "Centrality": centralitydata, "TripsRatio": tripsratiodata}
        self.vertexAttributeProperites = {}
        for attribute,attributedata in self.vertexAttributes.items():
            try:
                self.vertexAttributeProperites[attribute] = {"Median": attributedata.median(), "Sum": attributedata.sum(), "Mean": attributedata.mean()}
            except:
                self.vertexAttributeProperites[attribute] = {"Median": None, "Sum": None, "Mean": None}
            
        if debug:
            print("Set Vertex Attributes")
        

    def setEdgeAttributes(self, debug=False):
        if self.edgeAttributes is not None:
            return
        else:
            self.edgeAttributes = {}
            for attr in self.edgeAttrKeys:
                self.edgeAttributes[attr] = None
        
        error = 0
        from pandas import Series
        from numpy import log1p
        try:
            edgetuples           = list(self.edgeWeights.keys())
            weightsdata          = Series(self.g.es['weight'])
            weightsdata.index    = edgetuples
            betweenessdata       = Series(log1p(self.g.edge_betweenness()))
            betweenessdata.index = edgetuples
        except:
            error                = 1
            weightsdata          = None
            betweenessdata       = None
            
        
        self.edgeAttributes["Weight"]      = weightsdata
        self.edgeAttributes["Betweenness"] = betweenessdata
        self.edgeAttributeProperites = {}
        for attribute,attributedata in self.edgeAttributes.items():
            try:
                self.edgeAttributeProperites[attribute] = {"Median": attributedata.median(), "Sum": attributedata.sum(), "Mean": attributedata.mean()}
            except:
                self.edgeAttributeProperites[attribute] = {"Median": None, "Sum": None, "Mean": None}

        if debug:
            print("Set Edge Attributes.")
            
   
    def setNetworkAttributes(self, debug=False):
        self.setVertexAttributes(debug)
        self.setEdgeAttributes(debug)
        
    def getNetworkAttributes(self, debug=False):
        retval = {"Vertex": self.vertexAttributeProperites, "Edge": self.edgeAttributeProperites}
        return retval