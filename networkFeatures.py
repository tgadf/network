from vertexData import vertex
from edgeData import edge
from networkCategories import categories

class networkFeatures():
    def __init__(self, network, expectedFeatures = None, debug=False, writeSummary=False):
        self.network  = network
        self.g        = network.getNetwork()
        self.writeSummary = writeSummary
                
        self.features = {}
        self.device   = self.network.getDevice()
        
        self.numVertices               = self.network.numVertices
        self.getVertexID               = self.network.getVertexID
        self.vertexMetrics             = self.network.vertexMetrics
        self.vertexAttributes          = self.network.vertexAttributes
        self.vertexAttributeProperites = self.network.vertexAttributeProperites
        self.getVertexID               = self.network.getVertexID
        self.getVertexNum              = self.network.getVertexNum
        self.vertexIDToNum             = self.network.vertexIDToNum
        self.vertexNumToID             = self.network.vertexNumToID
        
        self.numEdges                = self.network.numEdges
        self.getEdgeID               = self.network.getEdgeID
        self.edgeMetrics             = self.network.edgeMetrics
        self.edgeAttributes          = self.network.edgeAttributes
        self.edgeAttributeProperites = self.network.edgeAttributeProperites
        self.getEdgeID               = self.network.getEdgeID
        self.getEdgeIdx              = self.network.getEdgeIdx
        self.getEdgeIDByIdx          = self.network.getEdgeIDByIdx
        self.getEdgeByIdx            = self.network.getEdgeByIdx
        self.getEdgeVerticesByID     = self.network.getEdgeVerticesByID
        self.getEdgeVertexIDsByID    = self.network.getEdgeVertexIDsByID
        self.getEdgeNumByID          = self.network.getEdgeNumByID
        
        #self.getVertexExternalData      = self.network.getVertexExternalData
        #self.getVertexExternalDataByKey = self.network.getVertexExternalDataByKey
        self.setVertexExternalData      = self.network.setVertexExternalData
        self.getEdgeExternalData        = self.network.getEdgeExternalData
        self.getEdgeExternalDataByKey   = self.network.getEdgeExternalDataByKey
        self.setEdgeExternalData        = self.network.setEdgeExternalData
        self.getNetworkExternalData     = self.network.getNetworkExternalData
        self.setNetworkExternalData     = self.network.setNetworkExternalData
        
        self.externalTranslationData  = {}
        self.expectedFeatures         = expectedFeatures
        
        self.mapFeatures             = None

        self.vertexFeatureAttrMap    = {}
        self.edgeFeatureAttrMap      = {}
        
        
        
        ################################################################################################################
        ## This is the data that is set in networkTrips
        ################################################################################################################
        self.externalVertexData = {}
        
        ## External Data
        keys=['CBSA', 'CSA', 'County', 'MetDiv', 'Place', 'State']
        self.externalVertexData["Census"] = ["{0}{1}".format("Census", key.title()) for key in keys]
        
        keys=['Attraction', 'Auto', 'Building', 'College', 'Commercial', 'Cycling', 'Entertainment', 'Fastfood', 'Fuel', 'Grocery', 'Industrial', 'Lodging', 'Medical', 'Municipal', 'Parking', 'Recreation', 'Restaurant', 'School', 'Sport', 'Transit']
        self.externalVertexData["HEREPOI"] = ["{0}{1}".format("HEREPOI", key.title()) for key in keys]
        
        keys=['Interstate', 'Usrte', 'Staterte', 'Highway', 'MajorRd']    
        self.externalVertexData["Road"] = ["{0}{1}".format("ROADS", key) for key in keys]
        
        keys=['Fuel', 'Parking', 'Bus', 'Ferry', 'Rail', 'Taxi', 'Tram', 'Buddhist', 'Christian', 'Hindu', 'Jewish', 'Muslim', 'Sikh', 'Taoist', 'Attraction', 'Auto', 'Building', 'College', 'Commercial', 'Entertainment', 'Fastfood', 'Grocery', 'Industrial', 'Lodging', 'Medical', 'Municipal', 'Public', 'Recreation', 'Religious', 'Restaurant', 'School', 'Sport']
        self.externalVertexData["OSM"] = ["{0}{1}".format("OSM", key) for key in keys]
        
        keys=['Airport', 'Amtrak']
        self.externalVertexData["Terminal"] = ["{0}{1}".format("Terminals", key) for key in keys]

        self.externalVertexData['POI'] = ['POIUniqueVisits']
        
        
        self.externalVertexKeys = self.externalVertexData.keys()
    
    
        
        
        
        ################################################################################################################
        ## This is the data that comes from the user information for each vertex
        ################################################################################################################    
        
        ## Vertex Features
        self.internalVertexKeys = self.vertexAttributes.keys()
        self.externalVertexClusterKeys  = ["CoM", "Radius", "Cells", "Quantiles"]
        self.externalVertexInternalKeys = ["DwellTime", "DayOfWeek", "DrivingDistance", "GeoDistanceRatio", "FractionalActive"]
        self.externalVertexNetworkKeys  = self.externalVertexInternalKeys + self.externalVertexClusterKeys
        
        ## Edge Features
        self.externalEdgeNetworkKeys    = ["DwellTime", "Duration", "GeoDistance", "DrivingDistance", "GeoDistanceRatio", "ITA", "Weight", "FractionalActive"]
        self.externalEdgeExternalVertexKeys = []
        for key,keys in self.externalVertexData.items():            
            self.externalEdgeExternalVertexKeys += keys
        
        
        
        ################################################################################################################
        ## This is the data that comes from the POI information for each vertex
        ################################################################################################################    
        self.externalVertexPOIKeys = ["25", "100", "250", "500"]
        
        
                     
        
        
        ################################################################################################################
        ## These are internal functions for attributes and features
        ################################################################################################################    
        self.attrTypes = {}
        
        self.internalEdgeKeys = self.edgeAttributes.keys()   
        
        self.categories        = categories(debug)
        self.getCategories     = self.categories.getCategories
        self.getCategory       = self.categories.getCategory
        self.getPermCategories = self.categories.getPermCategories
        self.getPermCategory   = self.categories.getPermCategory  
        self.getHomeRatioCategory = self.categories.getHomeRatioCategory
        self.getIntervalCategory = self.categories.getIntervalCategory
        
        self.baseWriteDir = "/home/tgadf/pol/plots/{0}".format(self.device)
        if self.writeSummary is True:
            from os import mkdir, rmdir
            try:
                rmdir(self.baseWriteDir)
                print("Removed {0}".format(self.baseWriteDir))
            except:
                pass
            
            try:
                mkdir(self.baseWriteDir)
                print("Created {0}".format(self.baseWriteDir))
            except:
                pass
        
        self.homeMetrics  = self.network.homeMetrics
        self.homeVertexID = self.network.homeVertexID
        self.homePOI      = None
        self.homeRank     = None
        
        self.vertices     = {}
        self.edges        = {}
        
        for vertexNum in range(self.numVertices):
            vertexID = self.getVertexID(vertexNum)
            self.vertices[vertexID] = vertex(vertexID, vertexNum)
        
        for edgeNum in range(self.numEdges):
            edgeID   = self.getEdgeID(edgeNum)
            edgeIdx  = self.getEdgeIdx(edgeNum)
            vertices = self.getEdgeVerticesByID(edgeID)
            self.edges[edgeID] = edge(edgeID, edgeIdx, edgeNum, vertices)
            
        
        if debug is True:
            print("Network Features for {0}".format(self.device), flush=True)


    ####################################################################################
    #
    # Getters
    #
    ####################################################################################
    def getFeatures(self):
        return self.features
    
    def getVertex(self, vertexID):
        try:
            retval = self.vertices[vertexID]
        except:
            retval = vertex(None, None)
        return retval
    
    def getEdge(self, edgeID):
        try:
            retval = self.edges[edgeID]
        except:
            retval = edge(None, None, None, None)
        return retval
    
    
    def printFeatures(self):
        print("=============== {0} ===============".format(self.device))
        print("{0:<5}{1:<10}{2}".format("#", "Value", "Feature"))
 
        i = 0
        for category, categorydata in self.features.items():
            for feature, featuredata in categorydata.items():
                if isinstance(featuredata, dict):
                    for subfeature, subfeaturedata in featuredata.items():
                        key = "".join([category,feature,subfeature])
                        try:
                            value = round(subfeaturedata,4)
                        except:
                            value = subfeaturedata
                        print("{0:<5}{1:<50}{2}".format(i, str(value), key))
                        i += 1
                else:
                    try:
                        value = round(featuredata,4)
                    except:
                        value = featuredata
                    key = "".join([category,feature])
                    print("{0:<5}{1:<50}{2}".format(i, str(value), key))
                    i += 1


    def printFeatureResult(self, key, retval, debug=False):
        if retval is None:
            if debug:
                print("Creating features for type {0}".format(key), flush=True)
        else:
            if debug:
                print("Created {0} features for type {1}".format(len(retval), key), flush=True)
            

    ####################################################################################
    #
    # Export Vertices/Edges
    #
    ####################################################################################
    def export(self, debug=False):
        if debug:
            print("Exporting Edges and Vertices")
        for edgeID,edge in self.edges.items():
            self.network.setEdge(edgeID, edge)
        for vertexID,vertex in self.vertices.items():
            self.network.setVertex(vertexID, vertex)
            

    ####################################################################################
    #
    # Set External Data
    #
    ####################################################################################
    def setExternalTranslationData(self, name, extData):
        self.externalTranslationData[name] = extData
    def setCensusData(self, censusData):
        for key in self.externalVertexData['Census']:
            self.externalTranslationData[key] = censusData.get(key)
    def setHEREData(self, hereData):
        for key in self.externalVertexData['HEREPOI']:
            self.externalTranslationData[key] = hereData.get(key)
    def setVenueData(self, venueData):
        for key in self.externalVertexData['Venue']:
            self.externalTranslationData[key] = venueData.get(key)
    def setCollegeData(self, collegeData):
        for key in self.externalVertexData['College']:
            self.externalTranslationData[key] = collegeData.get(key)
    def setSchoolData(self, schoolData):
        for key in self.externalVertexData['School']:
            self.externalTranslationData[key] = schoolData.get(key)
    def setAutoData(self, autoData):
        for key in self.externalVertexData['Auto']:
            self.externalTranslationData[key] = autoData.get(key)
    def setRailData(self, railData):
        for key in self.externalVertexData['Rail']:
            self.externalTranslationData[key] = railData.get(key)
    def setRoadData(self, roadData):
        for key in self.externalVertexData['Road']:
            self.externalTranslationData[key] = roadData.get(key)
        
            
            
    ####################################################################################
    # Fill External Network Data for Edges and Vertices
    ####################################################################################
    def fillExternalGeospatialData(self, debug=False):
        if debug:
            print("Filling Vertex Geospatial Data")
        verydebug=False
            
        if self.vertexMetrics is None:
            raise ValueError("Could not set external data because vertex metrics is None!!!")
        for vertexNum in range(self.numVertices):            
            vertexID   = self.getVertexID(vertexNum)
            if verydebug:
                print("  --> Vertex Number {0} and ID {1}".format(vertexNum, vertexID))
                
            vertex     = self.getVertex(vertexID)
            vertexData = self.vertexMetrics[vertexID]
            for extKey in self.externalVertexKeys:
                vtxExtData = self.vertexMetrics[vertexID][extKey]
                for key, value in vtxExtData.items():
                    if self.externalTranslationData.get(key) is not None:
                        val = self.externalTranslationData[key].get(value)
                        vertex.setExternalDataByKey(key, val)
                    else:
                        vertex.setExternalDataByKey(key, value)
                    if verydebug is True:
                        print("\t: {0}, {1}, {2}".format(extKey, key,vertex.getExternalDataByKey(key)))
            
            
    ####################################################################################
    # Fill External Network Data for Edges and Vertices
    ####################################################################################
    def fillExternalNetworkData(self, debug=False):
        if debug:
            print("Filling Vertex and Edge Metrics Data")
        verydebug=False
        
        if self.vertexMetrics is None:
            raise ValueError("Could not set external data because vertex metrics is None!!!")
        for vertexNum in range(self.numVertices):
            vertexID   = self.getVertexID(vertexNum)
            if verydebug:
                print("  --> Vertex Number {0} and ID {1}".format(vertexNum, vertexID))
            vertex     = self.getVertex(vertexID)
            for key in self.externalVertexNetworkKeys:
                value = self.vertexMetrics[vertexID].get(key)
                vertex.setExternalDataByKey(key, value)
                if verydebug is True:
                    print("\t: {0}, {1}".format(key,vertex.getExternalDataByKey(key)))
            
        for edgeNum in range(self.numEdges):
            edgeID   = self.getEdgeID(edgeNum)
            if verydebug:
                print("  --> Edge Number {0} and ID {1}".format(edgeNum, edgeID))
            edge     = self.getEdge(edgeID)  
            for key in self.externalEdgeNetworkKeys:
                value = self.edgeMetrics[edgeID].get(key)
                edge.setExternalDataByKey(key, value)
                if verydebug is True:
                    print("\t: {0}, {1}".format(key,edge.getExternalDataByKey(key)))
            
            
            
    ####################################################################################
    # Perform Lookup for Census Data
    ####################################################################################
    def fillExternalCensusData(self, debug=False):
        if debug:
            print("Filling External Census Data")
        verydebug=False

        from collections import Counter
        try:
            from lookupCBSA import getCBSAData
            from lookupCSA import getCSAData
            from lookupCounty import getCountyData
            from lookupMetDiv import getMetDivData
            from lookupPlace import getPlaceData
            from lookupState import getStateData
        except:
            pass
        
        keys=['CBSA', 'CSA', 'County', 'MetDiv', 'Place', 'State']
        getCensusData = {"CensusCbsa": getCBSAData, "CensusCsa": getCSAData, "CensusCounty": getCountyData, "CensusMetdiv": getMetDivData, "CensusPlace": getPlaceData, "CensusState": getStateData}
        for key in self.externalVertexData["Census"]:
            for vertexNum in range(self.numVertices):
                vertexID   = self.getVertexID(vertexNum)
                vertex  = self.getVertex(vertexID)
                if verydebug:
                    print("  --> Vertex Number {0} and ID {1}".format(vertexNum, vertexID))
                    
                value   = vertex.getExternalDataByKey(key)
                ## expect a Counter object
                if isinstance(value, Counter):
                    try:
                        mc    = value.most_common(1)
                        value = mc[0][0]
                    except:
                        print("There was an error getting most common {0}".format(key))
                        value = None
                        
                else:
                    print("Input is of type {0}".format(type(value)))
                try:
                    lookup  = getCensusData[key](str(value))
                except:
                    lookup  = value
                vertex.setExternalDataByKey(key, lookup)                    
                if verydebug is True:
                    print("\t: {0}, {1} == {2}".format(key, value, lookup))
                    
        if verydebug:
            raise ValueError("Stoppping after verydebug is True")
            
            
    ####################################################################################
    # Fill Internal Network Data for Edges and Vertices
    ####################################################################################
    def fillInternalData(self, debug=False):
        if debug:
            print("Filling Internal Vertex/Edge Data")
        verydebug=False

        # Vertex Graph Features
        for attribute,attributedata in self.vertexAttributes.items():
            for vertexNum in range(self.numVertices):
                vertexID   = self.getVertexID(vertexNum)
                if verydebug:
                    print("  --> Vertex Number {0} and ID {1}".format(vertexNum, vertexID))
                vertex     = self.getVertex(vertexID)
                value      = attributedata[vertexID]
                vertex.setInternalDataByKey(attribute, value)
                vertex.setFeatureDataByKey(attribute, value)
                if verydebug is True:
                    print("\t: {0}, {1}".format(attribute,vertex.getInternalDataByKey(attribute)))
                    print("\t: {0}, {1}".format(attribute,vertex.getFeatureDataByKey(attribute)))
                
        # Edge Graph Features
        for attribute,attributedata in self.edgeAttributes.items():
            for edgeNum in range(self.numEdges):
                edgeID    = self.getEdgeID(edgeNum)
                if verydebug:
                    print("  --> Edge Number {0} and ID {1}".format(edgeNum, edgeID))
                edge      = self.getEdge(edgeID)
                value     = attributedata[edgeID]
                edge.setInternalDataByKey(attribute, value)
                edge.setFeatureDataByKey(attribute, value)
                if verydebug is True:
                    print("\t: {0}, {1}".format(attribute,edge.getInternalDataByKey(attribute)))
                    print("\t: {0}, {1}".format(attribute,edge.getFeatureDataByKey(attribute)))
                        
                    
                    
    ####################################################################################
    # Fill Expanded Vertex Data Vertices
    ####################################################################################
    def fillVertexFeatureData(self, debug=False):
        if debug:
            print("Filling Vertex Feature Data")
        verydebug=False
        from collections import Counter
        
        ## Vertex Features
        for vertexNum in range(self.numVertices):
            vertexID   = self.getVertexID(vertexNum)
            if verydebug:
                print("  --> Vertex Number {0} and ID {1}".format(vertexNum, vertexID))
            vertex     = self.getVertex(vertexID)
            
            for extKey in self.externalVertexKeys:
                for key in self.externalVertexData[extKey]:
                    externalData = vertex.getExternalDataByKey(key, debug)
                    ## expect a Counter object or dict/str if already processed (i.e., Census)
                    if isinstance(externalData, (Counter)):
                        if externalData.get(1.0):
                            externalData = 1
                        else:
                            externalData = 0
                    elif isinstance(externalData, (dict,str)):
                        pass
                    else:
                        print("Input for external vertex key {0} is {1} and of type {2}".format(key, externalData, type(externalData)))
                        externalData = None
                    features     = self.categories.getFeatures(key, externalData, debug)
                    vertex.setFeatureDataByKey(key, features)
                    if verydebug is True:
                        print("\t: {0}, {1}, {2}, {3} == {4}".format(extKey, key, externalData, features, vertex.getFeatureDataByKey(key)))
                        
            for key in self.externalVertexNetworkKeys:
                externalData = vertex.getExternalDataByKey(key, debug)
                features     = self.categories.getFeatures(key, externalData, debug)
                vertex.setFeatureDataByKey(key, features)
                if verydebug is True:
                    print("\t: {0}, {1} == {2}".format(key,features,vertex.getFeatureDataByKey(key)))
                                
            if verydebug is True:
                raise ValueError("Stopping because verydebug is True")
        self.flattenVertexFeatureData(debug)
        
        
                    
    ####################################################################################
    # Flatten Vertex Data (Features -> Attrs)
    ####################################################################################
    def flattenVertexFeatureData(self, debug=False):
        if debug:
            print("Flatten Vertex Feature Data")
        verydebug=False
        from numpy import uint, int64
        
        ## Vertex Features
        for vertexNum in range(self.numVertices):
            vertexID   = self.getVertexID(vertexNum)
            vertex     = self.getVertex(vertexID)
            if verydebug:
                print("  --> Vertex Number {0} and ID {1}".format(vertexNum, vertexID))

            for featureName,featureData in vertex.getFeatures().items():
                if isinstance(featureData, dict):
                    for subName,subData in featureData.items():
                        if subName == "Name":
                            key = "{0}".format(featureName)
                        else:
                            key = "{0}{1}".format(featureName, subName)
                        if self.vertexFeatureAttrMap.get(featureName) is None:
                            self.vertexFeatureAttrMap[featureName] = set()
                        self.vertexFeatureAttrMap[featureName].add(key)
                        vertex.setAttrDataByKey(key, subData)
                        if verydebug is True:
                            print("\t: {0}, {1} == {2}".format(key,subData, vertex.getAttrDataByKey(key)))
                elif isinstance(featureData, (str,float,int,uint,int64,tuple)):
                    key = featureName
                    if self.vertexFeatureAttrMap.get(featureName) is None:
                        self.vertexFeatureAttrMap[featureName] = set()
                    self.vertexFeatureAttrMap[featureName].add(key)
                    vertex.setAttrDataByKey(key, featureData)
                    if verydebug is True:
                        print("\t: {0}, {1} == {2}".format(key,featureData, vertex.getAttrDataByKey(key)))
                else:
                    raise ValueError("Did not understand data {0} ({1}) when setting attrs for vertex".format(type(featureData), featureData))
                    
                    
    ####################################################################################
    # Fill Expanded Edge Data Vertices
    ####################################################################################
    def fillEdgeFeatureData(self, debug=False):
        if debug:
            print("Filling Edge Feature Data")
        verydebug=False
        ## Edge Features
        for edgeNum in range(self.numEdges):
            edgeID    = self.getEdgeID(edgeNum)
            edge      = self.getEdge(edgeID)
            if verydebug:
                print("  --> Edge Number {0} and ID {1}".format(edgeNum, edgeID))

            #self.externalVertexNetworkKeys = ["DwellTime", "DayOfWeek", "CoM"]
            for key in self.externalEdgeNetworkKeys:
                externalData = edge.getExternalDataByKey(key, debug)
                features     = self.categories.getFeatures(key, externalData, debug)
                edge.setFeatureDataByKey(key, features)
                if verydebug is True:
                    print("\t: {0}, {1} == {2}".format(key,features,edge.getFeatureDataByKey(key)))
           
        self.flattenEdgeFeatureData(debug)
            
                    
                    
    ####################################################################################
    # Flatten Edge Data (Features -> Attrs)
    ####################################################################################
    def flattenEdgeFeatureData(self, debug=False):
        if debug:
            print("Flatten Edge Feature Data")
        verydebug=False
        from numpy import uint, int64
            
        for edgeNum in range(self.numEdges):
            edgeID   = self.getEdgeID(edgeNum)
            if verydebug:
                print("  --> Edge Number {0} and ID {1}".format(edgeNum, edgeID))
            edge     = self.getEdge(edgeID)
            for featureName,featureData in edge.getFeatures().items():
                if isinstance(featureData, dict):
                    for subName,subData in featureData.items():
                        if subName == "Name":
                            key = "{0}".format(featureName)
                        else:
                            key = "{0}{1}".format(featureName, subName)
                        if self.edgeFeatureAttrMap.get(featureName) is None:
                            self.edgeFeatureAttrMap[featureName] = set()
                        self.edgeFeatureAttrMap[featureName].add(key)
                        edge.setAttrDataByKey(key, subData)
                        if verydebug is True:
                            print("\t: {0}, {1} == {2}".format(key,subData, edge.getAttrDataByKey(key)))
                elif isinstance(featureData, (str,float,int,uint,int64,tuple)):
                    key = featureName
                    if self.edgeFeatureAttrMap.get(featureName) is None:
                        self.edgeFeatureAttrMap[featureName] = set()
                    self.edgeFeatureAttrMap[featureName].add(key)
                    edge.setAttrDataByKey(key, featureData)
                    if verydebug is True:
                        print("\t: {0}, {1} == {2}".format(key,featureData, edge.getAttrDataByKey(key)))
                else:
                    raise ValueError("Did not understand data {0} ({1}) when setting attrs for edge".format(type(featureData), featureData))
                        
            vertices     = edge.getVertices()
            edgeVertices = [self.vertices[self.getVertexID(vertexNum)] for vertexNum in vertices]            
            vertexAttrs  = [v.getAttrs() for v in edgeVertices]
            featureNames = vertexAttrs[0].keys()
                        
            ## Set CoM by hand
            vertexCoM  = [v.getFeatureDataByKey("CoM") for v in edgeVertices]
            edge.setAttrDataByKey("CoM", vertexCoM)
            
            for featureName in featureNames:
                if featureName in self.externalEdgeExternalVertexKeys:
                    if verydebug:
                        print("\t: {0}".format(featureName))
                    if self.edgeFeatureAttrMap.get(featureName) is None:
                        self.edgeFeatureAttrMap[featureName] = set()
                    for attrName in self.vertexFeatureAttrMap[featureName]:
                        if edge.isSetFeature(attrName):
                            continue

                        self.edgeFeatureAttrMap[featureName].add(attrName)

                        attrs  = [str(v[attrName]) for v in vertexAttrs]
                        value  = self.getPermCategory(attrName, attrs)
                        edge.setAttrDataByKey(attrName, value)
                        if verydebug is True:
                            print("\t: {0}, {1} == {2}".format(attrName,value, edge.getAttrDataByKey(attrName)))
                            
           
            
    ####################################################################################
    #
    # Vertex/Edge Attrs For Output
    #
    ####################################################################################
    def getVertexAttrs(self, vertexNum, debug=False):
        vertexID = self.getVertexID(vertexNum)
        return self.getVertexAttrsByID(vertexID, debug)
    
    def getVertexAttrsByID(self, vertexID, debug=False):
        vertex    = self.getVertex(vertexID)
        vertexNum = vertex.getNum()
        key = "  Vertex{0}".format(vertexNum)
        self.printFeatureResult(key, None, debug)
        
        retval = {}
        error  = 0
        
        retval['ID']   = vertexID
        retval['Rank'] = vertexNum
        for attrName, attrValue in vertex.getAttrs().items():
            retval[attrName] = attrValue
        
        retval['Error']     = error
        self.printFeatureResult(key, retval, debug)
        
        return retval
            
    def getEdgeAttrs(self, edgeNum, debug=False):
        edgeID = self.getEdgeID(edgeNum)
        return self.getEdgeAttrsByID(edgeID, debug)
    
    def getEdgeAttrsByID(self, edgeID, debug=False):
        edge    = self.getEdge(edgeID)
        edgeNum = edge.getNum()
        key = "  Edge{0}".format(edgeNum)
        self.printFeatureResult(key, None, debug)
        
        retval = {}
        error  = 0
        
        retval['ID']   = edgeID
        retval['Rank'] = edgeNum
        for attrName, attrValue in edge.getAttrs().items():
            retval[attrName] = attrValue
            
        retval['Error']     = error
        self.printFeatureResult(key, retval, debug)
        
        return retval




        
    
    
    ####################################################################################################################
    #
    # Vertex Counter Features
    #
    ####################################################################################################################
    def setVertexExternalDataCounts(self, debug=False):
        key = "VertexCounts"
        self.printFeatureResult(key, None, debug)
        from collections import Counter
        verydebug=False

        attrCntr    = {}
        attrTopCntr = {}
        retval      = {}
                    
            
            
                    
        for vertexNum in range(self.numVertices):
            vertexID = self.getVertexID(vertexNum)
            if verydebug:
                print("  --> Vertex Number {0} and ID {1}".format(vertexNum, vertexID))
            vertex   = self.getVertex(vertexID)
            attrs    = vertex.getAttrs()
            if verydebug is True:
                print("\t: Attrs: {0}".format(len(attrs)))
            attrList = []
            
            for attrName,attrValue in attrs.items():
                ## Ignore the internal igraph attrs
                if attrName in self.internalVertexKeys or attrName in self.externalVertexClusterKeys:
                    continue
                ## Create counter if it isn't already there
                if attrCntr.get(attrName) is None:
                    attrCats = self.getCategories(attrName)
                    if isinstance(attrCats, list):
                        self.attrTypes[attrName]       = "Category"
                        attrCntr[attrName]        = Counter(dict(zip(attrCats, [0]*len(attrCats))))
                        attrTopCntr[attrName]     = {}
                        attrTopCntr[attrName][3]  = 0
                        attrTopCntr[attrName][10] = 0
                        attrTopCntr[attrName][25] = 0
                    else:
                        self.attrTypes[attrName]       = "Logical"
                        attrCntr[attrName]        = Counter()
                        attrTopCntr[attrName]     = {}
                        attrTopCntr[attrName][3]  = 0
                        attrTopCntr[attrName][10] = 0
                        attrTopCntr[attrName][25] = 0
                    
                ## Count the values if it's not None
                if attrValue is not None:
                    if verydebug is True:
                        print("\t: {0}, {1}, {2}".format(attrName,attrValue,attrCats))
                    attrCntr[attrName][attrValue] += 1

                    if isinstance(attrValue, (float,int)):
                        if int(attrValue) == 0:
                            continue
                    if isinstance(attrValue, str):
                        if attrValue == 'N':
                            continue                    
                    attrList.append(attrName)
                    if vertexNum < 3:
                        attrTopCntr[attrName][3] += 1
                    if vertexNum < 10:
                        attrTopCntr[attrName][10] += 1
                    if vertexNum < 25:
                        attrTopCntr[attrName][25] += 1
                        
            # Useful for future debugging
            vertex.setAttrsList(attrList)
                    
                    
                    
        
        for attrName,attrCnts in attrCntr.items():
            error = 0
            try:
                mc    = attrCnts.most_common(1)[0]
            except:
                mc    = None
                error = 1

            if mc is not None:
                value = mc[0]
                cnts  = mc[1]
            else:
                value = None
                cnts  = None
                error = 1
                
            nunique = len(attrCnts)
            counts  = sum(attrCnts.values())
            try:
                frac   = counts/self.numVertices
            except:
                frac   = 0.0
                error  = 1
                
            retval[attrName] = {}
            retval[attrName]["Error"]      = error
            retval[attrName]["Unique"]     = nunique
            retval[attrName]["Count"]      = counts
            retval[attrName]['Fraction']   = frac
            retval[attrName]['MostCommon'] = value
            retval[attrName]['CountTop3']  = attrTopCntr[attrName][3]
            retval[attrName]['CountTop10']  = attrTopCntr[attrName][10]
            retval[attrName]['CountTop25']  = attrTopCntr[attrName][25]
            
            if self.attrTypes[attrName] == "Category":
                for k,v in attrCntr[attrName].items():
                    retval[attrName]["".join([k,"Count"])] = v
                    try:
                        retval[attrName]["".join([k,"Fraction"])] = float(v)/counts
                    except:
                        retval[attrName]["".join([k,"Fraction"])] = 0.0
                    
        self.printFeatureResult(key, retval, debug)
        self.features[key] = retval
        
                    
        
        
    def setVertexFractions(self, debug=False):
        key = "VertexProperties"
        self.printFeatureResult(key, None, debug)
        
        retval = {}
        for attribute in self.internalVertexKeys:
            error = 0
            if self.numVertices >= 3:
                vertices = [self.vertices[self.getVertexID(x)] for x in range(3)]
            else:
                vertices = None
                
            if vertices is not None:
                attrdata = [v.getAttrDataByKey(attribute) for v in vertices]
            else:
                attrdata = None
                
            if attrdata is not None:
                try:
                    diffVtx0Vtx1  = float(attrdata[0] - attrdata[1])
                    diffVtx1Vtx2  = float(attrdata[1] - attrdata[2])
                    diffVtx0Vtx12 = float(attrdata[0] - attrdata[1] - attrdata[2])
                except:
                    diffVtx0Vtx1  = 0.0
                    diffVtx1Vtx2  = 0.0
                    diffVtx0Vtx12 = 0.0
                    #print(self.numVertices)
                    #print(vertices)
                    #print([x.showAttrs() for x in vertices])
                    #raise ValueError("Don't know what to do with vertex data: {0}".format(attrdata))
            else:
                diffVtx0Vtx1  = None
                diffVtx1Vtx2  = None
                diffVtx0Vtx12 = None
                error = 1
            
            if attribute == "Degree":
                lowval=2
                highval=20
                vhighval=200
            elif attribute == "Betweenness":
                lowval=1
                highval=1.5
                vhighval=3
            elif attribute == "Closeness":
                lowval=0.2
                highval=0.7
                vhighval=0.8
            elif attribute == "HubScore":
                lowval=0.1
                highval=0.5
                vhighval=0.9
            elif attribute == "Coreness":
                lowval=2
                highval=5
                vhighval=9
            elif attribute == "PageRank":
                lowval=0.01
                highval=0.1
                vhighval=0.25
            elif attribute == "Eccentricity":
                lowval=1
                highval=6
                vhighval=8
            elif attribute == "Centrality":
                lowval=0.01
                highval=0.5
                vhighval=0.9
            elif attribute == "Constraint":
                lowval=0.05
                highval=0.5
                vhighval=0.9
            elif attribute == "Trips":
                lowval=3
                highval=25
                vhighval=100
            elif attribute == "TripsRatio":
                lowval=1
                highval=1.5
                vhighval=2.0
            else:
                raise ValueError("No low/high value for {0}".format(attribute))
            
            fracLow  = 0.0
            highCnt  = 0
            vhighCnt = 0
            for vertexNum in range(self.numVertices):
                vertexID = self.getVertexID(vertexNum)
                vertex   = self.getVertex(vertexID)
                attr     = vertex.getAttrDataByKey(attribute)
                try:
                    if attr <= lowval:
                        fracLow += 1.0/self.numVertices
                    if attr >= highval:
                        highCnt += 1
                    if attr >= vhighval:
                        vhighCnt += 1
                except:
                    pass

            retval[attribute] = {"Error":            error,
                                 "DiffFirstSecond":  diffVtx0Vtx1,
                                 "DiffSecondThird":  diffVtx1Vtx2,
                                 "DiffTop3":         diffVtx0Vtx12,
                                 "LowFraction":      fracLow,
                                 "HighCount":        highCnt,
                                 "VeryHighCount":    vhighCnt}

        self.printFeatureResult(key, retval, debug)
        self.features[key] = retval
        
        
    def setVertexRatios(self, debug=False):
        key = "VertexUnique"
        self.printFeatureResult(key, None, debug)
            
        retval = {}
    
        error   = 0
        degrees = 0
        trips   = 0
        sigma   = 0
        for vertexNum in range(self.numVertices):
            vertexID = self.getVertexID(vertexNum)
            vertex   = self.getVertex(vertexID)
            degree   = vertex.getAttrDataByKey("Degree")
            trip     = vertex.getAttrDataByKey("Trips")
            degrees += degree
            trips   += trip
            sigma   += degree/trip
        try:
            ratio = degrees/trips
        except:
            ratio = None
            error    = 1
            
        retval["Degree"]   = degrees
        retval["Trips"]    = trips
        retval["Ratio"]    = ratio
        retval["Error"]    = error

        self.printFeatureResult(key, retval, debug)
        self.features[key] = retval

        
    def setVertexCorrelations(self, debug=False):
        key = "VertexCorrelations"
        self.printFeatureResult(key, None, debug)
            
        retval = {}

        error = 0
        for i,attribute1 in enumerate(self.vertexAttributes.keys()):
            for j,attribute2 in enumerate(self.vertexAttributes.keys()):
                if j <= i:
                    continue
                try:
                    corr = round(self.vertexAttributes[attribute1].corr(self.vertexAttributes[attribute2]),4)
                except:
                    corr = None
                    error = 1
                retval["".join([attribute1, attribute2])] = corr

        retval["Error"] = error
        self.printFeatureResult(key, retval, debug)
        self.features[key] = retval
                    
        
    def setVertexFeatures(self, debug=False):
        key = "Vertex"
        self.printFeatureResult(key, None, debug)
        retval = {}
        
        for vertexNum in range(5):
            features = self.getVertexAttrs(vertexNum, debug)
            retval["{0}".format(vertexNum)] = features

        self.printFeatureResult(key, retval, debug)
        self.features[key] = retval
        
        
        
        
        
        
    ####################################################################################
    #
    # Home Features
    #
    ####################################################################################
    def setHomeFeatures(self, debug=False):
        key = "Home"
        self.printFeatureResult(key, None, debug)
        retval = {}

        retval  = self.getVertexAttrsByID(self.homeVertexID)
        ratio = self.homeMetrics['Ratio']
        ratio_significance = self.getHomeRatioCategory(ratio, debug)
        retval["Ratio"]    = ratio_significance
        retval["Days"], _  = self.getIntervalCategory(self.homeMetrics['Days'], debug)
        #retval["Ratio"] = None
        #retval["Days"]  = None
            
        if False:
            tripsHome = 0
            allTrips  = 0
            for edgeNum in range(self.numEdges):
                edgeID = self.getEdgeID(edgeNum)
                edge   = self.getEdge(edgeID)
                edgeWeight = self.getEdgeExternalDataByKey(edgeNum, "EdgeWeight", debug)
                allTrips += edgeWeight
                if len([x for x in self.getEdgeVertexIDsByID(edgeID) if x == self.homeVertexID]) > 0:
                    tripsHome += edgeWeight
            try:
                retval["TripFraction"] = tripsHome / allTrips
            except:
                retval["TripFraction"] = 0.0

        self.printFeatureResult(key, retval, debug)
        self.features[key] = retval




        
    
    
    ####################################################################################################################
    #
    # Edge Features
    #
    ####################################################################################################################
    def setEdgeExternalDataCounts(self, debug=False):
        key = "EdgeCounts"
        self.printFeatureResult(key, None, debug)
        from collections import Counter
        verydebug=False

        attrTopCntr  = {}
        attrCntr = {}
        retval   = {}
                    
                
        for edgeNum in range(self.numEdges):
            edgeID = self.getEdgeID(edgeNum)
            if verydebug:
                print("  --> Edge Number {0} and ID {1}".format(edgeNum, edgeID))
            edge   = self.getEdge(edgeID)
            attrs  = edge.getAttrs()
            attrList = []
            
            for attrName,attrValue in attrs.items():
                ## Ignore the internal igraph attrs
                #if attrName in self.internalVertexKeys:
                #    continue
                ## Create counter if it isn't already there
                if attrCntr.get(attrName) is None:
                    attrCats = self.getPermCategories(attrName)
                    if isinstance(attrCats, list):
                        self.attrTypes[attrName]       = "Category"
                        attrCntr[attrName]        = Counter(dict(zip(attrCats, [0]*len(attrCats))))
                        attrTopCntr[attrName]     = {}
                        attrTopCntr[attrName][3]  = 0
                        attrTopCntr[attrName][10] = 0
                        attrTopCntr[attrName][25] = 0
                    else:
                        self.attrTypes[attrName]       = "Logical"
                        attrCntr[attrName]        = Counter()
                        attrTopCntr[attrName]     = {}
                        attrTopCntr[attrName][3]  = 0
                        attrTopCntr[attrName][10] = 0
                        attrTopCntr[attrName][25] = 0
                    
                if attrValue == "None--None":
                    continue
                if attrName in self.externalVertexClusterKeys or attrName in self.internalEdgeKeys:
                    continue
                    
                ## Count the values if it's not None
                if attrValue is not None:
                    if verydebug is True:
                        print("\t: {0}, {1}".format(attrName,attrValue))
                    if attrValue in ['N--N']:
                        continue
                    attrList.append(attrName)
                    attrCntr[attrName][attrValue] += 1
                    if edgeNum < 3:
                        attrTopCntr[attrName][3] += 1
                    if edgeNum < 10:
                        attrTopCntr[attrName][10] += 1
                    if edgeNum < 25:
                        attrTopCntr[attrName][25] += 1
                        
            # Useful for future debugging
            edge.setAttrsList(attrList)                        
            
        
        for attrName,attrCnts in attrCntr.items():
            error = 0
            try:
                mc    = attrCnts.most_common(1)[0]
            except:
                mc    = None
                error = 1

            if mc is not None:
                value = mc[0]
                cnts  = mc[1]
            else:
                value = None
                cnts  = None
                error = 1
                
            nunique = len(attrCnts)
            counts  = sum(attrCnts.values())
            try:
                frac   = counts/self.numVertices
            except:
                frac   = 0.0
                error  = 1
                
            retval[attrName] = {}
            retval[attrName]["Error"]       = error
            retval[attrName]["Unique"]      = nunique
            retval[attrName]["Count"]       = counts
            retval[attrName]['Fraction']    = frac
            retval[attrName]['MostCommon']  = value
            retval[attrName]['CountTop3']   = attrTopCntr[attrName][3]
            retval[attrName]['CountTop10']  = attrTopCntr[attrName][10]
            retval[attrName]['CountTop25']  = attrTopCntr[attrName][25]
            
            if self.attrTypes[attrName] == "Category":
                for k,v in attrCntr[attrName].items():
                    retval[attrName]["".join([k,"Count"])] = v
                    try:
                        retval[attrName]["".join([k,"Fraction"])] = float(v)/counts
                    except:
                        retval[attrName]["".join([k,"Fraction"])] = 0.0
                        
        self.printFeatureResult(key, retval, debug)
        self.features[key] = retval
        
        
    def setEdgeFractions(self, debug=False):
        key = "EdgeProperties"
        self.printFeatureResult(key, None, debug)
            
        retval = {}
        
        error = 0
        for attribute in self.internalEdgeKeys:
            if self.numEdges >= 3:
                edges = [self.edges[self.getEdgeID(x)] for x in range(3)]
            else:
                edges = None
                
            if edges is not None:
                attrdata = [e.getAttrDataByKey(attribute) for e in edges]
            else:
                attrdata = None
                
            if attrdata is not None:
                diffEdge0Edge1  = float(attrdata[0] - attrdata[1])
                diffEdge1Edge2  = float(attrdata[1] - attrdata[2])
                diffEdge0Edge12 = float(attrdata[0] - attrdata[1] - attrdata[2])
            else:
                diffEdge0Edge1  = None
                diffEdge1Edge2  = None
                diffEdge0Edge12 = None
                error = 1
                        
            if attribute == "Weight":
                lowval   = 3
                highval  = 10
                vhighval = 25
            elif attribute == "Betweenness":
                lowval   = 1
                highval  = 2
                vhighval = 3
            else:
                raise ValueError("No low/high value for {0}".format(attribute))
                

            fracLow  = 0.0
            highCnt  = 0
            vhighCnt = 0
            for edgeNum in range(self.numVertices):
                edgeID = self.getEdgeID(edgeNum)
                edge   = self.getEdge(edgeID)                
                attr   = edge.getAttrDataByKey(attribute)
                try:
                    if attr <= lowval:
                        fracLow += float(1.0/self.numVertices)
                    if attr >= highval:
                        highCnt += 1
                    if attr >= vhighval:
                        vhighCnt += 1
                except:
                    pass
                    
            retval[attribute] = {"Error":            error,
                                 "DiffFirstSecond":  diffEdge0Edge1,
                                 "DiffSecondThird":  diffEdge1Edge2,
                                 "DiffTop3":         diffEdge0Edge12,
                                 "LowFraction":      fracLow,
                                 "HighCount":        highCnt,
                                 "VeryHighCount":    vhighCnt}

        self.printFeatureResult(key, retval, debug)
        self.features[key] = retval
        
        
    def setEdgeRatios(self, debug=False):
        key = "EdgeUnique"
        self.printFeatureResult(key, None, debug)
            
        retval = {}
    
        error   = 0
        weight  = 0
        sigma   = 0
        for edgeNum in range(self.numEdges):
            edgeID  = self.getEdgeID(edgeNum)
            edge    = self.getEdge(edgeID)
            weight += edge.getAttrDataByKey("Weight")
            
        try:
            ratio = weight/self.numEdges
        except:
            ratio = None
            error    = 1
            
        retval["Trips"]    = weight
        retval["Ratio"]    = ratio
        retval["Error"]    = error
        
        
    def setEdgeCorrelations(self, debug=False):
        key = "EdgeCorrelations"
        self.printFeatureResult(key, None, debug)
            
        retval = {}

        error = 0
        for i,attribute1 in enumerate(self.edgeAttributes.keys()):
            for j,attribute2 in enumerate(self.edgeAttributes.keys()):
                if j <= i:
                    continue
                try:
                    corr = round(self.edgeAttributes[attribute1].corr(self.edgeAttributes[attribute2]),4)
                except:
                    corr = None
                    error = 1
                retval["".join([attribute1, attribute2])] = corr

        retval["Error"] = error
        self.printFeatureResult(key, retval, debug)
        self.features[key] = retval
        
        
    def setEdgeFeatures(self, debug=False):
        key = "Edge"
        self.printFeatureResult(key, None, debug)
            
        retval = {}
        
        for edgeNum in range(5):
            features = self.getEdgeAttrs(edgeNum, debug)
            retval["{0}".format(edgeNum)] = features

        self.printFeatureResult(key, retval, debug)
        self.features[key] = retval    
    
        
        
        
        
        
    
    
    ####################################################################################################################
    #
    # Gloabl Network Features
    #
    ####################################################################################################################
    def setArticulationStructure(self, debug=False):
        key = "VertexArticulationPoint"
        self.printFeatureResult(key, None, debug)
            
        try:
            ap = self.g.articulation_points()
        except:
            if debug:
                print("Could not get articulation_points")
            ap = []

        retval = {}
        retval["Count"] = len(ap)
        try:
            retval["Fraction"] = float(len(ap))/self.numVertices
        except:
            retval["Fraction"] = 0.0
        
        for vertexNum in range(self.numVertices):
            vertexID   = self.getVertexID(vertexNum)
            value      = int(vertexID in ap)
            self.setVertexExternalData(vertexNum, "VertexArticulationPoint", value)
            
        self.printFeatureResult(key, retval, debug)
        self.features[key] = retval


    def setCommunityStructure(self, debug=False):
        key = "VertexCommunity"
        self.printFeatureResult(key, None, debug)
            
        from igraph import arpack_options
        arpack_options.maxiter=30000

        from collections import Counter
        communityCntr = Counter()
        
        retval = {}
        vertexCommunities = Counter()
        try:
            communityItr = self.g.community_leading_eigenvector()
            nComm = 0
            nV = 0.0
            for comm in communityItr:
                nComm += 1
                nV += float(len(comm))
                for vertexID in comm:
                    vertexCommunities[vertexID] += 1
        except:
            nComm = None
            
        retval['Count'] = nComm
        for vertexNum in range(self.numVertices):
            vertexID   = self.getVertexID(vertexNum)
            value      = vertexCommunities[vertexID]
            self.setVertexExternalData(vertexNum, "VertexCommunity", value)                
            

        self.printFeatureResult(key, retval, debug)
        self.features[key] = retval


    def setCliqueStructure(self, debug=False):
        key = "GlobalClique"
        self.printFeatureResult(key, None, debug)
        
        retval = {}
        from collections import Counter
        cliqueCntr = Counter()
        nCliques = 0
        for clique in self.g.cliques():
            nCliques += 1
            for i in range(5):
                vertexID = self.getVertexID(i)
                if vertexID in clique:
                    cliqueCntr[i] += 1

        retval['Count'] = nCliques
        for i in range(5):
            retval["Vtx{0}".format(i)] = cliqueCntr[i]

        self.printFeatureResult(key, retval, debug)
        self.features[key] = retval


    def setDyadCensus(self, debug=False):
        key = "GlobalDyad"
        self.printFeatureResult(key, None, debug)
            
        retval = {}
        try:
            dy = self.g.dyad_census().as_dict()
            dyadAsym   = dy['asymmetric']
            dyadMutual = dy['mutual']
            dyadNull   = dy['null']
        except:
            print("Could not get Dyad Census from graph!")
            dyadAsym   = None
            dyadMutual = None
            dyadNull   = None
        retval["Asymmetric"] = dyadAsym
        retval["Mutual"]     = dyadMutual
        retval["Null"]       = dyadNull
        
        self.printFeatureResult(key, retval, debug)
        self.features[key] = retval
                             

    def setGlobalNetworkFeatures(self, debug = False):
        key = "Global"
        self.printFeatureResult(key, None, debug)
            
        retval = {}
    
        ## Global (Network)
        try:
            netDiameter = self.g.diameter()
        except:
            netDiameter = None
        if debug: print("Network Diameter:         {0:.2f}".format(netDiameter))
        retval["Diameter"] = netDiameter

        try:
            netDensity = self.g.density()
        except:
            netDensity = None
        if debug: print("Network Density:          {0:.2f}".format(netDensity))
        retval["Density"] = netDensity

        if False:
            try:
                netCohesion = self.g.cohesion()
            except:
                netCohesion = None
            if debug: print("Network Cohesion:         {0:.2f}".format(netCohesion))
            retval["Cohesion"] = netCohesion

        try:
            netGirth = self.g.girth()
        except:
            netGirth = None
        if debug: print("Network Girth:            {0:.2f}".format(netGirth))
        retval["Girth"] = netGirth

        try:
            tripConnectivity = self.g.edge_connectivity()
        except:
            tripConnectivity = None
        if debug: print("Trip Connectivity:        {0:.2f}".format(tripConnectivity))
        retval["Connectivity"] = tripConnectivity

        try:
            netTransitivity = self.g.transitivity_undirected()
        except:
            netTransitivity = None
        if debug: print("Network Transitivity:     {0:.2f}".format(netTransitivity))
        retval["Transitivity"] = netTransitivity

        try:
            netAvgPathLength = self.g.average_path_length()
        except:
            netAvgPathLength = None
        if debug: print("Network Avg Path Length:  {0:.2f}".format(netAvgPathLength))
        retval["AvgPathLength"] = netAvgPathLength

        try:
            netAssortativity = self.g.assortativity_degree()
        except:
            netAssortativity = None
        if debug: print("Network Assortativity:    {0:.2f}".format(netAssortativity))
        retval["Assortativity"] = netAssortativity

        self.printFeatureResult(key, retval, debug)
        self.features[key] = retval
        
        
        

            
            
        
    #######################################################################################################################
    #
    # Create Folium (Map) Data
    #
    #######################################################################################################################
    def setMapFeatures(self, maxVertices=10, maxEdges=10, debug=False):
        self.mapFeatures = self.getMapData(maxVertices, maxEdges, debug)
        
    def getMapFeatures(self):
        if self.mapFeatures is None:
            self.setMapFeatures()
        return self.mapFeatures
        
    def getMapData(self, maxVertices=100, maxEdges=100, debug=False):
        mapdata = {"Edges": {}, "Vertices": {}}
        for edgeNum in range(self.numEdges):
            if edgeNum > maxEdges:
                break

            edgeID = self.getEdgeID(edgeNum)
            edge   = self.getEdge(edgeID)
            weight = edge.getAttrDataByKey("Weight")
            com    = edge.getAttrDataByKey("CoM")
            dist   = edge.getAttrDataByKey("DrivingDistance")
            dow    = edge.getAttrDataByKey("DayOfWeek")
            mapdata["Edges"][edgeNum] = {"Weight": weight, "CoM": com, "Dist": dist, "DOW": dow}
            
                
        for vertexNum in range(self.numVertices):
            vertexID = self.getVertexID(vertexNum)
            vertex   = self.getVertex(vertexID)
            if vertexNum > maxVertices:
                if vertexID != self.homeVertexID:
                    continue
                                        
            degree   = vertex.getAttrDataByKey('Degree')
            trips    = vertex.getAttrDataByKey('Trips')
            poi      = vertex.getAttrDataByKey("POIUniqueVisits")
            dwell    = vertex.getAttrDataByKey("DwellTime")
            
            com      = vertex.getFeatureDataByKey("CoM")['Name']
            radius   = vertex.getFeatureDataByKey("Radius")['Name']
            quantile = vertex.getFeatureDataByKey("Quantiles")['Name']
            cells    = vertex.getFeatureDataByKey("Cells")['Name']
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

            locdata = {"CoM": com, "POI": poi, "Degree": degree, "Dwell": dwell, "Radius": radius, "Quantiles": quantile, "Trips": trips, "Attrs": attrsStr}
            if vertexNum < maxVertices:
                if vertexID != self.homeVertexID:
                    mapdata["Vertices"][vertexNum] = locdata
            if vertexID == self.homeVertexID:
                mapdata["Vertices"]["Home"] = locdata
                
        return mapdata

    

    #######################################################################################################################
    #
    # Create DataFrame
    #
    #######################################################################################################################
    def fixType(self, value):
        import numpy as np
        if isinstance(value, tuple):
            value = str(value)
        elif isinstance(value, np.int64):
            value = int(value)
        elif isinstance(value, np.float64):
            value = float(value)
        elif isinstance(value, str):
            value = str(value)
        elif isinstance(value, float):
            value = float(value)
        elif isinstance(value, int):
            value = int(value)
        elif isinstance(value, type(None)):
            value = None
        else:
            raise ValueError("Unknown Type: {0} --> {1}".format(type(value), value))
        return value
        #cntr[type(subfeaturedata)] += 1
                        
    def getFeatureDataFrame(self, debug=False):
        from pandas import DataFrame
        from collections import Counter
        features = {}
        cntr = Counter()
        for category, categorydata in self.features.items():
            for feature, featuredata in categorydata.items():
                if isinstance(featuredata, dict):
                    for subfeature, subfeaturedata in featuredata.items():
                        key = "".join([category,feature,subfeature])
                        value = self.fixType(subfeaturedata)
                        features[key] = value
                else:
                    key = "".join([category,feature])
                    value = self.fixType(featuredata)
                    features[key] = value

        self.printFeatures()
        #print(cntr.most_common())
        
        if debug:
            print("Created Data Frame with {0} features".format(len(features)))
            
        features['Device'] = self.device
        if self.expectedFeatures is not None:
            if len(features) != self.expectedFeatures:
                print("\nThere are only {0}/{1} features for {2}!!!\n".format(len(features), self.expectedFeatures, self.device))
                self.printFeatures()
                raise ValueError("\nThere are only {0}/{1} features for {2}!!!\n".format(len(features), self.expectedFeatures, self.device))

        if debug:
            self.printFeatures()
        df = DataFrame(features, index=[0])
        return df