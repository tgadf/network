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
        header = OrderedDict({"#": 4, "Cl": 5, "N": 5, "Home": 5, "Active": 7, "DayWeek": 8, "Dwell": 9, "Place": 20, "State": 20, "Cliques": 8, "Cluster": 8, "Degree": 8, "DCentral": 9, "ECentral": 9, "ShortPath": 10, "PageRank": 8})
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
            network    = vertexData["Network"]
            
            if internal['N'] < minN:
                continue
                
            widths = iter(header.values())
            
            ## #
            print('{cmt: <{width}}'.format(cmt=vertexNum, width=next(widths)), end="")            
            
            ## Cl
            print('{cmt: <{width}}'.format(cmt=vertexName, width=next(widths)), end="")
            
            
            n = internal['N']
            if n < minN:
                stop = True
            ## Active
            print('{cmt: <{width}}'.format(cmt=n, width=next(widths)), end="")    
            
            if internal['IsHome'] == 1:
                home = "***"
            else:
                home = ""
            ## Home
            print('{cmt: <{width}}'.format(cmt=home, width=next(widths)), end="")
            
            
            active = internal['FractionalVisits']
            ## Active
            print('{cmt: <{width}}'.format(cmt=active, width=next(widths)), end="")    
            
            
            dow = internal['DayOfWeek']
            ## Day
            print('{cmt: <{width}}'.format(cmt=dow, width=next(widths)), end="")     
            
            
            dwell = internal['DwellTime']
            ## Dwell
            print('{cmt: <{width}}'.format(cmt=dwell, width=next(widths)), end="")    
                
                
            try:
                place=str(vertexData["Census"]["Place"])
            except:
                place=""
            ## CBSA
            print('{cmt: <{width}}'.format(cmt=place, width=next(widths)), end="") 
                
                
            try:
                state=str(vertexData["Census"]["State"])
            except:
                state=""
            ## CBSA
            print('{cmt: <{width}}'.format(cmt=state, width=next(widths)), end="")

            
            
            nocliques = round(network["NumberOfCliques"],3)
            print('{cmt: <{width}}'.format(cmt=nocliques, width=next(widths)), end="")
            
            clustering = round(network["Clustering"],3)
            print('{cmt: <{width}}'.format(cmt=clustering, width=next(widths)), end="")
            
            degree = round(network["AverageNeighborDegree"],2)
            print('{cmt: <{width}}'.format(cmt=degree, width=next(widths)), end="")
            
            degree = round(network["DegreeCentrality"],3)
            print('{cmt: <{width}}'.format(cmt=degree, width=next(widths)), end="")
            
            degree = round(network["EigenvectorCentrality"],3)
            print('{cmt: <{width}}'.format(cmt=degree, width=next(widths)), end="")
            
            degree = round(network["ShortestPath"],3)
            print('{cmt: <{width}}'.format(cmt=degree, width=next(widths)), end="")
            
            degree = round(network["Pagerank"],3)
            print('{cmt: <{width}}'.format(cmt=degree, width=next(widths)), end="")
            
        
        
            print("") 
            #print("Center")
            #print(vertexData)
            #break
            
            
        
        
    #################################################################################################################
    # Print/Show Network
    #################################################################################################################
    def printEdges(self, minW=5, debug=False):
        edges = self.dn.getEdges()
        print("\n\n======================================== {0} Edges (min {1}) ========================================\n".format(len(edges), minW))
        from collections import OrderedDict
        header = OrderedDict({"#": 4, "ID": 18, "N": 5, "Active": 7, "DayWeek": 8, "Distance": 9, "Place": 20}) #, "State": 20, "Cliques": 8, "Cluster": 8, "Degree": 8, "DCentral": 9, "ECentral": 9, "ShortPath": 10, "PageRank": 8})
        for k,v in header.items():
            print('{cmt: <{width}}'.format(cmt=k, width=v), end="")
        print("")
        for k,v in header.items():
            print('{cmt: <{width}}'.format(cmt='---', width=v), end="")
        print("")
        for edgeNum,edgeName in enumerate(edges):
            edgeData = self.dn.getEdgeByName(edgeName, 'feat')
            internal = edgeData["Internal"]
            network  = edgeData["Network"]
            
            if network['EdgeWeight'] < minW:
                continue
            
            widths = iter(header.values())
            
            ## #
            print('{cmt: <{width}}'.format(cmt=edgeNum, width=next(widths)), end="")            
            
            ## Cl
            ID = str(edgeName)
            print('{cmt: <{width}}'.format(cmt=ID, width=next(widths)), end="")

            
            
            n = int(network['EdgeWeight'])
            ## Active
            print('{cmt: <{width}}'.format(cmt=n, width=next(widths)), end="")    
            
            
            
            
            active = internal['FractionalActive']
            ## Active
            print('{cmt: <{width}}'.format(cmt=active, width=next(widths)), end="")    
            
            
            dow = internal['DayOfWeek']
            ## Day
            print('{cmt: <{width}}'.format(cmt=dow, width=next(widths)), end="")     
            
            
            dist = internal['DrivingDistance']
            ## dist
            print('{cmt: <{width}}'.format(cmt=dist, width=next(widths)), end="")    
                
            try:
                place=str(edgeData["Census"]["Place"])
            except:
                place=""
            ## CBSA
            print('{cmt: <{width}}'.format(cmt=place, width=next(widths)), end="") 
                
            print("")
            
            