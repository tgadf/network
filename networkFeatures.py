from pandas import DataFrame
from driverNetwork import driverNetwork
from networkAlgos import networkAlgos
from networkCategories import categories
from collections import OrderedDict
from pandasUtils import getRowData, getColData, dropColumns, fixType, isDataFrame
from numpyUtils import isNumericDtype

class networkFeatures():
    def __init__(self, dn, debug=False):
        self.dn = dn
        self.features = {}
        
        self.categories        = categories(debug)
        self.getCategories     = self.categories.getCategories
        self.getCategory       = self.categories.getCategory
        self.getPermCategories = self.categories.getPermCategories
        self.getPermCategory   = self.categories.getPermCategory  
        self.getHomeRatioCategory = self.categories.getHomeRatioCategory
        self.getIntervalCategory = self.categories.getIntervalCategory
        
        

    #################################################################################################################
    #################################################################################################################
    # Vertex Counts
    #################################################################################################################
    #################################################################################################################
    def fillVertexCensusCounts(self, debug=False):
        if debug:
            print("Filling Vertex Census Counts")
            
            
        from collections import Counter
        vertexCounts = None

        for vertexNum,vertexName in enumerate(self.dn.getVertices()):
            vertexData = self.dn.getVertexByName(vertexName, 'feat').get("Census")
            if vertexData is None:
                raise ValueError("Could not get {0} category from vertex data!".format(category))
                
            if vertexCounts is None:
                featureNames = list(vertexData.keys())
                vertexCounts = {}
                for featureName in featureNames:
                    vertexCounts[featureName] = Counter()
            
            for featureName,value in vertexData.items():
                vertexCounts[featureName][value] += 1
                  
                            
        retval = {}
        nV = len(self.dn.getVertices())
        for featureName,counts in vertexCounts.items():
            key = featureName.replace("Census", "")
            key = key.replace("CENSUS", "")
            if key.endswith("Name"):
                key = key[:-4]
            
            retval[key] = {}
            retval[key]["N"] = len(counts)
            try:
                mc = counts.most_common(1)[0]
                retval[key]["MostCommon"]         = mc[0]
                retval[key]["MostCommonFraction"] = mc[1]/nV
            except:
                retval[key]["MostCommon"]         = None
                retval[key]["MostCommonFraction"] = None
    

        if debug:
            print("  Filling Vertex Census Counts")
             
        self.features["Vertex_Census_Counts"] = retval        

        
    def fillVertexCategoryCounts(self, category, debug=False):
        if debug:
            print("Filling Vertex {0} Counts".format(category))
            
        featureNames = None
            
        from collections import Counter
        vertexCounts = {"N": {}, 3: {}, 10: {}, 25: {}}

        for vertexNum,vertexName in enumerate(self.dn.getVertices()):
            vertexData = self.dn.getVertexByName(vertexName, 'feat').get(category)
            if vertexData is None:
                raise ValueError("Could not get {0} category from vertex data!".format(category))
            
            if featureNames is None:
                featureNames = list(vertexData.keys())
                for featureName in featureNames:
                    featCats = self.getCategories(featureName)
                    if featCats is not None:
                        if featCats == ['Y', 'N']:
                            key = featureName
                            for cutoff in ["N",3,10,25]:
                                vertexCounts[cutoff][key]  = 0
                        else:
                            for cat in featCats:
                                key = "".join([featureName,cat])
                                for cutoff in ["N",3,10,25]:
                                    vertexCounts[cutoff][key]  = 0
                        
            
            for featureName in featureNames:                
                value = vertexData[featureName]
                featCats = self.getCategories(featureName)
                if featCats is not None:
                    if featCats == ['Y', 'N']:
                        key = featureName
                        vertexCounts["N"][key] += int(value == 'Y')
                        for cutoff in [3,10,25]:
                            if vertexNum < cutoff:
                                vertexCounts[cutoff][key] += int(value == 'Y')
                    elif value in featCats:
                        key = "".join([featureName,value])
                        vertexCounts["N"][key] += 1
                        for cutoff in [3,10,25]:
                            if vertexNum < cutoff:
                                vertexCounts[cutoff][key] += 1
                    else:
                        raise ValueError("Value [{0}] not in [{1}] for feature [{2}]".format(value, featCats, featureName))
                            
                            
        retval = {}
        for cutoff,cutoffData in vertexCounts.items():
            for key,value in cutoffData.items():
                if retval.get(key) is None:
                    retval[key] = {}
                if isinstance(cutoff, int):
                    retval[key]["".join(["Top", str(cutoff)])] = value
                else:
                    retval[key][cutoff] = value
                    
        if debug:
            print("  Filling Vertex {0} Counts for {1} Cutoff Values".format(category, len(retval)))
                                
        self.features["Vertex_{0}_Counts".format(category)] = retval
        
        
    def fillVertexInternalCounts(self, debug=False):
        self.fillVertexCategoryCounts(category="Internal", debug=debug)
        
    def fillVertexGeoSpatialCounts(self, debug=False):
        self.fillVertexCategoryCounts(category="GeoSpatial", debug=debug)
        
            

        
        

    #################################################################################################################
    #################################################################################################################
    # Edge Counts
    #################################################################################################################
    #################################################################################################################
    def fillEdgeCensusCounts(self, debug=False):
        if debug:
            print("Filling Edge Census Counts")
            
            
        from collections import Counter
        edgeCounts = None

        for edgeNum,edgeName in enumerate(self.dn.getEdges()):
            edgeData = self.dn.getEdgeByName(edgeName, 'feat').get("Census")
            if edgeData is None:
                raise ValueError("Could not get {0} category from edge data!".format(category))
                
            if edgeCounts is None:
                featureNames = list(edgeData.keys())
                edgeCounts = {}
                for featureName in featureNames:
                    edgeCounts[featureName] = Counter()
            
            for featureName,value in edgeData.items():
                featureValue = " <-> ".join(sorted([str(x) for x in value]))
                edgeCounts[featureName][featureValue] += 1
                  
                            
        retval = {}
        nE = len(self.dn.getEdges())
        for key,counts in edgeCounts.items():            
            retval[key] = {}
            retval[key]["N"] = len(counts)
            try:
                mc = counts.most_common(1)[0]
                retval[key]["MostCommon"]         = mc[0]
                retval[key]["MostCommonFraction"] = mc[1]/nE
            except:
                retval[key]["MostCommon"]         = None
                retval[key]["MostCommonFraction"] = None
    

        if debug:
            print("  Filling Edge Census Counts")
             
        self.features["Edge_Census_Counts"] = retval               

     

        
    def fillEdgeGeoSpatialCounts(self, debug=False):
        category = "GeoSpatial"
        if debug:
            print("Filling edge {0} Counts".format(category))
            
        featureNames = None
            
        from collections import Counter
        edgeCounts = {"N": {}, 3: {}, 10: {}, 25: {}}

        for edgeNum,edgeName in enumerate(self.dn.getEdges()):
            edgeData = self.dn.getEdgeByName(edgeName, 'feat').get(category)
            if edgeData is None:
                raise ValueError("Could not get {0} category from edge data!".format(category))
            
            if featureNames is None:
                featureNames = list(edgeData.keys())
                for featureName in featureNames:
                    key = featureName
                    for cutoff in ["N",3,10,25]:
                        edgeCounts[cutoff][key]  = 0
                        
            
            for featureName in featureNames:
                key = featureName
                value = edgeData[featureName]
                if all([isinstance(x, int) for x in value]):
                    if any([x > 0 for x in value]):
                        value = 1
                    else:
                        value = 0
                    edgeCounts["N"][key] += value
                    for cutoff in [3,10,25]:
                        if edgeNum < cutoff:
                            edgeCounts[cutoff][key] += value
                            
        retval = {}
        for cutoff,cutoffData in edgeCounts.items():
            for key,value in cutoffData.items():
                if retval.get(key) is None:
                    retval[key] = {}
                if isinstance(cutoff, int):
                    retval[key]["".join(["Top", str(cutoff)])] = value
                else:
                    retval[key][cutoff] = value
                    
        if debug:
            print("  Filling edge {0} Counts for {1} Cutoff Values".format(category, len(retval)))
                                
        self.features["Edge_{0}_Counts".format(category)] = retval
        

        

    def fillEdgeInternalCounts(self, debug=False):
        category="Internal"
        if debug:
            print("Filling Edge {0} Counts".format(category))
            
        featureNames = None
            
        from collections import Counter
        edgeCounts = {"N": {}, 3: {}, 10: {}, 25: {}}

        for edgeNum,edgeName in enumerate(self.dn.getEdges()):
            edgeData = self.dn.getEdgeByName(edgeName, 'feat').get(category)
            if edgeData is None:
                raise ValueError("Could not get {0} category from edge data!".format(category))
            
            if featureNames is None:
                featureNames = list(edgeData.keys())
                for featureName in featureNames:
                    featCats = self.getCategories(featureName)
                    if featCats is not None:
                        if featCats == ['Y', 'N']:
                            key = featureName
                            for cutoff in ["N",3,10,25]:
                                edgeCounts[cutoff][key]  = 0
                        else:
                            for cat in featCats:
                                key = "".join([featureName,cat])
                                for cutoff in ["N",3,10,25]:
                                    edgeCounts[cutoff][key]  = 0
                        
            
            for featureName in featureNames:                
                value = edgeData[featureName]
                featCats = self.getCategories(featureName)
                if featCats is not None:
                    if featCats == ['Y', 'N']:
                        key = featureName
                        edgeCounts["N"][key] += int(value == 'Y')
                        for cutoff in [3,10,25]:
                            if edgeNum < cutoff:
                                edgeCounts[cutoff][key] += int(value == 'Y')
                    elif value in featCats:
                        key = "".join([featureName,value])
                        edgeCounts["N"][key] += 1
                        for cutoff in [3,10,25]:
                            if edgeNum < cutoff:
                                edgeCounts[cutoff][key] += 1
                    else:
                        raise ValueError("Value [{0}] not in [{1}] for feature [{2}]".format(value, featCats, featureName))
                            
                            
        retval = {}
        for cutoff,cutoffData in edgeCounts.items():
            for key,value in cutoffData.items():
                if retval.get(key) is None:
                    retval[key] = {}
                if isinstance(cutoff, int):
                    retval[key]["".join(["Top", str(cutoff)])] = value
                else:
                    retval[key][cutoff] = value
                    
        if debug:
            print("  Filling edge {0} Counts for {1} Cutoff Values".format(category, len(retval)))
                                
        self.features["Edge_{0}_Counts".format(category)] = retval
        
        
        
        
        
    #################################################################################################################
    # Vertex/Edge Properties
    #################################################################################################################
    def fillObjectProperties(self, objectData, debug=False):
        try:
            diffVtx0Vtx1  = float(objectData[0] - objectData[1])
        except:
            diffVtx0Vtx1  = None

        try:
            diffVtx1Vtx2  = float(objectData[1] - objectData[2])
        except:
            diffVtx1Vtx2  = None

        try:
            diffVtx0Vtx12 = float(objectData[0] - objectData[1] - objectData[2])
        except:
            diffVtx0Vtx12 = None

        try:
            qvals = list(objectData.quantile(q=[0.05,0.25,0.5,0.75,0.95]))
        except:
            qvals = [None, None, None, None, None]

        retval = {"Diff_First_Second":  diffVtx0Vtx1,
                  "Diff_Second_Third":  diffVtx1Vtx2,
                  "Diff_Top3":         diffVtx0Vtx12,
                  "Very_Low_Quantile":  qvals[0],
                  "Low_Quantile":      qvals[1],
                  "Mid_Quantile":      qvals[2],
                  "High_Quantile":     qvals[3],
                  "Very_High_Quantile": qvals[4]}
        return retval
        

    def fillVertexProperties(self, debug=False):
        if debug:
            print("Filling Vertex Properties")

        retval = {}
        vertexAttrsDF = self.dn.vInfo.vertexAttrsDF
        dtypes        = vertexAttrsDF.dtypes
        for attribute in vertexAttrsDF.columns:
            if isNumericDtype(dtypes[attribute]):
                vertexData = getColData(vertexAttrsDF, colnames=attribute)            
                retval[attribute] = self.fillObjectProperties(vertexData)

        nodeAttrs = self.dn.getNodeAttrs()
        if not isDataFrame(nodeAttrs):
            if debug:
                print("  There is no NodeAttrs DataFrame")
        else:
            for attribute in nodeAttrs.columns:
                vertexData = getColData(nodeAttrs, colnames=attribute)
                key = "_".join(x.title() for x in attribute.split("_"))
                retval[key] = self.fillObjectProperties(vertexData)

        if debug:
            print("  Filled Vertex Properties for {0} Attributes".format(len(retval)))
            
        self.features["Vertex_Properties"] = retval
        

    def fillEdgeProperties(self, debug=False):
        if debug:
            print("Filling Edge Properties")

        retval      = {}
        edgeAttrsDF = self.dn.eInfo.edgeAttrsDF
        dtypes      = edgeAttrsDF.dtypes
        for attribute in edgeAttrsDF.columns:
            if isNumericDtype(dtypes[attribute]):
                edgeData = getColData(edgeAttrsDF, colnames=attribute)
                retval[attribute] = self.fillObjectProperties(edgeData)

        edgeAttrs = self.dn.getEdgeAttrs()
        if not isDataFrame(edgeAttrs):
            if debug:
                print("  There is no EdgeAttrs DataFrame")
        else:
            for attribute in edgeAttrs.columns:
                vertexData = getColData(edgeAttrs, colnames=attribute)            
                key = "_".join(x.title() for x in attribute.split("_"))
                retval[key] = self.fillObjectProperties(vertexData)

        if debug:
            print("  Filled Edge Properties for {0} Attributes".format(len(retval)))
            
        self.features["Edge_Properties"] = retval

        
        
    #################################################################################################################
    # Top Vertex/Edge Features
    #################################################################################################################
    def fillIndividualObjectFeatures(self, objectNum, objectData, debug=False):
        retval = {}
        retval['Rank'] = objectNum
        for category, categoryData in objectData.items():
            for featureName, featureValue in categoryData.items():
                key = "".join([category,featureName])
                if isinstance(featureValue, list):
                    featureValue = len(featureValue)
                elif isinstance(featureValue, dict):
                    continue

                retval[key] = featureValue
        return retval
    

    def fillIndividualVertexFeatures(self, debug=False):
        if debug:
            print("Filling Individual Vertex Features")
        key = "Vertex_Top5"
        retval = {}
        
        for vertexNum, vertexName in enumerate(dn.getVertices()):
            vertexData = self.dn.getVertexByName(vertexName, 'feat')
            retval["{0}".format(vertexNum)] = self.fillIndividualObjectFeatures(vertexNum, vertexData, debug=debug)
            break
            
        if debug:
            print("  Filled Individual Features for {0} Vertices".format(len(retval)))
        self.features[key] = retval
        
        
    def fillIndividualEdgeFeatures(self, debug=False):
        if debug:
            print("Filling Individual Edge Features")
        key = "Edge_Top5"
        retval = {}
        
        for edgeNum in range(5):
            edge = self.dn.getEdge(edgeNum, 'feat')
            retval["{0}".format(edgeNum)] = self.fillIndividualObjectFeatures(edgeNum, edge, debug=debug)
            
        if debug:
            print("  Filled Individual Features for {0} Edges".format(len(retval)))            
        self.features[key] = retval
        
        
    def fillNetworkFeatures(self, debug=False):
        if debug:
            print("Filling Network Features")
        key = "Network"
        retval = {}
        
        netAttrs = self.dn.getNetAttrs()
        for featureName, featureValue in netAttrs.items():
            retval[featureName] = featureValue
            
        if debug:
            print("  Filled {0} Network Features".format(len(retval)))
        self.features[key] = retval


    def fillHomeFeatures(self, debug=False):
        if debug:
            print("Filling Home Vertex Features")
        key = "Home"
        retval = {}
                
        vertexName = str(self.dn.homeMetrics['GeoID'])
        vertexData = self.dn.getVertexByName(vertexName, 'feat')
        vertexNum  = self.dn.getVertexNum(vertexName)
        ratio = self.dn.homeMetrics['Ratio']
        ratio_significance = self.getHomeRatioCategory(ratio, debug)
        retval["Ratio"]    = ratio_significance
        retval["Days"]     = self.dn.homeMetrics['Days']
        retval["Days"], _  = self.getIntervalCategory(retval["Days"], debug)
        for featureName, value in self.fillIndividualObjectFeatures(vertexNum, vertexData).items():
            retval[featureName] = value

        if debug:
            print("  Filled {0} Home Vertex Features".format(len(retval)))
            
        self.features[key] = retval
        
                
        
    #################################################################################################################
    # Feature Correlations
    #################################################################################################################
    def fillVertexFeatureCorrelations(self, debug=False):
        if debug:
            print("Filling Vertex Feature Correlations")
        key = "Vertex_Corr"
        retval = {}
        
        vertexAttrs = self.dn.nodeAttrs
        for i,attribute1 in enumerate(vertexAttrs.columns):
            vertexData1 = getColData(vertexAttrs, colnames=attribute1)
            for j,attribute2 in enumerate(vertexAttrs.columns):
                if j <= i:
                    continue
                    
                vertexData2 = getColData(vertexAttrs, colnames=attribute2)               
                try:
                    corr = vertexData1.corr(vertexData2)
                except:
                    corr = None
                retval["_".join([attribute1, attribute2])] = corr

        if debug:
            print("  Filled {0} Vertex Feature Correlations".format(len(retval)))
            
        self.features[key] = retval
        
        
    def fillEdgeFeatureCorrelations(self, debug=False):
        if debug:
            print("Filling Edge Feature Correlations")
        key = "Edge_Corr"
        retval = {}
        
        edgeAttrs = self.dn.edgeAttrs
        for i,attribute1 in enumerate(edgeAttrs.columns):
            edgeData1 = getColData(edgeAttrs, colnames=attribute1)
            for j,attribute2 in enumerate(edgeAttrs.columns):
                if j <= i:
                    continue
                    
                edgeData2 = getColData(edgeAttrs, colnames=attribute2)               
                try:
                    corr = edgeData1.corr(edgeData2)
                except:
                    corr = None
                retval["_".join([attribute1, attribute2])] = corr

        if debug:
            print("  Filled {0} Edge Feature Correlations".format(len(retval)))
            
        self.features[key] = retval
        
        


    

    #######################################################################################################################
    #
    # Create DataFrame
    #
    #######################################################################################################################
    def getRawFeatures(self, debug=False):
        return self.features
    
    
    def getFeatureCategories(self, debug=False):
        return list(self.features.keys())
    
    
    def getFeatures(self, subcategory=None, selfeature=None, debug=False):
        from collections import Counter
        features = {}
        cntr = Counter()
        for category, categorydata in self.features.items():
            if subcategory is not None:
                if category != subcategory:
                    continue
            for feature, featuredata in categorydata.items():
                if isinstance(featuredata, dict):
                    for subfeature, subfeaturedata in featuredata.items():
                        key = "_".join([category,feature,subfeature])
                        key = "".join([s for s in key.split("_")])
                        if selfeature is not None:
                            if selfeature not in key:
                                continue
                        value = fixType(subfeaturedata)
                        features[key] = value
                else:
                    if selfeature is not None:
                        if selfeature not in feature:
                            continue
                    key = "_".join([category,feature])
                    key = "".join([s for s in key.split("_")])
                    value = fixType(featuredata)
                    features[key] = value
        
        if debug:
            print("Created Data Frame with {0} features".format(len(features)))

        if False:
            features['Device'] = self.device
            if self.expectedFeatures is not None:
                if len(features) != self.expectedFeatures:
                    print("\nThere are only {0}/{1} features for {2}!!!\n".format(len(features), self.expectedFeatures, self.device))
                    self.printFeatures()
                    raise ValueError("\nThere are only {0}/{1} features for {2}!!!\n".format(len(features), self.expectedFeatures, self.device))

        return features
    
                        
    def getFeatureDataFrame(self, debug=False):
        from pandas import DataFrame
        features = self.getFeatures(debug=debug)
        df = DataFrame(features, index=[0])
        return df
    
    
    def getHomeFeatureDataFrame(self, debug=False):
        from pandas import DataFrame
        features = self.getFeatures(subcategory="Home", debug=debug)
        df = DataFrame(features, index=[0])
        return df
    
    
    def getCategoryFeatureDataFrame(self, category, debug=False):
        from pandas import DataFrame
        features = self.getFeatures(subcategory=category, debug=debug)
        df = DataFrame(features, index=[0])
        return df
    
    
    def getSubFeatureDataFrame(self, selfeature, debug=False):
        from pandas import DataFrame
        features = self.getFeatures(selfeature=selfeature, debug=debug)
        df = DataFrame(features, index=[0])
        return df
    
    
    def getDwellTimeFeatureDataFrame(self, debug=False):
        from pandas import DataFrame
        features = self.getFeatures(selfeature="DwellTime", debug=debug)
        df = DataFrame(features, index=[0])
        return df