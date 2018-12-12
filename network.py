import networkx as nx
from edgeInfo import edgeInfo
from vertexInfo import vertexInfo

class network():
    def __init__(self, directed=True, debug=False):
        self.debug = debug
        self.directed = directed
        
        self.orderedEdges    = None
        self.edgeDict        = None
        self.orderedVertices = None
        self.nodeDict        = None
        
        if self.directed is True:
            self.g = nx.DiGraph()
        else:
            self.g = nx.Graph()

        self.eInfo            = edgeInfo(self.g, self.debug)
        self.getEdges         = self.eInfo.getEdges
        self.getEdge          = self.eInfo.getEdgeData
        self.getEdgeByName    = self.eInfo.getEdgeDataByName
        self.getEdgeAttrsGroups     = self.eInfo.getAttrGroups
        self.setEdgeFeature   = self.eInfo.setEdgeFeature        
        self.getEdgeFeature   = self.eInfo.getEdgeFeature
        self.getEdgeFeatures  = self.eInfo.getEdgeFeatures
        self.getEdgeNum       = self.eInfo.getEdgeNumByName
        
        self.vInfo                  = vertexInfo(self.g, self.debug)
        self.getVertices            = self.vInfo.getVertices
        self.getVertex              = self.vInfo.getVertexData
        self.getVertexByName        = self.vInfo.getVertexDataByName
        self.getVertexAttrsGroups   = self.vInfo.getAttrGroups
        self.setVertexFeature       = self.vInfo.setVertexFeature
        self.getVertexFeature       = self.vInfo.getVertexFeature
        self.getVertexFeatures      = self.vInfo.getVertexFeatures
        self.getVertexNum           = self.vInfo.getVertexNumByName
            
    def setDebug(self, debug):
        self.debug = debug
        
    def getNetwork(self):
        return self.g
    
    
    def update(self, debug=False):
        if debug:
            print("Updating Vertices/Edges")
        self.eInfo.orderEdges(debug=debug)
        self.vInfo.orderVertices(debug=debug)
        
            
    def flattenAttrs(self, debug=False):
        if debug:
            print("Flattening Vertices/Edges")
        self.eInfo.flattenEdgeAttrs(debug=debug)
        self.vInfo.flattenVertexAttrs(debug=debug)
        
    
    def collectAttrs(self, debug=False):
        if debug:
            print("Collecting Vertices/Edges")
        self.eInfo.collectEdgeAttrs(debug=debug)
        self.vInfo.collectVertexAttrs(debug=debug)
    
        if debug:
            print("Creating Vertex Attrs DataFrame")
        self.vInfo.createVertexAttrsDataFrame(debug=debug)
    
        if debug:
            print("Creating Edge Attrs DataFrame")
        self.eInfo.createEdgeAttrsDataFrame(debug=debug)
    
    
    
    
    ################################################################################################
    # Show Network Data
    ################################################################################################    
    def showVertices(self):
        for nodename,node in self.g.nodes_iter(data=True):
            print(nodename,'\t',node)
                
    def showEdges(self):
        for edgename,edge in self.g.adj.items():
            print(edgename,'\t',edge)
                
                

        
    ################################################################################################
    # Vertices / Nodes / Location (Initial Functions)
    ################################################################################################    
    def addVertex(self, name, attrs={}):
        self.g.add_node(u=name, attr_dict=attrs)
        if self.debug:
            print("  Added node: [{0}]".format(", ".join(names)))
                    
    def updateVertexAttrs(self, attrs, debug=False):
        if debug:
            print("Updating Vertex Attributes")
        if not isinstance(attrs, dict):
            print("Cannot add vertex attrs because the input is not a dict")
            return
        nx.set_node_attributes(G=self.g, values=attrs, name=None)
            
        
        
    ################################################################################################
    # Edges / Trips (Initial Functions)
    ################################################################################################    
    def addEdge(self, names, attrs={}, sort=False):
        if not isinstance(names, (tuple,list,set)):
            print("Cannot add edge {0} because the names need to come in a tuple/list/set.".format(names))
            return
        if len(names) == 2:
            if sort is True:
                names = sorted([str(x) for x in names])
            else:
                names = [str(x) for x in names]
        else:
            print("Cannot add edge {0} because we need two entries in the tuple/list/set.".format(names))
            return
        
        self.g.add_edge(names[0], names[1], attr_dict=attrs)
        if self.debug:
            print("  Added edge: [{0}]".format(", ".join(names)))
            
    def updateEdgeAttrs(self, attrs):
        if not isinstance(attrs, dict):
            print("Cannot add edge attrs because the input is not a dict")
            return
        nx.set_edge_attributes(G=self.g, values=attrs)