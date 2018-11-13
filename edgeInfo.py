import datetime
from collections import Counter
from pandasUtils import getRowData


class edgeInfo():
    def __init__(self, g, debug=False):
        self.g = g
        self.debug          = debug
        self.edgeDict       = None
        self.orderedEdges   = None
        self.edgeAttrGroups = None
        self.edgeAttrsDF    = None
        self.edgeFeatures   = {}
        self.edgeFeaturesDF = None
    

        
    def setEdgeDict(self):
        self.edgeDict = {(u, v): d for (u,v,d) in self.g.edges(data=True)}
        
    def getEdgeDict(self):
        return self.edgeDict
    
    def getAttrGroups(self):
        return self.edgeAttrGroups
    
    def orderEdges(self, metric='Weight'):
        self.setEdgeDict()
        tmp = {(u,v): d['attr_dict'][metric] for (u,v,d) in self.g.edges(data=True)}
        self.orderedEdges = sorted(tmp, key=tmp.get, reverse=True)
        
    def getEdgeWeights(self):
        metric  = "Weight"
        weights = {(u,v): d[metric] for (u,v,d) in self.g.edges(data=True)}
        return weights
        
        
    def getEdges(self, ordered=True):
        if self.orderedEdges is not None:
            return self.orderedEdges
        else:
            self.orderEdges()
            return self.orderedEdges
        
    def getEdgeNumByName(self, edgeName, debug=True):
        edgeList = self.getEdges()
        try:
            edgeNum = edgeList.index(edgeName)
        except:
            if debug:
                print("Could not get edge number for name {0}".format(edgeName))
            edgeNum = None
        return edgeNum
        
    def getEdgeNameByNum(self, edgeNum, debug=True):
        edgeList = self.getEdges()
        if edgeNum >= len(edgeList):
            if debug:
                print("Edge num {0} is greater than edge list length {1}".format(edgeNum, len(edgeList)))
            return None
        try:
            edgeName = edgeList[edgeNum]
        except:
            if debug:
                print("Could not get edge name for num {0}".format(edgeNum))
            edgeName = None
        return edgeName        
        
        
        
        
        
    def getEdgeData(self, edgeNum, datatype="raw", debug=True):
        edgeName = self.getEdgeNameByNum(edgeNum)
        return self.getEdgeDataByName(edgeName, datatype, debug=debug)
            
        
        
    def getEdgeDataByName(self, edgeName, datatype="raw", debug=True):
        edgeData = None
        if datatype == "raw":
            try:
                edgeData = self.edgeDict[edgeName]
            except:
                if debug:
                    print("Could not get edge data for edge name {0}".format(edgeName))
        elif datatype == "attr":
            try:
                edgeData = getRowData(self.edgeAttrsDF, rownames=str(edgeName))
                #edgeData = self.edgeAttrs[edgeName]
            except:
                if debug:
                    print("Could not get edge attr data for edge name {0}".format(edgeName))
        elif datatype == "feat":
            edgeData = self.edgeFeatures[edgeName]
        else:
            raise ValueError("Datatype {0} is not known".format(datatype))
        return edgeData
    
    
    
    ########################################################################################################################
    # Attributes
    ########################################################################################################################
    def flattenEdgeAttrs(self):
        self.edgeAttrGroups = {}
        for edgeName, edgeData in self.edgeDict.items():
            for attrName in list(edgeData.keys()):
                attrData = edgeData[attrName]
                if isinstance(attrData, dict):
                    if attrData.get('Avg') is None:
                        for subName, subData in attrData.items():
                            self.edgeAttrGroups[subName] = attrName
                            self.edgeDict[edgeName][subName] = subData
                        del self.edgeDict[edgeName][attrName]
                    else:
                        self.edgeAttrGroups[attrName] = "General"
                else:
                    self.edgeAttrGroups[attrName] = "Diagnostic"
                    
    
    def collectEdgeAttrs(self):
        self.edgeAttrNames = None
        self.edgeAttrs = {}
        for edgeName, edgeData in self.edgeDict.items():
            if not isinstance(edgeData, dict):
                raise ValueError("Cannot collect edge attrs because the data is not a dictionary")
            try:
                attrs = edgeData['attr_dict']
            except:
                attrs = edgeData
            if self.edgeAttrNames is None:
                self.edgeAttrNames = list(attrs.keys())
            for attrName in self.edgeAttrNames:
                attrData = attrs[attrName]
                if self.edgeAttrs.get(attrName) is None:
                    self.edgeAttrs[attrName] = []
                if attrData is None:
                    continue
                if isinstance(attrData, (int, float, str)):
                    self.edgeAttrs[attrName].append(attrData)
                elif isinstance(attrData, (datetime.date,list,tuple)):
                    self.edgeAttrs[attrName].append(attrData)
                elif isinstance(attrData, dict):
                    if isinstance(attrData, Counter):
                        self.edgeAttrs[attrName].append(attrData.most_common())
                    else:
                        if attrData.get('Avg') is not None:
                            self.edgeAttrs[attrName].append(attrData['Avg'])
                        else:
                            raise ValueError("Cannot collect edge attrs dictionary has no 'Avg' key: {0}, {1}".format(attrData, type(attrData)))
                else:
                    raise ValueError("Attr data for {0} is type {1} and not allowed.".format(attrName, type(attrData)))
 
        for attrName in list(self.edgeAttrs.keys()):
            if len(self.edgeAttrs[attrName]) == 0:
                del self.edgeAttrs[attrName]
                
        from pandas import DataFrame
        self.edgeAttrsDF = DataFrame(self.edgeAttrs)
        self.edgeAttrsDF.index = [str(x) for x in list(self.edgeDict.keys())]
            
        
        
    ########################################################################################################################
    # Features
    ########################################################################################################################
    def setEdgeFeature(self, edgeName, key, value):
        if self.edgeFeatures.get(edgeName) is None:
            self.edgeFeatures[edgeName] = {}
        self.edgeFeatures[edgeName][key] = value
        
    def getEdgeFeature(self, edgeName, key):
        return self.edgeFeatures[edgeName][key]
    
    def getEdgeFeatures(self, edgeName):
        return self.edgeFeatures[edgeName]