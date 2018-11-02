## edge Class

class edge():
    def __init__(self, edgeID, edgeIdx, edgeNum, vertices, debug=False):
        self.edgeID   = edgeID
        self.edgeIdx  = edgeIdx
        self.edgeNum  = edgeNum
        self.vertices = vertices

        self.externalData = None
        self.internalData = None
        
        self.features  = {}
        self.attrs     = {}
        self.attrsList = []

        
    ###########################################################################################
    #
    # Getters/Setters
    #
    ###########################################################################################   
    def getID(self):
        return self.edgeID
    def getIdx(self):
        return self.edgeIdx
    def getNum(self):
        return self.edgeNum
    def getVertices(self):
        return self.vertices
    
    def setExternalData(self, externalData):
        if self.externalData is None:
            self.externalData = externalData
        
    def setInternalData(self, externalData):
        if self.internalData is None:
            self.internalData = internalData
            
    def setExternalDataByKey(self, key, value):
        if self.externalData is None:
            self.externalData = {}
        self.externalData[key] = value
            
    def getExternalDataByKey(self, key, debug=False):
        if self.externalData is None:
            if debug:
                print("External Data is not set so returning None for {0}!".format(key))
                return None
        return self.externalData.get(key)
            
    def setInternalDataByKey(self, key, value):
        if self.internalData is None:
            self.internalData = {}
        self.internalData[key] = value
        
    def getInternalDataByKey(self, key):
        if self.internalData is None:
            print("Internal Data is not set so returning None for {0}!".format(key))
        return self.internalData.get(key)
        
        
    ###########################################################################################
    #
    # Print
    #
    ###########################################################################################        
    def showExternalData(self):
        for key,value in self.externalData.items():
            print(self.edgeID,'\t',self.edgeNum,'\t',key,'\t',value)
            
    def showInternalData(self):
        for key,value in self.internalData.items():
            print(self.edgeID,'\t',self.edgeNum,'\t',key,'\t',value)
            
    def showFeatures(self):
        if not isinstance(self.features, dict):
            print("There is no feature data for edge ID/Num {0}/{1}".format(self.getID(),self.getNum()))
            return
        for key,value in self.features.items():
            print(self.vertexID,'\t',self.vertexNum,'\t',key,'\t',value)
            
    def showAttrs(self):
        if not isinstance(self.attrs, dict):
            print("There is no attrs data for edge ID/Num {0}/{1}".format(self.getID(),self.getNum()))
            return
        for key,value in self.attrs.items():
            print(self.edgeID,'\t',self.edgeNum,'\t',key,'\t',value)
            
    
        
    ###########################################################################################
    #
    # Features
    #
    ###########################################################################################        
    def setFeatures(self, features):
        if self.features is None:
            self.features = features
        
    def getFeatures(self):
        return self.features
    
    def setFeatureDataByKey(self, key, value):
        if self.features is None:
            self.features = {}
        self.features[key] = value
                        
    def isSetFeature(self, key, debug=False):
        if self.features is None:
            if debug:
                print("feature Data is not set so returning None for {0}!".format(key))
                return None
        return key in self.features
            
    def getFeatureDataByKey(self, key, debug=False):
        if self.features is None:
            if debug:
                print("feature Data is not set so returning None for {0}!".format(key))
                return None
        return self.features.get(key)
    
        
    ###########################################################################################
    #
    # Attrs
    #
    ###########################################################################################        
    def setAttrs(self, attrs):
        if self.attrs is None:
            self.attrs = attrs
        
    def getAttrs(self):
        return self.attrs
        
    def setAttrsList(self, attrsList):
        self.attrsList = attrsList
        
    def getAttrsList(self):
        return self.attrsList
    
    def setAttrDataByKey(self, key, value):
        if self.attrs is None:
            self.attrs = {}
        self.attrs[key] = value
            
    def getAttrDataByKey(self, key, debug=False):
        if self.attrs is None:
            if debug:
                print("attr Data is not set so returning None for {0}!".format(key))
                return None
        return self.attrs.get(key)