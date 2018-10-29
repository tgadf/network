import pygeohash as geohash
from timeUtils import clock, elapsed
from shapely.geometry.polygon import Polygon
from shapely.geometry import Point
from pygeohash import neighbors, getGeoChars, encode, decode_exactly
from numpy import ceil,fabs,asarray
from random import random
from os.path import basename, join, splitext, isdir, splitext
import zipfile
from shapefile import Reader
import pickle
from collections import Counter
from shutil import rmtree
from haversine import haversine
    
def getBBox(shape):
    bbox = [float('%.6f' % coord) for coord in shape.bbox]
    return bbox


def getPolygon(shape):
    try:
        poly = Polygon(shape.points)
    except:
        poly = None
        
    
def addGeos(geos, geo, init=False):
    nAdd  = 0
    nGeos = len(geos)
    geos.add(geo)
    neighbors = set(geohash.neighbors(geo)).difference(geos)
    for neighbor in list(neighbors):
        geos.add(neighbor)
        nneighbors = set(geohash.neighbors(neighbor)).difference(geos)
        for nneighbor in list(nneighbors):
            geos.add(nneighbor)
    dAdd = len(geos) - nGeos
    if dAdd > 0:
        return 0
    else:
        if init:
            return 0
        return 1
    
    
def addLinearGeos(irec, nshapes, shape, prec, maxmiss=None, debug=True):
    geos = set()
    for i,pnt in enumerate(shape.points):
        long,lat = pnt
        geo      = geohash.encode(latitude=lat, longitude=long, precision=prec)
        geos.add(geo)
    if debug:
        print("Added {0} geos (guess = N/A) from {1} points.".format(len(geos), len(shape.points)))
    return geos


def addShapeGeos(irec, nshapes, shape, prec, geos, maxmiss=None, debug=True):
    bbox = getBBox(shape)
    lng0      = min([bbox[0], bbox[2]])
    lngrange  = abs(bbox[0] - bbox[2])
    lat0      = min([bbox[1], bbox[3]])
    latrange  = abs(bbox[1] - bbox[3])
    dEW   = 111*latrange
    dNS   = 111*lngrange
    area  = dEW * dNS
    if prec == 3:
        geoarea = 100.9*100.9 / 2
    elif prec == 4:
        geoarea = 20.9*20.9 / 2
    elif prec == 5:
        geoarea = 4.9*4.9 / 2
    elif prec == 6:
        geoarea = 1.2*0.61
    elif prec == 7:
        geoarea = 0.152*0.152 / 2
    elif prec == 8:
        geoarea = 0.038*0.019 / 3
    else:
        raise ValueError("No idea about {0}".format(prec))
        geoarea = None
    ngeoguess = int(ceil(area / geoarea))
    minMR = 2500
    if maxmiss is None:
        maxmiss = min([max([ngeoguess,5]), minMR])

    nmiss=0
    nrounds   = 0
    maxR = 100000
    maxrounds = min([max([5*ngeoguess, 10]), maxR])
    if maxrounds == maxR and False:
        debug=True
    if debug:
        print("  addShapeGeos({0}/{1}\tKm EW = {2}, Km NS  = {3}, Sq Km = {4}, ngeos = {5})".format(irec, nshapes, round(dEW,1), round(dNS,1), round(area,1), ngeoguess), end="\t----> ")
    for i in range(maxrounds):
        nrounds += 1
        genlat = latrange*random() + lat0
        genlng = lngrange*random() + lng0
        geo    = geohash.encode(latitude=genlat, longitude=genlng, precision=prec)
        retval = addGeos(geos, geo)
        if retval == 0:
            nmiss = 0
        else:
            nmiss += 1
        if debug and False: print("\t",i,"\tMiss:\t",nmiss,"Ngeos:\t",len(geos))
        if nmiss > maxmiss:
            break
    if debug:
        print("Added {0} geos (guess = {1}) with {2} round and {3} misses in the end.".format(len(geos), ngeoguess, nrounds, nmiss))
    return 


def getShapeData(shapedir, debug=False):
    name = splitext(basename(shapedir))[0]
    readerName = join(shapedir, name)
    print("Reading ShapeData from {0}, {1} --> {2}".format(shapedir, name, readerName))
    try:
        sf = Reader(readerName)
    except:
        sf = None

        return sf

def getInitGeo(shape, prec=7):
    poly = getPolygon(shape)
    if poly is None:
        geo = set()
        return geos
        
    try:
        center  = poly.centroid
        pnt     = center
        long0   = center.x
        lat0    = center.y
        geo     = geohash.encode(latitude=lat0, longitude=long0, precision=prec)
        geos    = set([geo])
    except:
        geos    = set()
    return geos


def saveGeoData(shapeData, geoShapeMap, Nshapes, ngeos, prefix):
    print("\n")
    if len(shapeData) > 0:
        fname = "{0}-data.p".format(prefix)
        print("There are {0} entries in the saved file.".format(len(shapeData)))
        pickle.dump(shapeData, open(fname, "wb"))
        print("Saved shape data to {0}".format(fname))
        print("\n")
    else:
        print("Not saving shape data because there are entries.")
        
    if len(geoShapeMap) > 0:
        fname = "{0}-geos.p".format(prefix)
        print("There are {0} entries in the saved file.".format(ngeos))
        pickle.dump(geoShapeMap, open(fname, "wb"))
        print("Saved shape data to {0}".format(fname))
        print("\n")
    else:
        print("Not saving geo shape data because there are entries.")
    
def rmZipDir(zipfilename, test=False):
    if isdir(zipfilename):
        extractDirname = zipfilename
    else: 
        extractDirname = splitext(zipfilename)[0]
        
    if isdir(extractDirname):
        print("  ---->>> Removed {0}".format(extractDirname))
        if test is False:
            rmtree(extractDirname)

            
def unZipFile(zipfilename, test=False, debug=True):
    extractDirname = splitext(zipfilename)[0]
    if debug:
        print("Unzipping {0} to {1}".format(zipfilename, extractDirname))
    rmZipDir(extractDirname, test)
    
    if test is False:
        zip_ref = zipfile.ZipFile(zipfilename, 'r')
        zip_ref.extractall(extractDirname)
        zip_ref.close()
    else:
        print("  --> Only testing. Didn't unzip")
    return extractDirname



def isGeoInShape(geo, poly):
    if poly is None:
        return False
    bbox   = [Point(x) for x in getGeoPrimBBox(geo)]
    center = Point(getCenterFromGeo(geo))
    if poly.contains(center):
        return True
    for pnt in bbox:
        if poly.contains(pnt):
            print("Poly is True")
            return True
    return False


def getEWGeos(geo):
    chars = '0123456789bcdefghjkmnpqrstuvwxyz'
    ch    = geo[-1]
    ic    = chars.index(ch)+1
    
    i0 = ic - 1
    imod  = ic & len(chars)
    
    i0 = imod

def getShapeInternalGeos(shape, geos, prec, debug=False, verydebug=False):
    ch = getGeoChars()
    
    ngeos = {}
    poly = getPolygon(shape)
    if poly is None:
        if debug:
            print("Could not create a polygon from this shape. Returning 0 internal geos.")
        return ngeos
    ng = len(geos)
    
    for j,geo in enumerate(geos.keys()):
        if debug:
            if j % 50 == 0:
                print("  Testing for internal shapes for shape {0} out of {1}: Found {2} internal geos so far.".format(j, ng, len(ngeos)))
        ig      = ch.index(geo[-1])
        lat,lng = getCenterFromGeo(geo)
        
        # 'n'        
        nb = 0
        for i in range(1,1000+1):
            nlat = lat + i*getGeoLatWidth(prec)
            #print(i,lng,nlat)
            geo  = encode(latitude=nlat, longitude=lng, precision=prec)
            if i < 2:
                if not poly.contains(Point((lng, nlat))):
                    break
            #if dirs['n'].get(ig) is None:
            #    dirs['n'][ig] = Counter()
            #dirs['n'][ig][ch.index(geo[-1])] += 1
            if geos.get(geo) is not None:
                break
            if ngeos.get(geo) is not None:
                nb += 1
                if nb > 0:
                    break
            ngeos[geo] = {"I": 1}
        
        # 's'
        nb = 0
        for i in range(1,1000+1):
            slat = lat - i*getGeoLatWidth(prec)
            geo  = encode(latitude=slat, longitude=lng, precision=prec)
            if i < 2:
                if not poly.contains(Point((lng, slat))):
                    break
            #if dirs['s'].get(ig) is None:
            #    dirs['s'][ig] = Counter()
            #dirs['s'][ig][ch.index(geo[-1])] += 1
            if geos.get(geo) is not None:
                break
            if ngeos.get(geo) is not None:
                nb += 1
                if nb > 0:
                    break
                break
            ngeos[geo] = {"I": 1}
            
        
    for geo in geos.keys():
        continue
        ig      = ch.index(geo[-1])
        lat,lng = getCenterFromGeo(geo)
        
        # 'w'
        nb = 0
        for i in range(1,1000+1):
            wlng = lng - i*getGeoLngWidth(prec)
            #print(i,wlng,lat)
            geo  = encode(latitude=lat, longitude=wlng, precision=prec)
            if dirs['w'].get(ig) is None:
                dirs['w'][ig] = Counter()
            dirs['w'][ig][ch.index(geo[-1])] += 1
            if geos.get(geo) is not None:
                break
            if ngeos.get(geo) is not None:
                nb += 1
                if nb > 1:
                    break
            if not poly.contains(Point((wlng, lat))):
                break
            ngeos[geo] = {"I": 1}
        
        # 'e'
        nb = 0
        for i in range(1,1000+1):
            elng = lng + i*getGeoLngWidth(prec)
            #print(i,elng,lat)
            geo  = encode(latitude=lat, longitude=elng, precision=prec)
            if dirs['e'].get(ig) is None:
                dirs['e'][ig] = Counter()
            dirs['e'][ig][ch.index(geo[-1])] += 1
            if geos.get(geo) is not None:
                break
            if ngeos.get(geo) is not None:
                nb += 1
                if nb > 1:
                    break
            if not poly.contains(Point((elng, lat))):
                break
            ngeos[geo] = {"I": 1}
        

        if False:
            for check in neighbors(geo):
                ic   = check[-1]
                dist = getDistance(geo,check)
                if dist < -0.7:
                    print(geo,'\t',check,'\t','ew','\t',ch.index(ig),ch.index(ic))
                elif getDistance(geo,check) < 1:
                    idx = ch.index(ig)
                    if idx % 4 == 3:
                        print(geo,'\t',check,'\t','ns','\t',ch.index(ig),ch.index(ic))
                        
    return ngeos


def mergeInternalGeos(ngeos, prec, debug=False, verydebug=False):
    
    apps = []
    intgeos = list(ngeos.keys())
    if debug:
        print("Starting with {0} geos".format(len(intgeos)))
    while apps is not None:
        apps = []

        intgeos = list(ngeos.keys())
        testset = Counter([x[:prec-1] for x in intgeos])
        if debug:
            print("  Checking for mergers with precision {0} for {1} geos out of {2}".format(prec-1, len(testset), len(intgeos)))
        for geo,geocnt in testset.most_common():
            if geocnt == 32:
                apps.append(geo)
                
        if False:
            for it,geo in enumerate(testset):
                if it % 100 == 0:
                    print("    Processing {0}/{1} possible mergers. Found {2} so far.".format(it, len(testset), len(apps)))
                check = len([x for x in intgeos if x.startswith(geo)])
                if check == 32:
                    apps.append(geo)

        if debug:
            print("  Found {0} mergers with precision {1}".format(len(apps), prec-1))
                
        if len(apps) == 0:
            intgeos = list(ngeos.keys())
            if debug:
                print("Breaking due to lack of mergers with {0} geos".format(len(intgeos)))
            break
            
        for geo in apps:
            for ch in getGeoChars():
                try:
                    del ngeos["{0}{1}".format(geo, ch)]
                except:
                    if debug:
                        print("There was an error trying to delete {0}".format(geo, ch))
                        
            ngeos[geo] = {"I": 1}
    
        prec -= 1
        intgeos = list(ngeos.keys())
        if debug:
            print("Ending with {0} geos".format(len(intgeos)))
    
    return ngeos


    
#######################################################################################################################
# Find boundary geos
#######################################################################################################################
def getShapeGeos(shape, prec, debug=False, verydebug=False):
    
    geos = {}
    
    ## Get geos for outer shape
    nPoints = len(shape.points)
    if debug:
        print("Lat Rat = {0}".format(getGeoLatWidth(prec)))
        print("Lng Rat = {0}".format(getGeoLngWidth(prec)))
        print("i / nP\t\tDist\t\tdLat\t\tLatR\t\tdLng\t\tLngR\t\tRatio")
    for i,pnt in enumerate(shape.points):
        long0 = pnt[0]
        lat0  = pnt[1]
        geo   = encode(latitude=lat0, longitude=long0, precision=prec)
        if geos.get(geo) is None:
            geos[geo] = {"I": 1, "O": 1}
            
        if i < nPoints - 1:
            nlong0,nlat0 = shape.points[i+1]
            
            dLat = nlat0  - lat0
            dLng = nlong0 - long0
            dist = getDistance(shape.points[i], shape.points[i+1])

            latRatio = fabs(dLat) / getGeoLatWidth(prec)
            lngRatio = fabs(dLng) / getGeoLngWidth(prec)
            
            midPoints = int(ceil(max([latRatio,lngRatio])))-1
            for j in range(1,midPoints+1):
                midLat = lat0  + j*dLat/(midPoints+1)
                midLng = long0 + j*dLng/(midPoints+1)
                geo    = encode(latitude=midLat, longitude=midLng, precision=prec)
                if geos.get(geo) is None:
                    geos[geo] = {"I": 1, "O": 1}
            if debug:
                print(i,'/',nPoints,'\t',round(dist,4),'\t',round(fabs(dLat),5),'\t',round(latRatio,4),'\t',round(fabs(dLng),5),'\t',round(lngRatio,4),'\t',midPoints)
            
        if debug:
            print("Adding Point [{0},{1}] and Geo {2}".format(lat0,long0,geo))    
        
    return geos


#######################################################################################################################
# Main function to get geos
#######################################################################################################################
def getGeos(shapedata, prec, linear=False, returnKeys=True, debug=False):
    if debug:
        print("Returning Shape of Size: {0}".format(len(shapedata.points)))
    geos  = getShapeGeos(shapedata, prec=prec, debug=False, verydebug=False)
    if linear is False:
        if debug:
            print("Returning Boundary Geos of Size:  {0}".format(len(geos)))
        ngeos = getShapeInternalGeos(shapedata, geos, prec=prec, debug=debug, verydebug=False)
        if debug:
            print("Returning Internal Geos of Size:  {0}".format(len(ngeos)))
        mgeos = mergeInternalGeos(ngeos, prec=prec, debug=debug, verydebug=False)    
        if debug:
            print("Returning Merged Geos of Size:  {0}".format(len(mgeos)))
    else:
        ngeos = None
        mgeos = None
    
    if not returnKeys:
        return {"Geos": geos, "NGeos": ngeos, "MGeos": mgeos}

    if all([geos, mgeos]):
        keys = set({**geos, **mgeos}.keys())
    else:
        keys = set(geos.keys())
        
    if debug:
        print("Return {0} geos".format(len(keys)))
    return keys
    



#######################################################################################################################
# Helper Functions
#######################################################################################################################
def swap_cols(arr, frm, to):
    arr[:,[frm, to]] = arr[:,[to, frm]]
    return arr



#######################################################################################################################
# Shapefile Iterator
#######################################################################################################################
def getShapeIter(shapename, debug=False):
    try:
        sf = Reader(shapename)
    except:
        if debug:
            print("Could not get shape data in {0}".format(shapename))
        return None
    return sf



#######################################################################################################################
# Shape MetaData
#######################################################################################################################
def getShapeFileInfo(sf, debug=False):
    if sf is None:
        if debug:
            print("Shape file data is None is getShapeFileInfo()")
    
    try:
        num = len(sf.shapes)
    except:
        num = None
        
    try:
        fields = sf.fields
    except:
        fields = None
        
    return {"Num": num, "Fields": fields}



    
#######################################################################################################################
# Find boundary geos
#######################################################################################################################
def getRecordShape(shapename, geoid, debug=False):
    sf = getShapeIter(shapename, debug=debug)
    if sf is None:
        if debug:
            print("Could not get shape iterator when trying to get shape data")
        return None
    
    if debug:
        print("Opened record/shape file with {0}".format(len(sf.shapes())))
        
    for shapeRec in sf.iterShapeRecords():
        record = shapeRec.record
        gid    = record[0]
        if gid == geoid:
            shape = shapeRec.shape
            if debug:
                print("Found shape with record {0}".format(geoid))
            return shape
        
    if debug:
        print("Could not find shape with geoid {0}".format(geoid))
    return None
    
    

#######################################################################################################################
# Get shape data
#######################################################################################################################
def getShapeData(shapename, geoid, debug=False):
    from numpy import asarray
    shapedata = getRecordShape(shapename, geoid, debug=debug)
    sdata     = getShapeArray(shapedata, debug=debug)
    return sdata
    
    

#######################################################################################################################
# Get shape array
#######################################################################################################################
def getShapeArray(shapedata, debug=False):
    if shapedata is not None:
        sdata = shapedata.points
        if debug:
            print("  There are {0} points in the shapefile".format(len(sdata)))
        sdata = swap_cols(asarray(sdata), 0, 1)
    else:
        if debug:
            print("Could not create array from shape record")
        sdata = None
    return sdata


#######################################################################################################################
# Return shape data and geos
#######################################################################################################################
def getShapeAndGeos(shapename, geoid, debug=False):
    shapedata = getRecordShape(shapename, geoid, debug=debug)
    sdata     = getShapeArray(shapedata, debug=debug)
    retval    = getGeos(shapedata, prec=7, returnKeys=False, debug=debug)
    return {"Shape": sdata, "Geos": retval}




def getDistance(point1, point2):
    if isinstance(point1, tuple) and isinstance(point2, tuple):
        return haversine(point1, point2)
    elif isinstance(point1, str) and isinstance(point2, str):
        return haversine(getCenterFromGeo(point1), getCenterFromGeo(point2))
    else:
        return None


def guessStartPrec(shape, debug=False):
    bbox = getBBox(shape)
    dLat,oLat = getLatRange(bbox)
    dLng,oLng = getLngRange(bbox)
    area      = dLat * dLng  

    ## Create Polygon
    poly      = getPolygon(shape)
    if poly is None:
        return 3
    polyarea  = poly.area
    
    for prec in range(4, 9):
        geoarea   = getGeoArea(prec)  

        ## Guess
        ngeoguess = geoarea / polyarea
        if ngeoguess < 10:
            if debug:
                print("Suggest starting with prec={0} with bbox area {1}, shape area {2}, and geo area {3}".format(prec-1, round(area,5), round(polyarea,5), round(geoarea,5)))
            return prec-1
    
    return 3


def getGeoLatWidth(prec):   
    """
L, dX, dY, dX*dY = 2 11.25 5.625 63.28125
L, dX, dY, dX*dY = 3 1.40625 1.40625 1.9775390625
L, dX, dY, dX*dY = 4 0.3515625 0.17578125 0.061798095703125
L, dX, dY, dX*dY = 5 0.0439453125 0.0439453125 0.0019311904907226562
L, dX, dY, dX*dY = 6 0.010986328125 0.0054931640625 6.034970283508301e-05
L, dX, dY, dX*dY = 7 0.001373291015625 0.001373291015625 1.885928213596344e-06
L, dX, dY, dX*dY = 8 0.00034332275390625 0.000171661376953125 5.893525667488575e-08
L, dX, dY, dX*dY = 9 4.291534423828125e-05 4.291534423828125e-05 1.8417267710901797e-09    
    """
    retvals = {}
    retvals[2] = 5.625  
    for i in range(3, 12):
        if i % 2 == 0:
            retvals[i] = retvals[i-1]/8
        else:
            retvals[i] = retvals[i-1]/4
            
    return retvals[prec]

def getGeoLatWidthDistance(prec, long):
    dLat = getGeoLatWidth(prec)
    pnt1 = (0, long)
    pnt2 = (dLat, long)
    return getDistance(pnt1, pnt2)


def getGeoLngWidth(prec):
    """
L, dX, dY, dX*dY = 2 11.25 5.625 63.28125
L, dX, dY, dX*dY = 3 1.40625 1.40625 1.9775390625
L, dX, dY, dX*dY = 4 0.3515625 0.17578125 0.061798095703125
L, dX, dY, dX*dY = 5 0.0439453125 0.0439453125 0.0019311904907226562
L, dX, dY, dX*dY = 6 0.010986328125 0.0054931640625 6.034970283508301e-05
L, dX, dY, dX*dY = 7 0.001373291015625 0.001373291015625 1.885928213596344e-06
L, dX, dY, dX*dY = 8 0.00034332275390625 0.000171661376953125 5.893525667488575e-08
L, dX, dY, dX*dY = 9 4.291534423828125e-05 4.291534423828125e-05 1.8417267710901797e-09    
    """
    retvals = {}
    retvals[2] = 11.25    
    for i in range(3, 12):
        if i % 2 == 0:
            retvals[i] = retvals[i-1]/4
        else:
            retvals[i] = retvals[i-1]/8
            
    return retvals[prec]


def getGeoArea(prec):
    ## conv
    conv  = 111    # km/degree
    iconv = 1/conv # degree/km
    
    geoSolidArea = getGeoLatWidth(prec) * getGeoLngWidth(prec)
    return geoSolidArea


def getCenterFromGeo(geo):
    lat,lng = decode_exactly(geo)[:2]
    return (lat,lng)


def getGeoBBox(geo):
    bb = []
    boundbox = bbox(geo)
    routes=[('n', 'w'), ('n', 'e'), ('s', 'e'), ('s', 'w'), ('n', 'w')]
    for route in routes:
        bb.append(tuple([boundbox[route[0]], boundbox[route[1]]]))
    return bb


def getGeoPrimBBox(geo):
    bb = []
    boundbox = bbox(geo)
    n = boundbox['n']
    s = boundbox['s']
    e = boundbox['e']
    w = boundbox['w']
         
    bb.append(tuple([n, w]))
    bb.append(tuple([n, e]))
    bb.append(tuple([s, e]))
    bb.append(tuple([s, w]))
    return bb


def getGeoDiagBBox(geo):
    bb = []
    boundbox = bbox(geo)
    n = boundbox['n']
    s = boundbox['s']
    e = boundbox['e']
    w = boundbox['w']
         
    bb.append(tuple([n, (e+w)/2]))
    bb.append(tuple([(n+s)/2, e]))
    bb.append(tuple([s, (e+w)/2]))
    bb.append(tuple([(n+s)/2, w]))
    return bb


def getGeoQuadBBox(geo):
    bb = []
    boundbox = bbox(geo)
    n = boundbox['n']
    s = boundbox['s']
    e = boundbox['e']
    w = boundbox['w']
         
    bb.append(tuple([n, (3*e+w)/4]))
    bb.append(tuple([(3*n+s)/4, e]))
    bb.append(tuple([s, (3*e+w)/4]))
    bb.append(tuple([(3*n+s)/4, w]))
    
    bb.append(tuple([n, (e+3*w)/4]))
    bb.append(tuple([(n+3*s)/4, e]))
    bb.append(tuple([s, (e+3*w)/4]))
    bb.append(tuple([(n+3*s)/4, w]))
    return bb


def getGeoOctoBBox(geo):
    bb = []
    boundbox = bbox(geo)
    n = boundbox['n']
    s = boundbox['s']
    e = boundbox['e']
    w = boundbox['w']
         
    bb.append(tuple([n, (7*e+w)/8]))
    bb.append(tuple([n, (5*e+3*w)/8]))
    bb.append(tuple([(7*n+s)/8, e]))
    bb.append(tuple([(5*n+3*s)/8, e]))
    bb.append(tuple([s, (7*e+w)/8]))
    bb.append(tuple([s, (5*e+3*w)/8]))
    bb.append(tuple([(7*n+s)/8, w]))
    bb.append(tuple([(5*n+3*s)/8, w]))
         
    bb.append(tuple([n, (e+7*w)/8]))
    bb.append(tuple([n, (3*e+5*w)/8]))
    bb.append(tuple([(n+7*s)/8, e]))
    bb.append(tuple([(3*n+5*s)/8, e]))
    bb.append(tuple([s, (e+7*w)/8]))
    bb.append(tuple([s, (3*e+5*w)/8]))
    bb.append(tuple([(n+7*s)/8, w]))
    bb.append(tuple([(3*n+5*s)/8, w]))
    return bb


def getGeoDeciBBox(geo):
    bb = []
    boundbox = bbox(geo)
    n = boundbox['n']
    s = boundbox['s']
    e = boundbox['e']
    w = boundbox['w']
         
    bb.append(tuple([n, (9*e+w)/10]))
    bb.append(tuple([n, (7*e+3*w)/10]))
    bb.append(tuple([(9*n+s)/10, e]))
    bb.append(tuple([(7*n+3*s)/10, e]))
    bb.append(tuple([s, (9*e+w)/10]))
    bb.append(tuple([s, (7*e+3*w)/10]))
    bb.append(tuple([(9*n+s)/10, w]))
    bb.append(tuple([(7*n+3*s)/10, w]))
         
    bb.append(tuple([n, (e+9*w)/10]))
    bb.append(tuple([n, (3*e+7*w)/10]))
    bb.append(tuple([(n+9*s)/10, e]))
    bb.append(tuple([(3*n+7*s)/10, e]))
    bb.append(tuple([s, (e+9*w)/10]))
    bb.append(tuple([s, (3*e+7*w)/10]))
    bb.append(tuple([(n+9*s)/10, w]))
    bb.append(tuple([(3*n+7*s)/10, w]))
    
    return bb


def getGeoIntPrimBBox(geo):
    bb = []
    boundbox = bbox(geo)
    center   = getCenterFromGeo(geo)    
    n = boundbox['n']
    s = boundbox['s']
    e = boundbox['e']
    w = boundbox['w']
    lat  = center[0]
    lng  = center[1]
    dLat = n - lat
    dLng = e - lng
    for i in range(1,4):
        n -= dLat/4
        s += dLat/4
        w += dLng/4
        e -= dLng/4

        bb.append(tuple([n, w]))
        bb.append(tuple([n, e]))
        bb.append(tuple([s, e]))
        bb.append(tuple([s, w]))
    
    return bb


def getGeoIntDiagBBox(geo):
    bb = []
    boundbox = bbox(geo)
    center   = getCenterFromGeo(geo)     
    n = boundbox['n']
    s = boundbox['s']
    e = boundbox['e']
    w = boundbox['w']
    lat  = center[0]
    lng  = center[1]
    dLat = n - lat
    dLng = e - lng
    for i in range(1,4):
        n -= dLat/4
        s += dLat/4
        w += dLng/4
        e -= dLng/4
         
        bb.append(tuple([n, (e+w)/2]))
        bb.append(tuple([(n+s)/2, e]))
        bb.append(tuple([s, (e+w)/2]))
        bb.append(tuple([(n+s)/2, w]))
    
    return bb


def getGeoIntQuadBBox(geo):
    bb = []
    boundbox = bbox(geo)
    center   = getCenterFromGeo(geo)     
    n = boundbox['n']
    s = boundbox['s']
    e = boundbox['e']
    w = boundbox['w']
    lat  = center[0]
    lng  = center[1]
    dLat = n - lat
    dLng = e - lng
    for i in range(1,4):
        n -= dLat/4
        s += dLat/4
        w += dLng/4
        e -= dLng/4
         
        bb.append(tuple([n, (3*e+w)/4]))
        bb.append(tuple([(3*n+s)/4, e]))
        bb.append(tuple([s, (3*e+w)/4]))
        bb.append(tuple([(3*n+s)/4, w]))

        bb.append(tuple([n, (e+3*w)/4]))
        bb.append(tuple([(n+3*s)/4, e]))
        bb.append(tuple([s, (e+3*w)/4]))
        bb.append(tuple([(n+3*s)/4, w]))
        
    return bb


def getGeoSubIntPrimBBox(geo):
    bb = []
    boundbox = bbox(geo)
    center   = getCenterFromGeo(geo)    
    n = boundbox['n']
    s = boundbox['s']
    e = boundbox['e']
    w = boundbox['w']
    lat  = center[0]
    lng  = center[1]
    dLat = n - lat
    dLng = e - lng
    for i in range(1,10):
        n -= dLat/9
        s += dLat/9
        w += dLng/9
        e -= dLng/9

        bb.append(tuple([n, w]))
        bb.append(tuple([n, e]))
        bb.append(tuple([s, e]))
        bb.append(tuple([s, w]))
    
    return bb


def getGeoSubIntDiagBBox(geo):
    bb = []
    boundbox = bbox(geo)
    center   = getCenterFromGeo(geo)     
    n = boundbox['n']
    s = boundbox['s']
    e = boundbox['e']
    w = boundbox['w']
    lat  = center[0]
    lng  = center[1]
    dLat = n - lat
    dLng = e - lng
    for i in range(1,10):
        n -= dLat/9
        s += dLat/9
        w += dLng/9
        e -= dLng/9
         
        bb.append(tuple([n, (e+w)/2]))
        bb.append(tuple([(n+s)/2, e]))
        bb.append(tuple([s, (e+w)/2]))
        bb.append(tuple([(n+s)/2, w]))
    
    return bb


def getGeoSubIntQuadBBox(geo):
    bb = []
    boundbox = bbox(geo)
    center   = getCenterFromGeo(geo)     
    n = boundbox['n']
    s = boundbox['s']
    e = boundbox['e']
    w = boundbox['w']
    lat  = center[0]
    lng  = center[1]
    dLat = n - lat
    dLng = e - lng
    for i in range(1,10):
        n -= dLat/9
        s += dLat/9
        w += dLng/9
        e -= dLng/9
         
        bb.append(tuple([n, (3*e+w)/4]))
        bb.append(tuple([(3*n+s)/4, e]))
        bb.append(tuple([s, (3*e+w)/4]))
        bb.append(tuple([(3*n+s)/4, w]))

        bb.append(tuple([n, (e+3*w)/4]))
        bb.append(tuple([(n+3*s)/4, e]))
        bb.append(tuple([s, (e+3*w)/4]))
        bb.append(tuple([(n+3*s)/4, w]))
        
    return bb





def isGeoInShape(geo, poly):
    
    isIN  = False
    isOUT = False
    
    ## 1st test the bounding areas
    center = decode_exactly(geo)[:2]
    for i in range(0,3+1):
        if i == 0:
            bbox = getGeoPrimBBox(geo)[:4] + [tuple(center)]
        elif i == 1:
            bbox = getGeoIntDiagBBox(geo)
        elif i == 2:
            bbox = getGeoIntPrimBBox(geo)
        elif i == 3:
            bbox = getGeoSubIntPrimBBox(geo)
        elif i == 4:
            bbox = getGeoQuadBBox(geo)
        elif i == 5:
            bbox = getGeoIntQuadBBox(geo)
        elif i == 6:
            bbox = getGeoDiagBBox(geo)
        elif i == 7:
            bbox = getGeoSubIntQuadBBox(geo)
            
        for lat,lng in bbox:
            pnt = Point(lng,lat)
            if poly.contains(pnt):
                isIN = True
            else:
                isOUT = True

            if isIN and isOUT:
                break
                    
        if isIN and isOUT:
            break
            
    retval = {}
    if isIN:
        retval["I"] = 1
    if isOUT:
        retval["O"] = 1
    return retval


        

def getInitGeo(shape, prec, debug=False):
    poly = getPolygon(shape)
    try:
        pnt   = poly.representative_point()
    except:
        pnt   = poly.centroid
        #pnt    = (center.x, center.y)
        #bbox  = getBBox(shape)
    long0 = pnt.x
    lat0  = pnt.y
    geo   = encode(latitude=lat0, longitude=long0, precision=prec)
    geos = {}
    geos[geo] = {"I": 1, "O": 1}
    if debug:
        print("Initial Point is [{0},{1}] and Geo {2}".format(lat0,long0,geo))
    return geos