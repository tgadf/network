from folium import PolyLine, CircleMarker, Circle, Marker, Icon, FeatureGroup, Map, LayerControl
import geohash


class foliumMap():
    def __init__(self, df=None, pc=None, gc=None, dn=None, nf=None):
        self.pc = None
        if pc is not None:
            self.setProtoClusters(pc)
        self.gc = None
        if gc is not None:
            self.setGeoClusters(gc)
        self.dn = None
        if dn is not None:
            self.setDriverNetwork(dn)
        self.nf = None
        if nf is not None:
            self.setNetworkFeatures(nf)
        self.df = None
        if df is not None:
            self.setTripsDataFrame(df)
        
        self.m  = None
        
        self.init_zoom = 10
        
        self.colors = ['red', 'blue', 'gray', 'darkred', 'lightred', 'orange', 'beige', 'green', 'darkgreen', 'lightgreen',
                       'darkblue', 'lightblue', 'purple', 'darkpurple', 'pink', 'cadetblue', 'lightgray']
        
        
    ########################################################################################
    # Setters
    ########################################################################################
    def setTripsDataFrame(self, df):
        self.df         = df
        self.df         = df[["lat0", "long0"]]
        self.df.columns = ["lat", "long"]
        pnts            = df[["lat1", "long1"]]
        pnts.columns    = ["lat", "long"]    
        self.df         = self.df.append(pnts)
        
    def setProtoClusters(self, pc):
        self.pc = pc
        
    def setGeoClusters(self, gc):
        self.gc = gc
        
    def setDriverNetwork(self, dn):
        self.dn = dn
        
    def setNetworkFeatures(self, nf):
        self.nf = nf
        
        
        
    ########################################################################################
    # Getters
    ########################################################################################        
    def getMap(self):
        return self.m
        
        
        
    ########################################################################################
    ########################################################################################
    # Create Map
    ########################################################################################
    ########################################################################################
    def createMapFromTripsDataFrame(self, zoom=None, debug=False):
        if self.df is None:
            print("There is no trips DataFrame object!")
            return
        
        try:
            lat0           = self.df['lat'].mean()
            long0          = self.df['long'].mean()
        except:
            raise ValueError("Could not get center of geo clusters and create map!")
            
        if zoom is None:
            zoom = self.init_zoom
        self.m = Map(location=[lat0, long0], zoom_start=zoom)
        
        
    def createMapFromProtoClusters(self, zoom=None, debug=False):
        if self.pc is None:
            print("There is no ProtoClusters object!")
            return
        
        try:
            lats  = Series(x["CoM"][0] for pcl,x in self.pc.items())
            lngs  = Series(x["CoM"][1] for pcl,x in self.pc.items())
            lat0  = lats.mean()
            long0 = lngs.mean()
        except:
            raise ValueError("Could not get center of geo clusters and create map!")
            
        if zoom is None:
            zoom = self.init_zoom
        self.m = Map(location=[lat0, long0], zoom_start=zoom)
        
        
    def createMapFromGeoClusters(self, zoom=None, debug=False):
        if self.gc is None:
            print("There is no GeoClusters object!")
            return
        
        try:
            coms  = self.gc.getClusterCoMs()
            lat0  = coms[0].mean()
            long0 = coms[1].mean()
        except:
            raise ValueError("Could not get center of geo clusters and create map!")
            
        if zoom is None:
            zoom = self.init_zoom
        self.m = Map(location=[lat0, long0], zoom_start=zoom)
        
        
    def createMapFromDriverNetwork(self, zoom=None, debug=False):
        if self.dn is None:
            print("There is no DriverNetwork object!")
            return

        try:
            self.dn.createGC()            
            self.gc = self.dn.getGC()
        except:
            raise ValueError("Could not get create geo clusters from driver network")

        try:
            coms  = self.gc.getClusterCoMs()
            lat0  = coms[0].mean()
            long0 = coms[1].mean()
        except:
            raise ValueError("Could not get center of geo clusters and create map!")
        
        
        
        if zoom is None:
            zoom = self.init_zoom
        self.m = Map(location=[lat0, long0], zoom_start=zoom)
        
        
    def createMapFromNetworkFeatures(self, zoom=None, debug=False):
        if self.nf is None:
            print("There is no NetworkFeatures object!")
            return
        
        if zoom is None:
            zoom = self.init_zoom
        self.m = Map(location=[lat0, long0], zoom_start=zoom)
        
        
    def createMap(self, debug=False):
        if self.nf is not None:
            self.createMapFromNetworkFeatures(debug=debug)
        elif self.dn is not None:
            self.createMapFromDriverNetwork(debug=debug)
        elif self.pc is not None:
            self.createMapFromProtoClusters(debug=debug)
        elif self.gc is not None:
            self.createMapFromGeoClusters(debug=debug)
        elif self.df is not None:
            self.createMapFromTripsDataFrame(debug=debug)
        else:
            raise ValueError("Cannot create map because there is no data object!")
            
        
        
    ########################################################################################
    ########################################################################################
    # Points/Clusters
    ########################################################################################
    ########################################################################################      
    def addPointsFromTripsDataFrame(self, debug=False):
        if self.m is None:
            print("Folium Map is None!")
            return
        
        if self.df is None:
            print("DataFrame is None!")
            return
        
        cols = ['darkblue', 'lightblue', 'pink', 'lightgray']
        
        rad = 5
        weight = 1
        for row in self.df.iterrows():
            com = row[1].values
            Circle(com, color=cols[1], radius=rad, fill=True, fill_color=cols[0], weight=weight, opacity=0).add_to(self.m)
    
    def addPointsFromGeoClusterCells(self, debug=False):
        if self.m is None:
            print("Folium Map is None!")
            return
        
        if self.gc is None:
            print("GeoClusters is None!")
            return
        
            

        cells = gc.getCells()
        for geo,cnt in cells.iteritems():
            com    = geohash.decode_exactly(geo)[:2]
            wgt    = int(cnt)
            popup  = str(wgt)
            Circle(com, color='black', radius=5, fill=True, fill_color='black', weight=wgt, opacity=0, popup=popup).add_to(self.m)
    
    
    def addPointsFromProtoClusters(self, debug=False):
        if self.m is None:
            print("Folium Map is None!")
            return
        
        if self.gc is None:
            print("GeoClusters is None!")
            return
        
        cols = ['darkblue', 'lightblue', 'pink', 'lightgray']
        
        from pandas import Series

        for pcl,protoCluster in gc.getProtoClusters().items():
            com    = protoCluster["CoM"]
            rad    = max([protoCluster["Radius"], 5])
            counts = protoCluster["Counts"]
            weight = int(counts)
            name   = pcl
            popup  = "{0} : N = {1}".format(name, counts)

            Circle(com, color=cols[0], radius=rad, fill=True, fill_color=cols[0], weight=weight, opacity=0).add_to(self.m)
    
    
    def addPointsFromSeedlessClusters(self, debug=False):
        if self.m is None:
            print("Folium Map is None!")
            return
        
        if self.gc is None:
            print("GeoClusters is None!")
            return
        
        cols = ['darkgreen']
        
        from pandas import Series

        for scl,seedlessCluster in gc.getSeedlessClusters().items():
            com    = seedlessCluster["CoM"]
            rad    = max([seedlessCluster["Radius"], 5])
            counts = seedlessCluster["Counts"]
            weight = int(counts)
            name   = scl
            popup  = "{0} : N = {1}".format(name, counts)

            Circle(com, color=cols[0], radius=rad, fill=True, fill_color=cols[0], weight=weight, opacity=0).add_to(self.m)
    
    
    def addPointsFromMergedClusters(self, debug=False):
        if self.m is None:
            print("Folium Map is None!")
            return
        
        if self.gc is None:
            print("GeoClusters is None!")
            return
        
        cols = ['darkred']
        
        from pandas import Series

        for cl,cluster in gc.getMergedClusters().items():
            com    = cluster["CoM"]
            rad    = max([cluster["Radius"], 5])
            counts = cluster["Counts"]
            weight = int(counts)
            name   = cl
            popup  = "{0} : N = {1}".format(name, counts)

            Circle(com, color=cols[0], radius=rad, fill=True, fill_color=cols[0], weight=weight, opacity=0).add_to(self.m)
    
    
    def addPointsFromGeoClusters(self, debug=False):
        if self.m is None:
            print("Folium Map is None!")
            return
        
        if self.gc is None:
            print("GeoClusters is None!")
            return
        
        cols = ['darkblue', 'lightblue', 'pink', 'lightgray']
        
        from pandas import Series
        feature_group_1 = FeatureGroup(name="Driver Top 90%")
        feature_group_2 = FeatureGroup(name="Driver Top 75%")
        feature_group_3 = FeatureGroup(name="Driver Top 50%")
        feature_group_4 = FeatureGroup(name="Driver Low 50%")

        weights = Series([cluster.getCounts() for cl,cluster in gc.getClusters().items()])
        alpha   = weights.quantile(0.9)
        beta    = weights.quantile(0.75)
        gamma   = weights.quantile(0.5)

        for cl,cluster in gc.getClusters().items():
            com    = cluster.getCoM()
            rad    = max([cluster.getRadius(), 10])
            counts = cluster.getCounts()
            weight = float(counts)
            quant  = cluster.getQuantiles()
            name   = cl
            cells  = ",".join(cluster.getCells())
            popup  = "{0} : N = {1} : {2}".format(name, weight, com)
            #popup  = ""

            if counts >= alpha:
                Marker(com, icon=Icon(color=cols[0], icon_color='white', icon="car", angle=0, prefix='fa'), popup=popup).add_to(feature_group_1)
                Circle(com, color=cols[0], radius=rad, fill=True, fill_color=cols[0], weight=weight, opacity=0).add_to(feature_group_1)
            elif counts >= beta:
                Marker(com, icon=Icon(color=cols[1], icon_color='white', icon="car", angle=0, prefix='fa'), popup=popup).add_to(feature_group_2)
                Circle(com, color=cols[1], radius=rad, fill=True, fill_color=cols[1], weight=weight, opacity=0).add_to(feature_group_2)
            elif counts >= gamma:
                Marker(com, icon=Icon(color=cols[2], icon_color='white', icon="car", angle=0, prefix='fa'), popup=popup).add_to(feature_group_3)
                Circle(com, color=cols[2], radius=rad, fill=True, fill_color=cols[2], weight=weight, opacity=0).add_to(feature_group_3)
            else:
                Marker(com, icon=Icon(color=cols[3], icon_color='white', icon="car", angle=0, prefix='fa'), popup=popup).add_to(feature_group_4)
                Circle(com, color=cols[3], radius=rad, fill=True, fill_color=cols[3], weight=weight, opacity=0).add_to(feature_group_4)

        feature_group_1.add_to(self.m)
        feature_group_2.add_to(self.m)
        feature_group_3.add_to(self.m)
        feature_group_4.add_to(self.m)
        LayerControl().add_to(self.m)
        
        
     
    def addPointsFromDriverNetwork(self, debug=False):
        if self.m is None:
            print("Folium Map is None!")
            return
        
        if self.dn is None:
            print("DrivingNetwork is None!")
            return
        
        if self.gc is None:
            print("GeoClusters is None!")
            return
        
        cols = ['darkblue', 'lightblue', 'pink', 'lightgray']
        
        from pandas import Series
        feature_group_1 = FeatureGroup(name="Driver Home")
        feature_group_2 = FeatureGroup(name="Daily Visits")
        feature_group_3 = FeatureGroup(name="Weekly Visits")
        feature_group_4 = FeatureGroup(name="Monthly Visits")
        feature_group_5 = FeatureGroup(name="Infrequent Visits")

        clusters = self.gc.getClusters()

        for vertexName in self.dn.getVertices():
            if vertexName == 'None':
                continue
            cluster = clusters[vertexName]
            clname  = cluster.getName()
            com     = cluster.getCoM()
            rad     = max([int(cluster.getRadius()), 10])
            
            weight = 10
            clusterFeatures = self.dn.getVertexByName(vertexName, "feat")
            home   = clusterFeatures["Internal"]["IsHome"]
            place  = clusterFeatures["Census"]["Place"]
            active = clusterFeatures["Internal"]["FractionalVisits"]
            visits = clusterFeatures["Internal"]["DailyVisits"]
            pois   = ", ".join([k for k,v in clusterFeatures["GeoSpatial"].items() if v > 0])
            popup = "{0} ({1}) : N = {2} : fActive = {3} : POIs: {4} : {5}".format(vertexName, place, weight, active, pois, com)
            #print(vertexName,popup)

            if home == 1:
                Marker(com, icon=Icon(color='darkred', icon_color='white', icon="home", angle=0, prefix='fa'), popup=popup).add_to(feature_group_1)
                Circle(com, color='darkred', radius=rad, fill=True, fill_color='darkred', weight=weight, opacity=0).add_to(feature_group_1)
            elif active == "Daily":
                Marker(com, icon=Icon(color=cols[0], icon_color='white', icon="car", angle=0, prefix='fa'), popup=popup).add_to(feature_group_2)
                Circle(com, color=cols[0], radius=rad, fill=True, fill_color=cols[0], weight=weight, opacity=0).add_to(feature_group_2)
            elif active == "Weekly":
                Marker(com, icon=Icon(color=cols[1], icon_color='white', icon="car", angle=0, prefix='fa'), popup=popup).add_to(feature_group_3)
                Circle(com, color=cols[1], radius=rad, fill=True, fill_color=cols[1], weight=weight, opacity=0).add_to(feature_group_3)
            elif active == "Monthly":
                Marker(com, icon=Icon(color=cols[2], icon_color='white', icon="car", angle=0, prefix='fa'), popup=popup).add_to(feature_group_4)
                Circle(com, color=cols[2], radius=rad, fill=True, fill_color=cols[2], weight=weight, opacity=0).add_to(feature_group_4)
            else:
                Marker(com, icon=Icon(color=cols[3], icon_color='white', icon="car", angle=0, prefix='fa'), popup=popup).add_to(feature_group_5)
                Circle(com, color=cols[3], radius=rad, fill=True, fill_color=cols[3], weight=weight, opacity=0).add_to(feature_group_5)

        feature_group_1.add_to(self.m)
        feature_group_2.add_to(self.m)
        feature_group_3.add_to(self.m)
        feature_group_4.add_to(self.m)
        feature_group_5.add_to(self.m)
        LayerControl().add_to(self.m)        
        
           
    def addPoints(self, debug=False):
        if self.m is None:
            raise ValueError("Cannot add points to an empty map")
        if self.nf is not None:
            self.addPointsFromNetworkFeatures(debug=debug)
        elif self.dn is not None:
            self.addPointsFromDriverNetwork(debug=debug)
        elif self.pc is not None:
            self.addPointsFromProtoClusters(debug=debug)
        elif self.gc is not None:
            self.addPointsFromGeoClusters(debug=debug)
        elif self.df is not None:
            self.addPointsFromTripsDataFrame(debug=debug)
        else:
            print("Cannot add points because there is map and object!")