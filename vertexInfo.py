import datetime
from numpy import int64, float64
from collections import Counter
from pandas import DataFrame
from pandasUtils import getRowData, getColData, isDataFrame


class vertexInfo():
    def __init__(self, g, debug=False):
        self.g = g
        self.debug            = debug
        self.vertexDict       = None
        self.orderedVertices  = None
        self.vertexAttrGroups = None
        self.vertexAttrsDF    = None
        self.vertexFeatures   = {}
        self.vertexFeaturesDF = None

        self.diagnosticAttrs = ['CoM', 'Radius', 'Cells', 'Quantiles', 'Geohashs', 'First', 'Last', 'Geo']
                              
    def setNodeDict(self):
        self.nodeDict = {u: d for (u,d) in self.g.nodes(data=True)}
        
    def getNodeDict(self):
        return self.nodeDict
    
    def getAttrGroups(self):
        return self.vertexAttrGroups
        
    def orderVertices(self, metric='Centrality', debug=False):
        if debug:
            print("Ordering Vertices by {0}".format(metric))
        self.setNodeDict()
        if metric == 'Centrality':
            from networkx.algorithms import degree_centrality
            tmp = degree_centrality(self.g)
        elif metric == 'Counts':
            tmp = {u: d['N'] for (u,d) in self.g.nodes(data=True)}
        else:
            raise ValueError("Metric {0} is not used for vertex ordering".format(metric))           
        self.orderedVertices = sorted(tmp, key=tmp.get, reverse=True)
                

            
    def getVertices(self, ordered=True):
        if self.orderedVertices is not None:
            return self.orderedVertices
        else:
            self.orderVertices()
            return self.orderedVertices
        
    def getVertexNumByName(self, vertexName, debug=True):
        vertexList = self.getVertices()
        try:
            vertexNum = vertexList.index(vertexName)
        except:
            if debug:
                print("Could not get vertex number for name {0}".format(vertexName))
            vertexNum = None
        return vertexNum
        
    def getVertexNameByNum(self, vertexNum, debug=True):
        if not isinstance(vertexNum, int):
            raise ValueError("Vertex number {0} must be an integer".format(vertexNum))
        vertexList = self.getVertices()
        if vertexNum >= len(vertexList):
            if debug:
                print("vertex num {0} is greater than vertex list length {1}".format(vertexNum, len(vertexList)))
            return None
        try:
            vertexName = vertexList[vertexNum]
        except:
            if debug:
                print("Could not get vertex name for num {0}".format(vertexNum))
            vertexName = None
        return vertexName
    
        
    def getVertexData(self, vertexNum, datatype="raw", debug=True):
        vertexName = self.getVertexNameByNum(vertexNum)
        return self.getVertexDataByName(vertexName, datatype, debug=debug)
            
        
    def getVertexDataByName(self, vertexName, datatype="raw", debug=True):
        vertexData = None
        if datatype == "raw":
            try:
                vertexData = self.nodeDict[vertexName]
            except:
                if debug:
                    print("Could not get vertex data for vertex name {0}".format(vertexName))
        elif datatype == "attr":
            if self.vertexAttrsDF is None:
                raise ValueError("Cannot access vertex attrs DF because it's None!")
            try:
                vertexData = getRowData(self.vertexAttrsDF, rownames=str(vertexName))
                #vertexData = self.vertexAttrs[vertexName]
            except:
                if debug:
                    print("Could not get vertex attr data for vertex name {0}. Avail: {1}".format(vertexName, self.vertexAttrsDF.index))
        elif datatype == "feat":
            vertexData = self.vertexFeatures[vertexName]
        else:
            raise ValueError("Datatype {0} is not known".format(datatype))
        return vertexData
        
        
            
        
    ########################################################################################################################
    # Attributes
    ########################################################################################################################
    def flattenVertexAttrs(self, debug=False):
        if debug:
            print("Flattening Vertex Attributes")
        self.vertexAttrGroups = {}        
        for vertexName in list(self.nodeDict.keys()):
            vertexData = self.nodeDict[vertexName]
            for attrName in list(vertexData.keys()):
                attrData = vertexData[attrName]
                if isinstance(attrData, dict):
                    if attrData.get('Avg') is None:
                        for subName, subData in attrData.items():
                            self.vertexAttrGroups[subName] = attrName
                            vertexData[subName] = subData
                        del vertexData[attrName]
                    else:
                        self.vertexAttrGroups[attrName] = "General"
                else:
                    if attrName in self.diagnosticAttrs:
                        self.vertexAttrGroups[attrName] = "Diagnostic"
                    else:
                        self.vertexAttrGroups[attrName] = "General"
            self.nodeDict[vertexName] = vertexData
            
        
    def collectVertexAttrs(self, debug=False, verydebug=False):
        if debug:
            print("Collecting Vertex Attributes")
        self.vertexAttrNames = None
        self.vertexAttrs = {}
        for vertexName, vertexData in self.nodeDict.items():
            if debug and verydebug:
                print("  Vertex[{0}] with {1} attributes".format(vertexName, len(vertexData)))
            if not isinstance(vertexData, dict):
                raise ValueError("Cannot collect vertex attrs because the data is not a dictionary")
            attrs = vertexData
            if self.vertexAttrNames is None:
                self.vertexAttrNames = list(attrs.keys())
            for attrName in self.vertexAttrNames:
                attrData = attrs[attrName]
                if self.vertexAttrs.get(attrName) is None:
                    self.vertexAttrs[attrName] = []
                if attrData is None:
                    self.vertexAttrs[attrName].append(attrData)
                elif isinstance(attrData, (int, float, str, int64, float64)):
                    self.vertexAttrs[attrName].append(attrData)
                elif isinstance(attrData, (datetime.date,list,tuple)):
                    self.vertexAttrs[attrName].append(attrData)
                elif isinstance(attrData, dict):
                    if isinstance(attrData, Counter):
                        self.vertexAttrs[attrName].append(attrData.most_common())
                    else:
                        if attrData.get('Avg') is not None:
                            self.vertexAttrs[attrName].append(attrData['Avg'])
                        else:
                            raise ValueError("Cannot collect vertex attrs dictionary for {0} because it has no 'Avg' key: {1}, {2}".format(attrName, attrData, type(attrData)))
                else:
                    raise ValueError("Attr data {0} for {1} is type {2} and not allowed.".format(attrData, attrName, type(attrData)))
 
        for attrName in list(self.vertexAttrs.keys()):
            if len(self.vertexAttrs[attrName]) == 0:
                del self.vertexAttrs[attrName]
            
        
    ########################################################################################################################
    # Clean and Aggregate Attributes
    ########################################################################################################################
    def createVertexAttrsDataFrame(self, debug=False):
        if debug:
            print("Cleaning Vertex Attribute Names")
        self.vertexAttrsDF = DataFrame(self.vertexAttrs)
        self.vertexAttrsDF.index = list(self.nodeDict.keys())
        
    def getVertexAttrsDataFrame(self, debug=False):
        return self.vertexAttrsDF
            
        
    ########################################################################################################################
    # Features
    ########################################################################################################################
    def setVertexFeature(self, vertexName, category, key, value):
        ### Fix name (if needed)
        if True:
            if key.startswith("OSM"):
                key = key[3:]
            if key.endswith("Name"):
                key = key[:-4]
            if key.startswith("CENSUS"):
                key = key[6:]
            if key.startswith("CENSUS"):
                key = key[6:]
            if key.startswith("ROADS"):
                key = key[5:]
            if key.startswith("RAIL"):
                key = key[4:]
            if key.startswith("POIHERE"):
                key = key[7:]
            if key.startswith("TERMINALS"):
                key = key[9:]
            
        if self.vertexFeatures.get(vertexName) is None:
            self.vertexFeatures[vertexName] = {}
        if self.vertexFeatures[vertexName].get(category) is None:
            self.vertexFeatures[vertexName][category] = {}
        if self.vertexFeatures[vertexName][category].get(key) is not None:
            curval = self.vertexFeatures[vertexName][category][key]
            if isinstance(curval, int):
                newval = max(curval,value)
                self.vertexFeatures[vertexName][category][key] = newval
            else:
                raise ValueError("Overwriting {0}/{1} and it's not an integer".format(category, key))
        else:
            self.vertexFeatures[vertexName][category][key] = value
        
    def getVertexFeature(self, vertexName, category, key):
        try:
            retval = self.vertexFeatures[vertexName][category][key]
        except:
            raise ValueError("Could not get feature for Vertex {0}, Category {1} and Key {2}".format(vertexName, category, key))
        return retval
    
    def getVertexFeatures(self, vertexName):
        return self.vertexFeatures[vertexName]
    
    def getVertexCategoryFeatures(self, vertexName, category):
        return self.vertexFeatures[vertexName][category]
            
        
    ########################################################################################################################
    # DataFrame of Important Features
    ########################################################################################################################
    def getVertexHomeFeaturesDataFrame(self):
        homeFeatures = ["DwellTime", "DailyVisits", "OvernightStays", "Interval"]
        if isDataFrame(self.vertexAttrsDF):
            colnames = ["N", "IsHome"]
            for poscolname in homeFeatures:
                colnames += [x for x in self.vertexAttrsDF.columns if x.find(poscolname) != -1]
            homeFeaturesDF = getColData(self.vertexAttrsDF, colnames=colnames)
            return homeFeaturesDF
        else:
            print("Vertex Attributes DataFrame is not ready yet!")
            return None