from network import network
from geocluster import geoClusters, geoCluster
from networkAlgos import networkAlgos
from networkCategories import categories
from collections import OrderedDict
from pandasUtils import getRowData, getColData, dropColumns, fixType, isDataFrame

from place import getPlaceData
from cbsa import getCBSAData
from csa import getCSAData
from metdiv import getMetDivData
from county import getCountyData
from state import getStateData


class driverNetwork(network):
    def __init__(self, trips, debug=False):
        network.__init__(self, directed=False, debug=False)
        
        self.categories        = categories(debug)
        self.getCategories     = self.categories.getCategories
        self.getCategory       = self.categories.getCategory
        self.getPermCategories = self.categories.getPermCategories
        self.getPermCategory   = self.categories.getPermCategory  
        self.getHomeRatioCategory = self.categories.getHomeRatioCategory
        self.getIntervalCategory = self.categories.getIntervalCategory
        
        self.nodeAttrs = None
        self.edgeAttrs = None
        self.netAttrs  = None
        
        self.gc = None
                
        if trips is not None:
            if isinstance(trips, dict):
                self.name          = trips.get('device')
                self.edgeMetrics   = trips.get('edgeMetrics')
                self.vertexMetrics = trips.get('vertexMetrics')
                self.vertexMetrics = {str(k): v for k,v in self.vertexMetrics.items()}
                self.homeMetrics   = trips.get('homeMetrics')
                print("Creating a driver network with {0} vertices and {1} edges.".format(len(self.vertexMetrics), len(self.edgeMetrics)))
            else:
                raise ValueError("Input trips must be a dictionary of edgeMetrics, vertexMetrics, and homeMetrics (optional)")
        else:
            raise ValueError("Input trips is None!")

            
    ################################################################################################
    # Cluster/Node Info
    ################################################################################################    
    def createGC(self, debug=False):
        self.gc = geoClusters(key="FromDriverNetwork")
        clusterPrefix = "cl"
        clusters = OrderedDict()
        for vertexName in self.getVertices():
            vertexData = self.getVertexByName(vertexName, "attr")
            try:
                clnum = int(vertexName.replace(clusterPrefix, ""))
            except:
                continue
            
            cluster   = geoCluster(seed=None, cnts=None, clnum=clnum, clusterPrefix=clusterPrefix, debug=debug)
            cluster.setRadius(vertexData["Radius"])
            cluster.setCells(vertexData["Geohashs"])
            cluster.setQuantiles(vertexData["Quantiles"])
            cluster.setCoM(vertexData["CoM"])
            
            clusters[cluster.getName()] = cluster

        self.gc.setClusters(clusters)
            
            
#        vtxMetrics[geoID]["CoM"]            = gc.getClusterCoM(geoID)
#        vtxMetrics[geoID]["Radius"]         = gc.getClusterRadius(geoID)
#        vtxMetrics[geoID]["Cells"]          = gc.getClusterCells(geoID)
#        vtxMetrics[geoID]["Quantiles"]      = gc.getClusterQuantiles(geoID)
#        vtxMetrics[geoID]["Geohashs"]       = gc.getClusterCellNames(geoID)
#        try:
#        dn.getVertexByName('cl33', 'attr')

    def getGC(self):
        return self.gc

            
    ################################################################################################
    # Getters
    ################################################################################################    
    def getNodeAttrs(self):
        return self.nodeAttrs
        
    def getNodeDict(self):
        return self.vInfo.nodeDict
        
    def getEdgeAttrs(self):
        return self.edgeAttrs
        
    def getNetAttrs(self):
        return self.netAttrs
        
            
    ####################################################################################
    # Create Network
    ####################################################################################
    def create(self, debug=False):
        if debug:
            print("Creating Network Attributes")
        for edgename,edgedata in self.edgeMetrics.items():
            self.addEdge(edgename, edgedata)
        self.updateVertexAttrs(self.vertexMetrics, debug=debug)
        self.update(debug=debug)
        self.flattenAttrs(debug=debug)
        self.collectAttrs(debug=debug)

        
    ####################################################################################
    # Compute Network Attributes
    ####################################################################################
    def computeNetworkAttrs(self, level=2, debug=False):
        if debug:
            if level == 1:
                print("Computing Network Attributes (simple)")
            elif level == 2:
                print("Computing Network Attributes (medium)")
            elif level == 3:
                print("Computing Network Attributes (hard)")
        self.netAlgos = networkAlgos()
        results = self.netAlgos.compute(self.g, level=level, debug=debug)
        self.nodeAttrs = results['Nodes']
        self.edgeAttrs = results['Edges']
        self.edgeAttrs['edge_weight'] = self.eInfo.getEdgeWeights().values() # add weights
        self.netAttrs  = results['Net']
        if debug:
            print("  Created {0} attributes for {1} vertices".format(self.nodeAttrs.shape[1], self.nodeAttrs.shape[0]))
            print("  Created {0} attributes for {1} edges".format(self.edgeAttrs.shape[1], self.edgeAttrs.shape[0]))
            print("  Created {0} attributes for the network".format(len(self.netAttrs)))


    ####################################################################################
    # Perform Lookup for Census Data
    ####################################################################################
    def fillVertexCensusData(self, debug=False):
        if debug:
            print("Filling Vertex Census Data")
        verydebug=False
        
        censusKeys = [k for k,v in self.getVertexAttrsGroups().items() if v == "Census"]
        getCensusData = {"CENSUSCbsa": getCBSAData, "CENSUSCsa": getCSAData, "CENSUSCounty": getCountyData, 
                         "CENSUSMetdiv": getMetDivData, "CENSUSPlace": getPlaceData, "CENSUSState": getStateData}
        for key in censusKeys:
            if getCensusData.get(key) is None:
                continue
            for vertexName in self.getVertices():
                vertex = self.getVertexByName(vertexName, 'attr')
                if verydebug:
                    print("  --> Vertex Name {0}".format(vertexName))

                value   = vertex[key]
                
                
                if isinstance(value, list):
                    try:
                        #mc    = value.most_common(1)
                        value = value[0][0]
                    except:
                        print("There was an error getting most common {0}".format(key))
                        value = None        
                else:
                    print("Input {0} is type {1}".format(value, type(value)))
                    
                try:
                    lookup       = getCensusData[key](str(value))
                    features     = self.categories.getFeatures(key.replace("CENSUS", "Census"), lookup, debug)
                except:
                    raise ValueError("Something went wrong with census lookup for {0} and value {1}".format(key, value))

                for lookupName,lookupValue in features.items():
                    featureName = "".join([key,lookupName])
                    self.setVertexFeature(vertexName=vertexName, category="Census", key=featureName, value=lookupValue)
                
                if verydebug is True:
                    print("\t: {0}, {1} == {2} ({3})".format(key, value, lookup, features))
                    
                    
        ### Fill CENSUS Region
        if True:
            for vertexName in self.getVertices():
                state  = self.getVertexFeature(vertexName=vertexName, category="Census", key="State")
                region = self.categories.getFeatures("CensusRegion", state, debug=True)
                value  = region['Region']
                self.setVertexFeature(vertexName=vertexName, category="Census", key="Region", value=value)
                    
        if verydebug:
            raise ValueError("Stoppping after verydebug is True")
            

            
    ####################################################################################
    # Format and Fill GeoSpatial Data
    ####################################################################################
    def fillVertexGeospatialData(self, debug=False):
        if debug:
            print("Filling Vertex Geospatial Data")
        verydebug=False
        
        groupings = ["HEREPOI", "OSM", "Roads", "Rail", "Terminals"]
        for grouping in groupings:
            keys = [k for k,v in self.getVertexAttrsGroups().items() if v == grouping]            
            for vertexName in self.getVertices():
                vertex = self.getVertexByName(vertexName, 'attr')
                if verydebug:
                    print("  --> Vertex Number {0} and ID {1}".format(vertexNum, vertexID))

                for key in keys:
                    value   = vertex[key]

                    result = None
                    if isinstance(value, list):
                        try:
                            test = value[0][0]
                            if test is None:
                                result = 0 #'N'
                            else:
                                if test == 1.0:
                                    result = 1 #'Y'
                                else:
                                    result = 0 #'N'
                        except:
                            result = 0 #'N'
                    else:
                        print("Input {0} is type {1}".format(value, type(value)))

                    self.setVertexFeature(vertexName=vertexName, category="GeoSpatial", key=key, value=result)
                    if verydebug is True:
                        print("\t: {0}, {1} == {2}".format(key, value, result))
                    
        if verydebug:
            raise ValueError("Stoppping after verydebug is True")            
            

            
    ####################################################################################
    # Format and Fill Internal Vertex Data
    ####################################################################################
    def fillVertexInternalData(self, debug=False):
        if debug:
            print("Filling Vertex Internal Data")
        verydebug=False

        keys = [k for k,v in self.getVertexAttrsGroups().items() if v == "General"]
        for vertexName in self.getVertices():
            vertex = self.getVertexByName(vertexName, 'attr')
            if verydebug:
                print("  --> Vertex Number {0}".format(vertexName))

            for key in keys:
                value   = vertex[key]
                feature = self.categories.getFeatures(key, value, debug)
                if isinstance(feature, dict):
                    if feature.get('Name') is None:
                        feature = value
                    else:
                        feature = feature['Name']
                self.setVertexFeature(vertexName=vertexName, category="Internal", key=key, value=feature)
                   
        if verydebug:
            raise ValueError("Stoppping after verydebug is True")                  
            

            
    ####################################################################################
    # Format and Fill Network Algos Vertex Data
    ####################################################################################
    def fillVertexNetworkData(self, debug=False):
        if debug:
            print("Filling Vertex Network Data")
        verydebug=False

        vertexNetworkDF = self.getVertexNetworkDataFrame()
        if not isDataFrame(vertexNetworkDF):
            if debug:
                print("There is no vertex network DataFrame!")
            return
        
        for vertexName in self.getVertices():
            vertexData = getRowData(vertexNetworkDF, rownames=vertexName)
            if verydebug:
                print("  --> Vertex Name {0}".format(vertexName))

            for key in vertexData.index:
                value = vertexData[key]
                featureName = ''.join([s.title() for s in key.split("_")])
                self.setVertexFeature(vertexName=vertexName, category="Network", key=featureName, value=value)
                    
        if verydebug:
            raise ValueError("Stoppping after verydebug is True")                      
            

            
            
            
    ####################################################################################
    ####################################################################################
    # Format and Fill Edge Vertex Data
    ####################################################################################                    
    ####################################################################################
    def fillEdgeVertexData(self, debug=False):
        if debug:
            print("Filling Edge Data")
        verydebug=False

        for edgeName in self.getEdges():
            try:
                features = [self.getVertexByName(x, 'feat') for x in tuple(edgeName)]
            except:
                if debug:
                    print("  There are no vertex features!")
                return
            categories = features[0].keys()
            categories = ["Census", "GeoSpatial"]
            for category in categories:
                featureNames = features[0][category]
                for featureName in featureNames:
                    values = [features[i][category][featureName] for i in range(2)]
                    self.setEdgeFeature(edgeName=edgeName, category=category, key=featureName, value=values)
                    if verydebug is True:
                        print("\t: {0}, {1}, {2}".format(edgeName, key, values))
                    
        if verydebug:
            raise ValueError("Stoppping after verydebug is True")                              
            

    def fillEdgeNetworkData(self, debug=False):
        if debug:
            print("Filling Edge Network Data")
        verydebug=False

        edgeNetworkDF = self.getEdgeNetworkDataFrame()
        if not isDataFrame(edgeNetworkDF):
            if debug:
                print("There is no edge network DataFrame!")
            return
        
        for edgeName in self.getEdges():
            #edgeData = getRowData(edgeNetworkDF, rownames=str(tuple(edgeName)))
            edgeData = getRowData(edgeNetworkDF, rownums=list(edgeNetworkDF.index).index(edgeName)) # Still ???
            if verydebug:
                print("  --> Edge Name {0}".format(edgeName))

            for key in edgeData.index:
                value = edgeData[key]
                featureName = ''.join([s.title() for s in key.split("_")])
                self.setEdgeFeature(edgeName=edgeName, category="Network", key=featureName, value=value)
                    
        if verydebug:
            raise ValueError("Stoppping after verydebug is True")                            
            

    def fillEdgeInternalData(self, debug=False):
        if debug:
            print("Filling Edge Internal Data")
        verydebug=False

        for edgeName in self.getEdges():
            edgeDataDF = self.getEdgeByName(edgeName, 'attr')
            if verydebug:
                print("  --> Edge Name {0}".format(edgeName))
                
            if not isDataFrame(edgeDataDF):
                if debug:
                    print("There is no edge internal DataFrame!")
                return
            
            keys = edgeDataDF.columns
            for key in keys:
                value   = getColData(edgeDataDF, colnames=key)[0]
                feature = self.categories.getFeatures(key, value, debug)
                if isinstance(feature, dict):
                    if feature.get('Name') is None:
                        continue
                    else:
                        feature = feature['Name']
                if isinstance(feature, list):
                    continue
                self.setEdgeFeature(edgeName=edgeName, category="Internal", key=key, value=feature)
            
            
       
        
    #################################################################################################################
    # DataFrame Functions
    #################################################################################################################
    def getVertexInternalDataFrame(self, debug=False):
        return self.vInfo.vertexAttrsDF

    def getVertexNetworkDataFrame(self, debug=False):
        return self.nodeAttrs

    def getEdgeInternalDataFrame(self, debug=False):
        return self.eInfo.edgeAttrsDF

    def getEdgeNetworkDataFrame(self, debug=False):
        return self.edgeAttrs

    def getNetworkDataFrame(self, debug=False):
        return self.netAttrs