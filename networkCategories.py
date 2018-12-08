## categories Class

class categories():
    def __init__(self, debug=False):
        self.catmap        = {}
        self.cats          = {}
        self.catgetter     = {}
        self.permcats      = {}
        self.permcatgetter = {}
        self.featureMap    = {}
        
        ## Delimeter
        self.delim = "--"

        ## Vertex
        self.cats['HomeRatio']         = self.getHomeRatioCategories(debug)
        self.catgetter['HomeRatio']    = self.getHomeRatioCategory
        
        ## Census
        
        #### Place
        self.featureMap['CensusPlace']   = self.getPlaceFeatures
        self.catmap['CensusPlace']       = ['PlacePop', 'PlaceHousing', 'PlaceArea', 'PlaceType']
        self.cats['PlacePop']            = self.getPlacePopCategories(debug)
        self.catgetter['PlacePop']       = self.getPlacePopCategory
        self.cats['PlaceType']           = self.getPlaceTypeCategories(debug)
        self.catgetter['PlaceType']      = self.getPlaceTypeCategory
        self.cats['PlaceHousing']           = self.getPlaceTypeCategories(debug)
        self.catgetter['PlaceHousing']      = self.getPlaceTypeCategory
        self.cats['PlaceArea']           = self.getPlaceAreaCategories(debug)
        self.catgetter['PlaceArea']      = self.getPlaceAreaCategory
        self.permcats['CensusPlacePop']        = self.getPlacePopPermCategories(debug)
        self.permcatgetter['CensusPlacePop']   = self.getPlacePopPermCategory
        self.permcats['CensusPlaceHousing']        = self.getPlaceHousingPermCategories(debug)
        self.permcatgetter['CensusPlaceHousing']   = self.getPlaceHousingPermCategory
        self.permcats['CensusPlaceArea']        = self.getPlaceAreaPermCategories(debug)
        self.permcatgetter['CensusPlaceArea']   = self.getPlaceAreaPermCategory
        self.permcats['CensusPlaceType']       = self.getPlaceTypePermCategories(debug)
        self.permcatgetter['CensusPlaceType']  = self.getPlaceTypePermCategory

        
        #### MetDiv
        self.featureMap['CensusMetdiv']   = self.getMetDivFeatures
        self.catmap['CensusMetdiv']       = ['MetDivPop', 'MetDivHousing', 'MetDivArea', 'MetDivType']
        self.cats['MetDivPop']            = self.getMetDivPopCategories(debug)
        self.catgetter['MetDivPop']       = self.getMetDivPopCategory
        self.cats['MetDivType']           = self.getMetDivTypeCategories(debug)
        self.catgetter['MetDivType']      = self.getMetDivTypeCategory
        self.cats['MetDivHousing']           = self.getMetDivTypeCategories(debug)
        self.catgetter['MetDivHousing']      = self.getMetDivTypeCategory
        self.cats['MetDivArea']           = self.getMetDivAreaCategories(debug)
        self.catgetter['MetDivArea']      = self.getMetDivAreaCategory
        self.permcats['CensusMetdivPop']        = self.getMetDivPopPermCategories(debug)
        self.permcatgetter['CensusMetdivPop']   = self.getMetDivPopPermCategory
        self.permcats['CensusMetdivHousing']        = self.getMetDivHousingPermCategories(debug)
        self.permcatgetter['CensusMetdivHousing']   = self.getMetDivHousingPermCategory
        self.permcats['CensusMetdivArea']        = self.getMetDivAreaPermCategories(debug)
        self.permcatgetter['CensusMetdivArea']   = self.getMetDivAreaPermCategory
        self.permcats['CensusMetdivType']       = self.getMetDivTypePermCategories(debug)
        self.permcatgetter['CensusMetdivType']  = self.getMetDivTypePermCategory

        
        #### CBSA
        self.featureMap['CensusCbsa']   = self.getCBSAFeatures
        self.catmap['CensusCbsa']       = ['CBSAPop', 'CBSAHousing', 'CBSAArea', 'CBSAType']
        self.cats['CBSAPop']            = self.getCBSAPopCategories(debug)
        self.catgetter['CBSAPop']       = self.getCBSAPopCategory
        self.cats['CBSAType']           = self.getCBSATypeCategories(debug)
        self.catgetter['CBSAType']      = self.getCBSATypeCategory
        self.cats['CBSAHousing']           = self.getCBSATypeCategories(debug)
        self.catgetter['CBSAHousing']      = self.getCBSATypeCategory
        self.cats['CBSAArea']           = self.getCBSAAreaCategories(debug)
        self.catgetter['CBSAArea']      = self.getCBSAAreaCategory
        self.permcats['CensusCbsaPop']        = self.getCBSAPopPermCategories(debug)
        self.permcatgetter['CensusCbsaPop']   = self.getCBSAPopPermCategory
        self.permcats['CensusCbsaHousing']        = self.getCBSAHousingPermCategories(debug)
        self.permcatgetter['CensusCbsaHousing']   = self.getCBSAHousingPermCategory
        self.permcats['CensusCbsaArea']        = self.getCBSAAreaPermCategories(debug)
        self.permcatgetter['CensusCbsaArea']   = self.getCBSAAreaPermCategory
        self.permcats['CensusCbsaType']       = self.getCBSATypePermCategories(debug)
        self.permcatgetter['CensusCbsaType']  = self.getCBSATypePermCategory

        
        #### CSA
        self.featureMap['CensusCsa']   = self.getCSAFeatures
        self.catmap['CensusCsa']       = ['CSAPop', 'CSAHousing', 'CSAArea', 'CSAType']
        self.cats['CSAPop']            = self.getCSAPopCategories(debug)
        self.catgetter['CSAPop']       = self.getCSAPopCategory
        self.cats['CSAType']           = self.getCSATypeCategories(debug)
        self.catgetter['CSAType']      = self.getCSATypeCategory
        self.cats['CSAHousing']           = self.getCSATypeCategories(debug)
        self.catgetter['CSAHousing']      = self.getCSATypeCategory
        self.cats['CSAArea']           = self.getCSAAreaCategories(debug)
        self.catgetter['CSAArea']      = self.getCSAAreaCategory
        self.permcats['CensusCsaPop']        = self.getCSAPopPermCategories(debug)
        self.permcatgetter['CensusCsaPop']   = self.getCSAPopPermCategory
        self.permcats['CensusCsaHousing']        = self.getCSAHousingPermCategories(debug)
        self.permcatgetter['CensusCsaHousing']   = self.getCSAHousingPermCategory
        self.permcats['CensusCsaArea']        = self.getCSAAreaPermCategories(debug)
        self.permcatgetter['CensusCsaArea']   = self.getCSAAreaPermCategory
        self.permcats['CensusCsaType']       = self.getCSATypePermCategories(debug)
        self.permcatgetter['CensusCsaType']  = self.getCSATypePermCategory

        
        #### County
        self.featureMap['CensusCounty']   = self.getCountyFeatures
        self.catmap['CensusCounty']       = ['CountyPop', 'CountyHousing', 'CountyArea', 'CountyType']
        self.cats['CountyPop']            = self.getCountyPopCategories(debug)
        self.catgetter['CountyPop']       = self.getCountyPopCategory
        self.cats['CountyType']           = self.getCountyTypeCategories(debug)
        self.catgetter['CountyType']      = self.getCountyTypeCategory
        self.cats['CountyHousing']           = self.getCountyTypeCategories(debug)
        self.catgetter['CountyHousing']      = self.getCountyTypeCategory
        self.cats['CountyArea']           = self.getCountyAreaCategories(debug)
        self.catgetter['CountyArea']      = self.getCountyAreaCategory
        self.permcats['CensusCountyPop']        = self.getCountyPopPermCategories(debug)
        self.permcatgetter['CensusCountyPop']   = self.getCountyPopPermCategory
        self.permcats['CensusCountyHousing']        = self.getCountyHousingPermCategories(debug)
        self.permcatgetter['CensusCountyHousing']   = self.getCountyHousingPermCategory
        self.permcats['CensusCountyArea']        = self.getCountyAreaPermCategories(debug)
        self.permcatgetter['CensusCountyArea']   = self.getCountyAreaPermCategory
        self.permcats['CensusCountyType']       = self.getCountyTypePermCategories(debug)
        self.permcatgetter['CensusCountyType']  = self.getCountyTypePermCategory

        
        #### State
        self.featureMap['CensusState']   = self.getStateFeatures
        #self.catmap['CensusState']       = ['StatePop', 'CountyHousing', 'CountyArea', 'CountyType']

        
        #### Region
        self.featureMap['CensusRegion'] = self.getStateFeatures
        self.cats['CensusRegion']       = self.getRegionCategories(debug)
        self.catgetter['CensusRegion']  = self.getRegionCategory

        self.cats['POIUniqueVisits']           = self.getPOICategories(debug)
        self.catgetter['POIUniqueVisits']      = self.getPOICategory
        
        self.cats['DwellTime']      = self.getDwellTimeCategories(debug)
        self.catgetter['DwellTime'] = self.getDwellTimeCategory
        

        ## Mixed
        self.cats['DayOfWeek']      = self.getDayOfWeekCategories(debug)
        self.catgetter['DayOfWeek'] = self.getDayOfWeekCategory
                
        ## Edge
        self.cats['Duration']       = self.getDurationCategories(debug)
        self.catgetter['DayOfWeek'] = self.getDurationCategory
        self.cats['Distance']       = self.getDistanceCategories(debug)
        self.catgetter['Distance']  = self.getDistanceCategory
        self.cats['GeoDistanceRatio']       = self.getDistanceRatioCategories(debug)
        self.catgetter['GeoDistanceRatio']  = self.getDistanceRatioCategory
        self.cats['DrivingDistance']       = self.getDistanceCategories(debug)
        self.catgetter['GeoDistance']  = self.getDistanceCategory
        self.cats['GeoDistance']       = self.getDistanceCategories(debug)
        self.catgetter['DrivingDistance']  = self.getDistanceCategory
        self.cats['Interval']       = self.getIntervalCategories(debug)
        self.catgetter['Interval']  = self.getIntervalCategory
        self.cats['FractionalActive']       = self.getFractionActiveCategories(debug)
        self.catgetter['FractionalActive']  = self.getFractionActiveCategory
        self.cats['FractionalVisits']       = self.getFractionVisitsCategories(debug)
        self.catgetter['FractionalVisits']  = self.getFractionVisitsCategory
        self.cats['OvernightStays']       = self.getOvernightStaysCategories(debug)
        self.catgetter['OvernightStays']  = self.getOvernightStaysCategory
        self.cats['DailyVisits']       = self.getDailyVisitsCategories(debug)
        self.catgetter['DailyVisits']  = self.getDailyVisitsCategory
        self.cats['ITA']            = self.getITACategories(debug)
        self.catgetter['ITA']       = self.getITACategory
        
        
        ## Permutations
        self.permcats['POIUniqueVisits']               = self.getPOIPermCategories(debug)
        self.permcatgetter['POIUniqueVisits']          = self.getPOIPermCategory
        self.permcats['DwellTime']         = self.getDwellTimePermCategories(debug)
        self.permcatgetter['DwellTime']    = self.getDwellTimePermCategory

        
        
        self.featureMap['DwellTime']        = self.getDwellTimeFeatures
        self.featureMap['Duration']         = self.getDurationFeatures
        self.featureMap['Distance']         = self.getDistanceFeatures
        self.featureMap['DrivingDistance']  = self.getDistanceFeatures
        self.featureMap['GeoDistance']      = self.getDistanceFeatures
        self.featureMap['GeoDistanceRatio']  = self.getDistanceRatioFeatures
        self.featureMap['Interval']         = self.getIntervalFeatures
        self.featureMap['FractionalActive']         = self.getFractionActiveFeatures
        self.featureMap['FractionalVisits']         = self.getFractionVisitsFeatures
        self.featureMap['OvernightStays']         = self.getOvernightStaysFeatures
        self.featureMap['DailyVisits']         = self.getDailyVisitsFeatures
        self.featureMap['DayOfWeek']        = self.getDayOfWeekFeatures
        self.featureMap['ITA']              = self.getITAFeatures
        self.featureMap['N']                = self.getNFeatures
        #self.featureMap['Weight']           = self.getWeightFeatures
        self.featureMap['POIUniqueVisits']  = self.getPOIFeatures
        self.featureMap['HEREPOIAttraction']   = self.getNumericalFeatures

        ## External Data
        self.cats['HEREPOIAttraction']              = self.getNumericalCategories(debug)
        self.catgetter['HEREPOIAttraction']         = self.getNumericalCategory
        self.permcats['HEREPOIAttraction']          = self.getNumericalPermCategories(debug)
        self.permcatgetter['HEREPOIAttraction']     = self.getNumericalPermCategory
        self.featureMap['HEREPOIAttraction']        = self.getNumericalFeatures
        self.cats['HEREPOIAuto']              = self.getNumericalCategories(debug)
        self.catgetter['HEREPOIAuto']         = self.getNumericalCategory
        self.permcats['HEREPOIAuto']          = self.getNumericalPermCategories(debug)
        self.permcatgetter['HEREPOIAuto']     = self.getNumericalPermCategory
        self.featureMap['HEREPOIAuto']        = self.getNumericalFeatures
        self.cats['HEREPOIBuilding']              = self.getNumericalCategories(debug)
        self.catgetter['HEREPOIBuilding']         = self.getNumericalCategory
        self.permcats['HEREPOIBuilding']          = self.getNumericalPermCategories(debug)
        self.permcatgetter['HEREPOIBuilding']     = self.getNumericalPermCategory
        self.featureMap['HEREPOIBuilding']        = self.getNumericalFeatures
        self.cats['HEREPOICollege']              = self.getNumericalCategories(debug)
        self.catgetter['HEREPOICollege']         = self.getNumericalCategory
        self.permcats['HEREPOICollege']          = self.getNumericalPermCategories(debug)
        self.permcatgetter['HEREPOICollege']     = self.getNumericalPermCategory
        self.featureMap['HEREPOICollege']        = self.getNumericalFeatures
        self.cats['HEREPOICommercial']              = self.getNumericalCategories(debug)
        self.catgetter['HEREPOICommercial']         = self.getNumericalCategory
        self.permcats['HEREPOICommercial']          = self.getNumericalPermCategories(debug)
        self.permcatgetter['HEREPOICommercial']     = self.getNumericalPermCategory
        self.featureMap['HEREPOICommercial']        = self.getNumericalFeatures
        self.cats['HEREPOICycling']              = self.getNumericalCategories(debug)
        self.catgetter['HEREPOICycling']         = self.getNumericalCategory
        self.permcats['HEREPOICycling']          = self.getNumericalPermCategories(debug)
        self.permcatgetter['HEREPOICycling']     = self.getNumericalPermCategory
        self.featureMap['HEREPOICycling']        = self.getNumericalFeatures
        self.cats['HEREPOIEntertainment']              = self.getNumericalCategories(debug)
        self.catgetter['HEREPOIEntertainment']         = self.getNumericalCategory
        self.permcats['HEREPOIEntertainment']          = self.getNumericalPermCategories(debug)
        self.permcatgetter['HEREPOIEntertainment']     = self.getNumericalPermCategory
        self.featureMap['HEREPOIEntertainment']        = self.getNumericalFeatures
        self.cats['HEREPOIFastfood']              = self.getNumericalCategories(debug)
        self.catgetter['HEREPOIFastfood']         = self.getNumericalCategory
        self.permcats['HEREPOIFastfood']          = self.getNumericalPermCategories(debug)
        self.permcatgetter['HEREPOIFastfood']     = self.getNumericalPermCategory
        self.featureMap['HEREPOIFastfood']        = self.getNumericalFeatures
        self.cats['HEREPOIFuel']              = self.getNumericalCategories(debug)
        self.catgetter['HEREPOIFuel']         = self.getNumericalCategory
        self.permcats['HEREPOIFuel']          = self.getNumericalPermCategories(debug)
        self.permcatgetter['HEREPOIFuel']     = self.getNumericalPermCategory
        self.featureMap['HEREPOIFuel']        = self.getNumericalFeatures
        self.cats['HEREPOIGrocery']              = self.getNumericalCategories(debug)
        self.catgetter['HEREPOIGrocery']         = self.getNumericalCategory
        self.permcats['HEREPOIGrocery']          = self.getNumericalPermCategories(debug)
        self.permcatgetter['HEREPOIGrocery']     = self.getNumericalPermCategory
        self.featureMap['HEREPOIGrocery']        = self.getNumericalFeatures
        self.cats['HEREPOIIndustrial']              = self.getNumericalCategories(debug)
        self.catgetter['HEREPOIIndustrial']         = self.getNumericalCategory
        self.permcats['HEREPOIIndustrial']          = self.getNumericalPermCategories(debug)
        self.permcatgetter['HEREPOIIndustrial']     = self.getNumericalPermCategory
        self.featureMap['HEREPOIIndustrial']        = self.getNumericalFeatures
        self.cats['HEREPOILodging']              = self.getNumericalCategories(debug)
        self.catgetter['HEREPOILodging']         = self.getNumericalCategory
        self.permcats['HEREPOILodging']          = self.getNumericalPermCategories(debug)
        self.permcatgetter['HEREPOILodging']     = self.getNumericalPermCategory
        self.featureMap['HEREPOILodging']        = self.getNumericalFeatures
        self.cats['HEREPOIMedical']              = self.getNumericalCategories(debug)
        self.catgetter['HEREPOIMedical']         = self.getNumericalCategory
        self.permcats['HEREPOIMedical']          = self.getNumericalPermCategories(debug)
        self.permcatgetter['HEREPOIMedical']     = self.getNumericalPermCategory
        self.featureMap['HEREPOIMedical']        = self.getNumericalFeatures
        self.cats['HEREPOIMunicipal']              = self.getNumericalCategories(debug)
        self.catgetter['HEREPOIMunicipal']         = self.getNumericalCategory
        self.permcats['HEREPOIMunicipal']          = self.getNumericalPermCategories(debug)
        self.permcatgetter['HEREPOIMunicipal']     = self.getNumericalPermCategory
        self.featureMap['HEREPOIMunicipal']        = self.getNumericalFeatures
        self.cats['HEREPOIParking']              = self.getNumericalCategories(debug)
        self.catgetter['HEREPOIParking']         = self.getNumericalCategory
        self.permcats['HEREPOIParking']          = self.getNumericalPermCategories(debug)
        self.permcatgetter['HEREPOIParking']     = self.getNumericalPermCategory
        self.featureMap['HEREPOIParking']        = self.getNumericalFeatures
        self.cats['HEREPOIRecreation']              = self.getNumericalCategories(debug)
        self.catgetter['HEREPOIRecreation']         = self.getNumericalCategory
        self.permcats['HEREPOIRecreation']          = self.getNumericalPermCategories(debug)
        self.permcatgetter['HEREPOIRecreation']     = self.getNumericalPermCategory
        self.featureMap['HEREPOIRecreation']        = self.getNumericalFeatures
        self.cats['HEREPOIRestaurant']              = self.getNumericalCategories(debug)
        self.catgetter['HEREPOIRestaurant']         = self.getNumericalCategory
        self.permcats['HEREPOIRestaurant']          = self.getNumericalPermCategories(debug)
        self.permcatgetter['HEREPOIRestaurant']     = self.getNumericalPermCategory
        self.featureMap['HEREPOIRestaurant']        = self.getNumericalFeatures
        self.cats['HEREPOISchool']              = self.getNumericalCategories(debug)
        self.catgetter['HEREPOISchool']         = self.getNumericalCategory
        self.permcats['HEREPOISchool']          = self.getNumericalPermCategories(debug)
        self.permcatgetter['HEREPOISchool']     = self.getNumericalPermCategory
        self.featureMap['HEREPOISchool']        = self.getNumericalFeatures
        self.cats['HEREPOISport']              = self.getNumericalCategories(debug)
        self.catgetter['HEREPOISport']         = self.getNumericalCategory
        self.permcats['HEREPOISport']          = self.getNumericalPermCategories(debug)
        self.permcatgetter['HEREPOISport']     = self.getNumericalPermCategory
        self.featureMap['HEREPOISport']        = self.getNumericalFeatures
        self.cats['HEREPOITransit']              = self.getNumericalCategories(debug)
        self.catgetter['HEREPOITransit']         = self.getNumericalCategory
        self.permcats['HEREPOITransit']          = self.getNumericalPermCategories(debug)
        self.permcatgetter['HEREPOITransit']     = self.getNumericalPermCategory
        self.featureMap['HEREPOITransit']        = self.getNumericalFeatures
        self.cats['OSMAttraction']              = self.getNumericalCategories(debug)
        self.catgetter['OSMAttraction']         = self.getNumericalCategory
        self.permcats['OSMAttraction']          = self.getNumericalPermCategories(debug)
        self.permcatgetter['OSMAttraction']     = self.getNumericalPermCategory
        self.featureMap['OSMAttraction']        = self.getNumericalFeatures
        self.cats['OSMAuto']              = self.getNumericalCategories(debug)
        self.catgetter['OSMAuto']         = self.getNumericalCategory
        self.permcats['OSMAuto']          = self.getNumericalPermCategories(debug)
        self.permcatgetter['OSMAuto']     = self.getNumericalPermCategory
        self.featureMap['OSMAuto']        = self.getNumericalFeatures
        self.cats['OSMBuddhist']              = self.getNumericalCategories(debug)
        self.catgetter['OSMBuddhist']         = self.getNumericalCategory
        self.permcats['OSMBuddhist']          = self.getNumericalPermCategories(debug)
        self.permcatgetter['OSMBuddhist']     = self.getNumericalPermCategory
        self.featureMap['OSMBuddhist']        = self.getNumericalFeatures
        self.cats['OSMBuilding']              = self.getNumericalCategories(debug)
        self.catgetter['OSMBuilding']         = self.getNumericalCategory
        self.permcats['OSMBuilding']          = self.getNumericalPermCategories(debug)
        self.permcatgetter['OSMBuilding']     = self.getNumericalPermCategory
        self.featureMap['OSMBuilding']        = self.getNumericalFeatures
        self.cats['OSMBus']              = self.getNumericalCategories(debug)
        self.catgetter['OSMBus']         = self.getNumericalCategory
        self.permcats['OSMBus']          = self.getNumericalPermCategories(debug)
        self.permcatgetter['OSMBus']     = self.getNumericalPermCategory
        self.featureMap['OSMBus']        = self.getNumericalFeatures
        self.cats['OSMChristian']              = self.getNumericalCategories(debug)
        self.catgetter['OSMChristian']         = self.getNumericalCategory
        self.permcats['OSMChristian']          = self.getNumericalPermCategories(debug)
        self.permcatgetter['OSMChristian']     = self.getNumericalPermCategory
        self.featureMap['OSMChristian']        = self.getNumericalFeatures
        self.cats['OSMCollege']              = self.getNumericalCategories(debug)
        self.catgetter['OSMCollege']         = self.getNumericalCategory
        self.permcats['OSMCollege']          = self.getNumericalPermCategories(debug)
        self.permcatgetter['OSMCollege']     = self.getNumericalPermCategory
        self.featureMap['OSMCollege']        = self.getNumericalFeatures
        self.cats['OSMCommercial']              = self.getNumericalCategories(debug)
        self.catgetter['OSMCommercial']         = self.getNumericalCategory
        self.permcats['OSMCommercial']          = self.getNumericalPermCategories(debug)
        self.permcatgetter['OSMCommercial']     = self.getNumericalPermCategory
        self.featureMap['OSMCommercial']        = self.getNumericalFeatures
        self.cats['OSMEntertainment']              = self.getNumericalCategories(debug)
        self.catgetter['OSMEntertainment']         = self.getNumericalCategory
        self.permcats['OSMEntertainment']          = self.getNumericalPermCategories(debug)
        self.permcatgetter['OSMEntertainment']     = self.getNumericalPermCategory
        self.featureMap['OSMEntertainment']        = self.getNumericalFeatures
        self.cats['OSMFastfood']              = self.getNumericalCategories(debug)
        self.catgetter['OSMFastfood']         = self.getNumericalCategory
        self.permcats['OSMFastfood']          = self.getNumericalPermCategories(debug)
        self.permcatgetter['OSMFastfood']     = self.getNumericalPermCategory
        self.featureMap['OSMFastfood']        = self.getNumericalFeatures
        self.cats['OSMFerry']              = self.getNumericalCategories(debug)
        self.catgetter['OSMFerry']         = self.getNumericalCategory
        self.permcats['OSMFerry']          = self.getNumericalPermCategories(debug)
        self.permcatgetter['OSMFerry']     = self.getNumericalPermCategory
        self.featureMap['OSMFerry']        = self.getNumericalFeatures
        self.cats['OSMFuel']              = self.getNumericalCategories(debug)
        self.catgetter['OSMFuel']         = self.getNumericalCategory
        self.permcats['OSMFuel']          = self.getNumericalPermCategories(debug)
        self.permcatgetter['OSMFuel']     = self.getNumericalPermCategory
        self.featureMap['OSMFuel']        = self.getNumericalFeatures
        self.cats['OSMGrocery']              = self.getNumericalCategories(debug)
        self.catgetter['OSMGrocery']         = self.getNumericalCategory
        self.permcats['OSMGrocery']          = self.getNumericalPermCategories(debug)
        self.permcatgetter['OSMGrocery']     = self.getNumericalPermCategory
        self.featureMap['OSMGrocery']        = self.getNumericalFeatures
        self.cats['OSMHindu']              = self.getNumericalCategories(debug)
        self.catgetter['OSMHindu']         = self.getNumericalCategory
        self.permcats['OSMHindu']          = self.getNumericalPermCategories(debug)
        self.permcatgetter['OSMHindu']     = self.getNumericalPermCategory
        self.featureMap['OSMHindu']        = self.getNumericalFeatures
        self.cats['OSMIndustrial']              = self.getNumericalCategories(debug)
        self.catgetter['OSMIndustrial']         = self.getNumericalCategory
        self.permcats['OSMIndustrial']          = self.getNumericalPermCategories(debug)
        self.permcatgetter['OSMIndustrial']     = self.getNumericalPermCategory
        self.featureMap['OSMIndustrial']        = self.getNumericalFeatures
        self.cats['OSMJewish']              = self.getNumericalCategories(debug)
        self.catgetter['OSMJewish']         = self.getNumericalCategory
        self.permcats['OSMJewish']          = self.getNumericalPermCategories(debug)
        self.permcatgetter['OSMJewish']     = self.getNumericalPermCategory
        self.featureMap['OSMJewish']        = self.getNumericalFeatures
        self.cats['OSMLodging']              = self.getNumericalCategories(debug)
        self.catgetter['OSMLodging']         = self.getNumericalCategory
        self.permcats['OSMLodging']          = self.getNumericalPermCategories(debug)
        self.permcatgetter['OSMLodging']     = self.getNumericalPermCategory
        self.featureMap['OSMLodging']        = self.getNumericalFeatures
        self.cats['OSMMedical']              = self.getNumericalCategories(debug)
        self.catgetter['OSMMedical']         = self.getNumericalCategory
        self.permcats['OSMMedical']          = self.getNumericalPermCategories(debug)
        self.permcatgetter['OSMMedical']     = self.getNumericalPermCategory
        self.featureMap['OSMMedical']        = self.getNumericalFeatures
        self.cats['OSMMunicipal']              = self.getNumericalCategories(debug)
        self.catgetter['OSMMunicipal']         = self.getNumericalCategory
        self.permcats['OSMMunicipal']          = self.getNumericalPermCategories(debug)
        self.permcatgetter['OSMMunicipal']     = self.getNumericalPermCategory
        self.featureMap['OSMMunicipal']        = self.getNumericalFeatures
        self.cats['OSMMuslim']              = self.getNumericalCategories(debug)
        self.catgetter['OSMMuslim']         = self.getNumericalCategory
        self.permcats['OSMMuslim']          = self.getNumericalPermCategories(debug)
        self.permcatgetter['OSMMuslim']     = self.getNumericalPermCategory
        self.featureMap['OSMMuslim']        = self.getNumericalFeatures
        self.cats['OSMParking']              = self.getNumericalCategories(debug)
        self.catgetter['OSMParking']         = self.getNumericalCategory
        self.permcats['OSMParking']          = self.getNumericalPermCategories(debug)
        self.permcatgetter['OSMParking']     = self.getNumericalPermCategory
        self.featureMap['OSMParking']        = self.getNumericalFeatures
        self.cats['OSMPublic']              = self.getNumericalCategories(debug)
        self.catgetter['OSMPublic']         = self.getNumericalCategory
        self.permcats['OSMPublic']          = self.getNumericalPermCategories(debug)
        self.permcatgetter['OSMPublic']     = self.getNumericalPermCategory
        self.featureMap['OSMPublic']        = self.getNumericalFeatures
        self.cats['OSMRail']              = self.getNumericalCategories(debug)
        self.catgetter['OSMRail']         = self.getNumericalCategory
        self.permcats['OSMRail']          = self.getNumericalPermCategories(debug)
        self.permcatgetter['OSMRail']     = self.getNumericalPermCategory
        self.featureMap['OSMRail']        = self.getNumericalFeatures
        self.cats['OSMRecreation']              = self.getNumericalCategories(debug)
        self.catgetter['OSMRecreation']         = self.getNumericalCategory
        self.permcats['OSMRecreation']          = self.getNumericalPermCategories(debug)
        self.permcatgetter['OSMRecreation']     = self.getNumericalPermCategory
        self.featureMap['OSMRecreation']        = self.getNumericalFeatures
        self.cats['OSMReligious']              = self.getNumericalCategories(debug)
        self.catgetter['OSMReligious']         = self.getNumericalCategory
        self.permcats['OSMReligious']          = self.getNumericalPermCategories(debug)
        self.permcatgetter['OSMReligious']     = self.getNumericalPermCategory
        self.featureMap['OSMReligious']        = self.getNumericalFeatures
        self.cats['OSMRestaurant']              = self.getNumericalCategories(debug)
        self.catgetter['OSMRestaurant']         = self.getNumericalCategory
        self.permcats['OSMRestaurant']          = self.getNumericalPermCategories(debug)
        self.permcatgetter['OSMRestaurant']     = self.getNumericalPermCategory
        self.featureMap['OSMRestaurant']        = self.getNumericalFeatures
        self.cats['OSMSchool']              = self.getNumericalCategories(debug)
        self.catgetter['OSMSchool']         = self.getNumericalCategory
        self.permcats['OSMSchool']          = self.getNumericalPermCategories(debug)
        self.permcatgetter['OSMSchool']     = self.getNumericalPermCategory
        self.featureMap['OSMSchool']        = self.getNumericalFeatures
        self.cats['OSMSikh']              = self.getNumericalCategories(debug)
        self.catgetter['OSMSikh']         = self.getNumericalCategory
        self.permcats['OSMSikh']          = self.getNumericalPermCategories(debug)
        self.permcatgetter['OSMSikh']     = self.getNumericalPermCategory
        self.featureMap['OSMSikh']        = self.getNumericalFeatures
        self.cats['OSMSport']              = self.getNumericalCategories(debug)
        self.catgetter['OSMSport']         = self.getNumericalCategory
        self.permcats['OSMSport']          = self.getNumericalPermCategories(debug)
        self.permcatgetter['OSMSport']     = self.getNumericalPermCategory
        self.featureMap['OSMSport']        = self.getNumericalFeatures
        self.cats['OSMTaoist']              = self.getNumericalCategories(debug)
        self.catgetter['OSMTaoist']         = self.getNumericalCategory
        self.permcats['OSMTaoist']          = self.getNumericalPermCategories(debug)
        self.permcatgetter['OSMTaoist']     = self.getNumericalPermCategory
        self.featureMap['OSMTaoist']        = self.getNumericalFeatures
        self.cats['OSMTaxi']              = self.getNumericalCategories(debug)
        self.catgetter['OSMTaxi']         = self.getNumericalCategory
        self.permcats['OSMTaxi']          = self.getNumericalPermCategories(debug)
        self.permcatgetter['OSMTaxi']     = self.getNumericalPermCategory
        self.featureMap['OSMTaxi']        = self.getNumericalFeatures
        self.cats['OSMTram']              = self.getNumericalCategories(debug)
        self.catgetter['OSMTram']         = self.getNumericalCategory
        self.permcats['OSMTram']          = self.getNumericalPermCategories(debug)
        self.permcatgetter['OSMTram']     = self.getNumericalPermCategory
        self.featureMap['OSMTram']        = self.getNumericalFeatures
        self.cats['ROADSHighway']              = self.getNumericalCategories(debug)
        self.catgetter['ROADSHighway']         = self.getNumericalCategory
        self.permcats['ROADSHighway']          = self.getNumericalPermCategories(debug)
        self.permcatgetter['ROADSHighway']     = self.getNumericalPermCategory
        self.featureMap['ROADSHighway']        = self.getNumericalFeatures
        self.cats['ROADSInterstate']              = self.getNumericalCategories(debug)
        self.catgetter['ROADSInterstate']         = self.getNumericalCategory
        self.permcats['ROADSInterstate']          = self.getNumericalPermCategories(debug)
        self.permcatgetter['ROADSInterstate']     = self.getNumericalPermCategory
        self.featureMap['ROADSInterstate']        = self.getNumericalFeatures
        self.cats['ROADSMajorRd']              = self.getNumericalCategories(debug)
        self.catgetter['ROADSMajorRd']         = self.getNumericalCategory
        self.permcats['ROADSMajorRd']          = self.getNumericalPermCategories(debug)
        self.permcatgetter['ROADSMajorRd']     = self.getNumericalPermCategory
        self.featureMap['ROADSMajorRd']        = self.getNumericalFeatures
        self.cats['ROADSStaterte']              = self.getNumericalCategories(debug)
        self.catgetter['ROADSStaterte']         = self.getNumericalCategory
        self.permcats['ROADSStaterte']          = self.getNumericalPermCategories(debug)
        self.permcatgetter['ROADSStaterte']     = self.getNumericalPermCategory
        self.featureMap['ROADSStaterte']        = self.getNumericalFeatures
        self.cats['ROADSUsrte']              = self.getNumericalCategories(debug)
        self.catgetter['ROADSUsrte']         = self.getNumericalCategory
        self.permcats['ROADSUsrte']          = self.getNumericalPermCategories(debug)
        self.permcatgetter['ROADSUsrte']     = self.getNumericalPermCategory
        self.featureMap['ROADSUsrte']        = self.getNumericalFeatures
        self.cats['TerminalsAirport']              = self.getNumericalCategories(debug)
        self.catgetter['TerminalsAirport']         = self.getNumericalCategory
        self.permcats['TerminalsAirport']          = self.getNumericalPermCategories(debug)
        self.permcatgetter['TerminalsAirport']     = self.getNumericalPermCategory
        self.featureMap['TerminalsAirport']        = self.getNumericalFeatures
        self.cats['TerminalsAmtrak']              = self.getNumericalCategories(debug)
        self.catgetter['TerminalsAmtrak']         = self.getNumericalCategory
        self.permcats['TerminalsAmtrak']          = self.getNumericalPermCategories(debug)
        self.permcatgetter['TerminalsAmtrak']     = self.getNumericalPermCategory
        self.featureMap['TerminalsAmtrak']        = self.getNumericalFeatures        
        
        #self.multiFeatureMap = {}
        #self.multiFeatureMap["POI"] = getMultiFeaturesPOI
        
        
    def getFeatures(self, name, data, debug=False):
        f = self.featureMap.get(name)
        if f is None:
            retval = {}
            if isinstance(data, dict):
                retval['Name']  = data.get('Name')
                retval['Other'] = {}
                for k,v in data.items():
                    if k != 'Name':
                        retval['Other'][k] = v
            elif data is None:
                retval['Name'] = None
            elif isinstance(data, (int, str, float)):
                retval['Name'] = data
            elif isinstance(data, (tuple)):
                retval['Name'] = data
            elif isinstance(data, (list)):
                retval['Name'] = data
            else:
                #if debug:
                #    print("Not sure what to do with feature {0} with value {1}".format(name, data))
                retval['Name'] = None
                
            return retval
        else:
            return f(data, debug)
        
    def getFeatureTypes(self, name, debug=False):
        retval = self.catmap.get(name)
        if retval is None:
            return [name]
        return retval

    def getCategories(self, name, debug=False):
        if self.cats.get(name) is None:
            if debug is True:
                print("There is no list for category {0}".format(name))
            return None
        return self.cats[name]
    
    def getCategory(self, name, value, debug=False):
        if self.catgetter.get(name) is None:
            if debug is True:
                print("There is no getter for category {0}".format(name))
            return None
        return self.catgetter[name](value, debug)

    def getPermCategories(self, name, debug=False):
        if self.permcats.get(name) is None:
            if debug is True:
                print("There is no list for perm category {0}".format(name))
            return None
        return self.permcats[name]

    def getPermCategory(self, name, value, debug=False):
        if self.permcatgetter.get(name) is None:
            if debug is True:
                print("There is no getter for perm category {0}".format(name))
            return None
        return self.permcatgetter[name](value, debug)
    

        



    ##########################################################################################
    #
    # Permutations for Numerical Data
    #
    ##########################################################################################
    def getNumericalPermCategories(self, debug=False):
        import itertools
        vals=self.getNumericalCategories()
        categories  = [self.delim.join(x) for x in itertools.combinations(sorted(vals), 2)]
        categories += [self.delim.join([x, x]) for x in sorted(vals)]
        return categories
    def getNumericalPermCategory(self, vals, debug=False):
        category = self.delim.join(sorted([str(x) for x in vals]))
        return category
    
    def getNumericalCategories(self, debug=False):
        return ["Y", "N"]

    def getNumericalCategory(self, val, debug=False):
        if val > 0:
            return "Y"
        return "N"

    def getNumericalFeatures(self, numData, debug=False):
        numFeatures = {}
        if numData is None:
            numCategory   = None

        if isinstance(numData, (int,float)):
            numCategory = self.getNumericalCategory(numData)
        else:
            numCategory   = None

        numFeatures["Name"]         = numCategory
        if debug and False:
            print("  Found the following numerical features:")
            for k,v in numFeatures.items():
                print("\t",k,"\t",v)
        return numFeatures
    
    
        
    ##########################################################################################
    #
    # Categories
    #
    ##########################################################################################
    def getHomeRatioCategories(self, debug=False):
        return ["Low", "Mid", "High"]

    def getHomeRatioCategory(self, ratio, debug=False):
        if isinstance(ratio, (int, float)):
            if ratio > 5:
                return "High"
            elif ratio > 2:
                return "Mid"
            else:
                return "Low"
        else:
            return None
            




    ##########################################################################################
    #
    # State/Region Data Information
    #
    ##########################################################################################
    def getRegionCategories(self, debug=False):
        categories = []
        region   = "NORTHEAST"
        division = "New England"
        categories.append(" ".join(str(x) for x in [region,division]))
        region   = "NORTHEAST"
        division = "Middle Atlantic"
        categories.append(" ".join(str(x) for x in [region,division]))
        region   = "MIDWEST"
        division = "East North Central"
        categories.append(" ".join(str(x) for x in [region,division]))
        region   = "MIDWEST"
        division = "West North Central"
        categories.append(" ".join(str(x) for x in [region,division]))
        region   = "SOUTH"
        division = "South Atlantic"
        categories.append(" ".join(str(x) for x in [region,division]))
        region   = "SOUTH"
        division = "East South Central"
        categories.append(" ".join(str(x) for x in [region,division]))
        region   = "SOUTH"
        division = "West South Central"
        categories.append(" ".join(str(x) for x in [region,division]))
        region   = "WEST"
        division = "Mountain"
        categories.append(" ".join(str(x) for x in [region,division]))
        region   = "WEST"
        division = "Pacific"
        categories.append(" ".join(str(x) for x in [region,division]))
        region   = "OffTheGrid"
        division = "OffTheGrid"
        categories.append(" ".join(str(x) for x in [region,division]))
        categories = [x.replace(" ", "") for x in categories]
        return categories
    def getRegionCategory(self, state, debug=False):        
        category     = None
        if state in ["Connecticut", "Maine", "Massachusetts", "New Hampshire", "Rhode Island", "Vermont"]:
            region   = "NORTHEAST"
            division = "New England"
        elif state in ["New Jersey", "New York", "Pennsylvania"]:
            region   = "NORTHEAST"
            division = "Middle Atlantic"
        elif state in ["Illinois", "Indiana", "Michigan", "Ohio", "Wisconsin"]:
            region   = "MIDWEST"
            division = "East North Central"
        elif state in ["Iowa", "Kansas", "Minnesota", "Missouri", "Nebraska", "North Dakota", "South Dakota"]:
            region   = "MIDWEST"
            division = "West North Central"
        elif state in ["Delaware", "District of Columbia", "Florida", "Georgia", "Maryland", "North Carolina", "South Carolina", "Virginia", "West Virginia"]:
            region   = "SOUTH"
            division = "South Atlantic"
        elif state in ["Alabama", "Kentucky", "Mississippi", "Tennessee"]:
            region   = "SOUTH"
            division = "East South Central"
        elif state in ["Arkansas", "Louisiana", "Oklahoma", "Texas"]:
            region   = "SOUTH"
            division = "West South Central"
        elif state in ["Arizona", "Colorado", "Idaho", "Montana", "Nevada", "New Mexico", "Utah", "Wyoming"]:
            region   = "WEST"
            division = "Mountain"
        elif state in ["Alaska", "California", "Hawaii", "Oregon", "Washington"]:
            region   = "WEST"
            division = "Pacific"
        else:
            if debug:
                print("Could not find region/division for state {0}".format(state))
            region   = "OffTheGrid"
            division = "OffTheGrid"
        category = "".join(str(x) for x in [region,division])        
        category = category.replace(" ", "")
        return category, "High"

    def getStateFeatures(self, stateData, debug):
        stateFeatures = {}
        if stateData is None:
            stateName = None
            region    = None

        stateName    = None
        if isinstance(stateData, str):
            stateName    = stateData

        regionName, _ = self.getRegionCategory(stateName)

        stateFeatures["Name"]   = stateName
        stateFeatures["Region"] = regionName
        if debug and False:
            print("  Found the following state features:")
            for k,v in stateFeatures.items():
                print("\t",k,"\t",v)
        return stateFeatures



    ##########################################################################################
    #
    # Place Data Information
    #
    ##########################################################################################
    
    ###################################################
    # Place Pop
    ###################################################
    def getPlacePopPermCategories(self, debug=False):
        import itertools
        categories  = [self.delim.join(x) for x in itertools.combinations(sorted(self.getPlacePopCategories(debug)), 2)]
        categories += [self.delim.join([x, x]) for x in sorted(self.getPlacePopCategories(debug))]
        return categories
    def getPlacePopPermCategory(self, pops, debug=False):
        category = self.delim.join(sorted([str(x) for x in pops]))
        return category

    def getPlacePopCategories(self, debug=False):
        return ["RealSmall", "Small", "Mid", "Big", "RealBig"]
    def getPlacePopCategory(self, pop, debug=False):
        if pop is None:
            return "RealSmall"
        if pop < 1000:
            return "Small"
        elif pop < 15000:
            return "Mid"
        elif pop < 50000:
            return "Big"
        else:
            return "RealBig"
        
        
    ###################################################
    # Place Housing
    ###################################################
    def getPlaceHousingPermCategories(self, debug=False):
        import itertools
        categories  = [self.delim.join(x) for x in itertools.combinations(sorted(self.getPlaceHousingCategories(debug)), 2)]
        categories += [self.delim.join([x, x]) for x in sorted(self.getPlaceHousingCategories(debug))]
        return categories
    def getPlaceHousingPermCategory(self, housings, debug=False):
        category = self.delim.join(sorted([str(x) for x in housings]))
        return category

    def getPlaceHousingCategories(self, debug=False):
        return ["RealSmall", "Small", "Mid", "Big", "RealBig"]
    def getPlaceHousingCategory(self, housing, debug=False):
        if housing is None:
            return "RealSmall"
        if housing < 400:
            return "Small"
        elif housing < 5000:
            return "Mid"
        elif housing < 16000:
            return "Big"
        else:
            return "RealBig"
        
        
    ###################################################
    # Place Area
    ###################################################
    def getPlaceAreaPermCategories(self, debug=False):
        import itertools
        categories  = [self.delim.join(x) for x in itertools.combinations(sorted(self.getPlaceAreaCategories(debug)), 2)]
        categories += [self.delim.join([x, x]) for x in sorted(self.getPlaceAreaCategories(debug))]
        return categories
    def getPlaceAreaPermCategory(self, areas, debug=False):
        category = self.delim.join(sorted([str(x) for x in areas]))
        return category

    def getPlaceAreaCategories(self, debug=False):
        return ["RealSmall", "Small", "Mid", "Big", "RealBig"]
    def getPlaceAreaCategory(self, area, debug=False):        
        if area is None:
            return "RealSmall"
        if area   < 0.005:
            return "Small"
        elif area < 0.0035:
            return "Mid"
        elif area < 0.009:
            return "Big"
        else:
            return "RealBig"
        
        
    ###################################################
    # Place Type
    ###################################################
    def getPlaceTypeCategories(self, debug=False):
        return ['City', 'Borough', 'CDP', 'Village', 'Municipality', 'Town', 'Other']    
    def getPlaceTypeCategory(self, placetype, debug=False):
        if placetype in ['City', 'Borough', 'CDP', 'Village', 'Municipality', 'Town']:
            return placetype
        return "Other"

    def getPlaceTypePermCategories(self, debug=False):
        import itertools
        categories  = [self.delim.join(x) for x in itertools.combinations(sorted(self.getPlaceTypeCategories(debug)), 2)]
        categories += [self.delim.join([x, x]) for x in sorted(self.getPlaceTypeCategories(debug))]
        return categories
    def getPlaceTypePermCategory(self, placetypes, debug=False):
        category = self.delim.join(sorted([str(x) for x in placetypes]))
        return category

        
        
    ###################################################
    # Place Features
    ###################################################
    def getPlaceFeatures(self, placeData, debug):
        placeFeatures = {}
        if placeData is None:
            placeName         = None
            placePopCategory  = None
            placeAreaCategory = None
            placeHousingCategory = None

        if isinstance(placeData, dict):
            placeName    = placeData.get("Name")
            placeType    = placeData.get("Type")
            placePop     = placeData.get("Population")
            placeHousing = placeData.get("Housing")
            placeArea    = placeData.get("Area")
        else:
            placeName    = None
            placeType    = None
            placePop     = None
            placeArea    = None
            placeHousing = None

        if isinstance(placePop, list):
            if len(placePop) > 0:
                placeTotalPop = placePop[0]
            else:
                placeTotalPop = None
        else:
            placeTotalPop = None

        if isinstance(placeHousing, list):
            if len(placeHousing) > 0:
                placeTotalHousing = placeHousing[0]
            else:
                placeTotalHousing = None
        else:
            placeTotalHousing = None

        placeTypeCategory    = self.getPlaceTypeCategory(placeType)
        placePopCategory     = self.getPlacePopCategory(placeTotalPop)
        placeHousingCategory = self.getPlaceHousingCategory(placeTotalHousing)
        placeAreaCategory    = self.getPlaceAreaCategory(placeArea)

        placeFeatures["Name"]    = placeName
        placeFeatures["Type"]    = placeTypeCategory
        placeFeatures["Pop"]     = placePopCategory
        placeFeatures["Housing"] = placeHousingCategory
        placeFeatures["Area"]    = placeAreaCategory
        if debug and False:
            print("  Found the following place features:")
            for k,v in placeFeatures.items():
                print("\t",k,"\t",v)
        return placeFeatures



    ##########################################################################################
    #
    # MetDiv Data Information
    #
    ##########################################################################################
    
    ###################################################
    # MetDiv Pop
    ###################################################
    def getMetDivPopPermCategories(self, debug=False):
        import itertools
        categories  = [self.delim.join(x) for x in itertools.combinations(sorted(self.getMetDivPopCategories(debug)), 2)]
        categories += [self.delim.join([x, x]) for x in sorted(self.getMetDivPopCategories(debug))]
        return categories
    def getMetDivPopPermCategory(self, pops, debug=False):
        category = self.delim.join(sorted([str(x) for x in pops]))
        return category

    def getMetDivPopCategories(self, debug=False):
        return ["RealSmall", "Small", "Mid", "Big", "RealBig"]
    def getMetDivPopCategory(self, pop, debug=False):
        if pop is None:
            return "RealSmall"
        if pop   < 2000000:
            return "Small"
        elif pop < 5000000:
            return "Mid"
        elif pop < 10000000:
            return "Big"
        else:
            return "RealBig"
        
        
    ###################################################
    # MetDiv Housing
    ###################################################
    def getMetDivHousingPermCategories(self, debug=False):
        import itertools
        categories  = [self.delim.join(x) for x in itertools.combinations(sorted(self.getMetDivHousingCategories(debug)), 2)]
        categories += [self.delim.join([x, x]) for x in sorted(self.getMetDivHousingCategories(debug))]
        return categories
    def getMetDivHousingPermCategory(self, housings, debug=False):
        category = self.delim.join(sorted([str(x) for x in housings]))
        return category

    def getMetDivHousingCategories(self, debug=False):
        return ["RealSmall", "Small", "Mid", "Big", "RealBig"]
    def getMetDivHousingCategory(self, housing, debug=False):
        if housing is None:
            return "RealSmall"
        if housing   < 750000:
            return "Small"
        elif housing < 1800000:
            return "Mid"
        elif housing < 3400000:
            return "Big"
        else:
            return "RealBig"
        
        
    ###################################################
    # MetDiv Area
    ###################################################
    def getMetDivAreaPermCategories(self, debug=False):
        import itertools
        categories  = [self.delim.join(x) for x in itertools.combinations(sorted(self.getMetDivAreaCategories(debug)), 2)]
        categories += [self.delim.join([x, x]) for x in sorted(self.getMetDivAreaCategories(debug))]
        return categories
    def getMetDivAreaPermCategory(self, areas, debug=False):
        category = self.delim.join(sorted([str(x) for x in areas]))
        return category

    def getMetDivAreaCategories(self, debug=False):
        return ["RealSmall", "Small", "Mid", "Big", "RealBig"]
    def getMetDivAreaCategory(self, area, debug=False):  
        if area is None:
            return "RealSmall"
        if area   < 0.55:
            return "Small"
        elif area < 1.3:
            return "Mid"
        elif area < 1.45:
            return "Big"
        else:
            return "RealBig"
        
        
    ###################################################
    # MetDiv Type
    ###################################################
    def getMetDivTypeCategories(self, debug=False):
        return ['Metro', 'Other']    
    def getMetDivTypeCategory(self, placetype, debug=False):
        if placetype in ['Metro']:
            return placetype
        return "Other"

    def getMetDivTypePermCategories(self, debug=False):
        import itertools
        categories  = [self.delim.join(x) for x in itertools.combinations(sorted(self.getMetDivTypeCategories(debug)), 2)]
        categories += [self.delim.join([x, x]) for x in sorted(self.getMetDivTypeCategories(debug))]
        return categories
    def getMetDivTypePermCategory(self, metdivtypes, debug=False):
        category = self.delim.join(sorted([str(x) for x in metdivtypes]))
        return category

        
        
    ###################################################
    # MetDiv Features
    ###################################################
    def getMetDivFeatures(self, metdivData, debug):
        metdivFeatures = {}
        if metdivData is None:
            metdivName         = None
            metdivPopCategory  = None
            metdivAreaCategory = None
            metdivHousingCategory = None

        if isinstance(metdivData, dict):
            metdivName    = metdivData.get("Name")
            metdivType    = metdivData.get("Type")
            metdivPop     = metdivData.get("Population")
            metdivHousing = metdivData.get("Housing")
            metdivArea    = metdivData.get("Area")
        else:
            metdivName    = None
            metdivType    = None
            metdivPop     = None
            metdivArea    = None
            metdivHousing = None

        if isinstance(metdivPop, list):
            if len(metdivPop) > 0:
                metdivTotalPop = metdivPop[0]
            else:
                metdivTotalPop = None
        else:
            metdivTotalPop = None

        if isinstance(metdivHousing, list):
            if len(metdivHousing) > 0:
                metdivTotalHousing = metdivHousing[0]
            else:
                metdivTotalHousing = None
        else:
            metdivTotalHousing = None

        metdivTypeCategory    = self.getMetDivTypeCategory(metdivType)
        metdivPopCategory     = self.getMetDivPopCategory(metdivTotalPop)
        metdivHousingCategory = self.getMetDivHousingCategory(metdivTotalHousing)
        metdivAreaCategory    = self.getMetDivAreaCategory(metdivArea)

        metdivFeatures["Name"]    = metdivName
        metdivFeatures["Type"]    = metdivTypeCategory
        metdivFeatures["Pop"]     = metdivPopCategory
        metdivFeatures["Housing"] = metdivHousingCategory
        metdivFeatures["Area"]    = metdivAreaCategory
        if debug and False:
            print("  Found the following metdiv features:")
            for k,v in metdivFeatures.items():
                print("\t",k,"\t",v)
        return metdivFeatures



    ##########################################################################################
    #
    # CBSA Data Information
    #
    ##########################################################################################
    
    ###################################################
    # CBSA Pop
    ###################################################
    def getCBSAPopPermCategories(self, debug=False):
        import itertools
        categories  = [self.delim.join(x) for x in itertools.combinations(sorted(self.getCBSAPopCategories(debug)), 2)]
        categories += [self.delim.join([x, x]) for x in sorted(self.getCBSAPopCategories(debug))]
        return categories
    def getCBSAPopPermCategory(self, pops, debug=False):
        category = self.delim.join(sorted([str(x) for x in pops]))
        return category

    def getCBSAPopCategories(self, debug=False):
        return ["RealSmall", "Small", "Mid", "Big", "RealBig"]
    def getCBSAPopCategory(self, pop, debug=False):
        if pop is None:
            return "RealSmall"
        if pop   < 75000:
            return "Small"
        elif pop < 500000:
            return "Mid"
        elif pop < 2000000:
            return "Big"
        else:
            return "RealBig"

        
    ###################################################
    # CBSA Housing
    ###################################################
    def getCBSAHousingPermCategories(self, debug=False):
        import itertools
        categories  = [self.delim.join(x) for x in itertools.combinations(sorted(self.getCBSAHousingCategories(debug)), 2)]
        categories += [self.delim.join([x, x]) for x in sorted(self.getCBSAHousingCategories(debug))]
        return categories
    def getCBSAHousingPermCategory(self, housings, debug=False):
        category = self.delim.join(sorted([str(x) for x in housings]))
        return category

    def getCBSAHousingCategories(self, debug=False):
        return ["RealSmall", "Small", "Mid", "Big", "RealBig"]
    def getCBSAHousingCategory(self, housing, debug=False):
        if housing is None:
            return "RealSmall"
        if housing   < 30000:
            return "Small"
        elif housing < 200000:
            return "Mid"
        elif housing < 750000:
            return "Big"
        else:
            return "RealBig"
        

    ###################################################
    # CBSA Area
    ###################################################
    def getCBSAAreaPermCategories(self, debug=False):
        import itertools
        categories  = [self.delim.join(x) for x in itertools.combinations(sorted(self.getCBSAAreaCategories(debug)), 2)]
        categories += [self.delim.join([x, x]) for x in sorted(self.getCBSAAreaCategories(debug))]
        return categories
    def getCBSAAreaPermCategory(self, areas, debug=False):
        category = self.delim.join(sorted([str(x) for x in areas]))
        return category

    def getCBSAAreaCategories(self, debug=False):
        return ["RealSmall", "Small", "Mid", "Big", "RealBig"]
    def getCBSAAreaCategory(self, area, debug=False):  
        if area is None:
            return "RealSmall"
        if area   < 0.26:
            return "Small"
        elif area < 1.1:
            return "Mid"
        elif area < 2.1:
            return "Big"
        else:
            return "RealBig"
        
        
    ###################################################
    # CBSA Type
    ###################################################
    def getCBSATypeCategories(self, debug=False):
        return ['Metro', 'Micro', 'Other']    
    def getCBSATypeCategory(self, placetype, debug=False):
        if placetype in ['Metro', 'Micro']:
            return placetype
        return "Other"

    def getCBSATypePermCategories(self, debug=False):
        import itertools
        categories  = [self.delim.join(x) for x in itertools.combinations(sorted(self.getCBSATypeCategories(debug)), 2)]
        categories += [self.delim.join([x, x]) for x in sorted(self.getCBSATypeCategories(debug))]
        return categories
    def getCBSATypePermCategory(self, cbsatypes, debug=False):
        category = self.delim.join(sorted([str(x) for x in cbsatypes]))
        return category

        
        
    ###################################################
    # CBSA Features
    ###################################################
    def getCBSAFeatures(self, cbsaData, debug):
        cbsaFeatures = {}
        if cbsaData is None:
            cbsaName         = None
            cbsaPopCategory  = None
            cbsaAreaCategory = None
            cbsaHousingCategory = None

        if isinstance(cbsaData, dict):
            cbsaName    = cbsaData.get("Name")
            cbsaType    = cbsaData.get("Type")
            cbsaPop     = cbsaData.get("Population")
            cbsaHousing = cbsaData.get("Housing")
            cbsaArea    = cbsaData.get("Area")
        else:
            cbsaName    = None
            cbsaType    = None
            cbsaPop     = None
            cbsaArea    = None
            cbsaHousing = None

        if isinstance(cbsaPop, list):
            if len(cbsaPop) > 0:
                cbsaTotalPop = cbsaPop[0]
            else:
                cbsaTotalPop = None
        else:
            cbsaTotalPop = None

        if isinstance(cbsaHousing, list):
            if len(cbsaHousing) > 0:
                cbsaTotalHousing = cbsaHousing[0]
            else:
                cbsaTotalHousing = None
        else:
            cbsaTotalHousing = None

        cbsaTypeCategory    = self.getCBSATypeCategory(cbsaType)
        cbsaPopCategory     = self.getCBSAPopCategory(cbsaTotalPop)
        cbsaHousingCategory = self.getCBSAHousingCategory(cbsaTotalHousing)
        cbsaAreaCategory    = self.getCBSAAreaCategory(cbsaArea)

        cbsaFeatures["Name"]    = cbsaName
        cbsaFeatures["Type"]    = cbsaTypeCategory
        cbsaFeatures["Pop"]     = cbsaPopCategory
        cbsaFeatures["Housing"] = cbsaHousingCategory
        cbsaFeatures["Area"]    = cbsaAreaCategory
        
        if debug and False:
            print("  Found the following cbsa features:")
            for k,v in cbsaFeatures.items():
                print("\t",k,"\t",v)
        return cbsaFeatures



    ##########################################################################################
    #
    # CSA Data Information
    #
    ##########################################################################################
    
    ###################################################
    # CSA Pop
    ###################################################
    def getCSAPopPermCategories(self, debug=False):
        import itertools
        categories  = [self.delim.join(x) for x in itertools.combinations(sorted(self.getCSAPopCategories(debug)), 2)]
        categories += [self.delim.join([x, x]) for x in sorted(self.getCSAPopCategories(debug))]
        return categories
    def getCSAPopPermCategory(self, pops, debug=False):
        category = self.delim.join(sorted([str(x) for x in pops]))
        return category

    def getCSAPopCategories(self, debug=False):
        return ["RealSmall", "Small", "Mid", "Big", "RealBig"]
    def getCSAPopCategory(self, pop, debug=False):
        if pop is None:
            return "RealSmall"
        if pop   < 570000:
            return "Small"
        elif pop < 3300000:
            return "Mid"
        elif pop < 7800000:
            return "Big"
        else:
            return "RealBig"


    ###################################################
    # CSA Housing
    ###################################################
    def getCSAHousingPermCategories(self, debug=False):
        import itertools
        categories  = [self.delim.join(x) for x in itertools.combinations(sorted(self.getCSAHousingCategories(debug)), 2)]
        categories += [self.delim.join([x, x]) for x in sorted(self.getCSAHousingCategories(debug))]
        return categories
    def getCSAHousingPermCategory(self, housings, debug=False):
        category = self.delim.join(sorted([str(x) for x in housings]))
        return category

    def getCSAHousingCategories(self, debug=False):
        return ["RealSmall", "Small", "Mid", "Big", "RealBig"]
    def getCSAHousingCategory(self, housing, debug=False):
        if housing is None:
            return "RealSmall"
        if housing   < 230000:
            return "Small"
        elif housing < 1280000:
            return "Mid"
        elif housing < 3000000:
            return "Big"
        else:
            return "RealBig"


    ###################################################
    # CSA Area
    ###################################################
    def getCSAAreaPermCategories(self, debug=False):
        import itertools
        categories  = [self.delim.join(x) for x in itertools.combinations(sorted(self.getCSAAreaCategories(debug)), 2)]
        categories += [self.delim.join([x, x]) for x in sorted(self.getCSAAreaCategories(debug))]
        return categories
    def getCSAAreaPermCategory(self, areas, debug=False):
        category = self.delim.join(sorted([str(x) for x in areas]))
        return category

    def getCSAAreaCategories(self, debug=False):
        return ["RealSmall", "Small", "Mid", "Big", "RealBig"]
    def getCSAAreaCategory(self, area, debug=False):  
        if area is None:
            return "RealSmall"
        if area   < 0.9:
            return "Small"
        elif area < 2.6:
            return "Mid"
        elif area < 3.75:
            return "Big"
        else:
            return "RealBig"

        
    ###################################################
    # CSA Type
    ###################################################
    def getCSATypeCategories(self, debug=False):
        return ['CSA']    
    def getCSATypeCategory(self, csatype, debug=False):
        return "CSA"

    def getCSATypePermCategories(self, debug=False):
        import itertools
        categories  = [self.delim.join(x) for x in itertools.combinations(sorted(self.getCSATypeCategories(debug)), 2)]
        categories += [self.delim.join([x, x]) for x in sorted(self.getCSATypeCategories(debug))]
        return categories
    def getCSATypePermCategory(self, csatypes, debug=False):
        category = self.delim.join(sorted([str(x) for x in csatypes]))
        return category

        
        
    ###################################################
    # CSA Features
    ###################################################
    def getCSAFeatures(self, csaData, debug):
        csaFeatures = {}
        if csaData is None:
            csaName         = None
            csaPopCategory  = None
            csaAreaCategory = None
            csaHousingCategory = None

        if isinstance(csaData, dict):
            csaName    = csaData.get("Name")
            csaType    = csaData.get("Type")
            csaPop     = csaData.get("Population")
            csaHousing = csaData.get("Housing")
            csaArea    = csaData.get("Area")
        else:
            csaName    = None
            csaType    = None
            csaPop     = None
            csaArea    = None
            csaHousing = None

        if isinstance(csaPop, list):
            if len(csaPop) > 0:
                csaTotalPop = csaPop[0]
            else:
                csaTotalPop = None
        else:
            csaTotalPop = None

        if isinstance(csaHousing, list):
            if len(csaHousing) > 0:
                csaTotalHousing = csaHousing[0]
            else:
                csaTotalHousing = None
        else:
            csaTotalHousing = None

        csaTypeCategory    = self.getCSATypeCategory(csaType)
        csaPopCategory     = self.getCSAPopCategory(csaTotalPop)
        csaHousingCategory = self.getCSAHousingCategory(csaTotalHousing)
        csaAreaCategory    = self.getCSAAreaCategory(csaArea)

        csaFeatures["Name"]    = csaName
        csaFeatures["Type"]    = csaTypeCategory
        csaFeatures["Pop"]     = csaPopCategory
        csaFeatures["Housing"] = csaHousingCategory
        csaFeatures["Area"]    = csaAreaCategory
        if debug and False:
            print("  Found the following csa features:")
            for k,v in csaFeatures.items():
                print("\t",k,"\t",v)
        return csaFeatures



    ##########################################################################################
    #
    # County Data Information
    #
    ##########################################################################################
    
    ###################################################
    # County Pop
    ###################################################
    def getCountyPopPermCategories(self, debug=False):
        import itertools
        categories  = [self.delim.join(x) for x in itertools.combinations(sorted(self.getCountyPopCategories(debug)), 2)]
        categories += [self.delim.join([x, x]) for x in sorted(self.getCountyPopCategories(debug))]
        return categories
    def getCountyPopPermCategory(self, pops, debug=False):
        category = self.delim.join(sorted([str(x) for x in pops]))
        return category

    def getCountyPopCategories(self, debug=False):
        return ["RealSmall", "Small", "Mid", "Big", "RealBig"]
    def getCountyPopCategory(self, pop, debug=False):
        if pop is None:
            return "RealSmall"
        if pop   < 25000:
            return "Small"
        elif pop < 200000:
            return "Mid"
        elif pop < 625000:
            return "Big"
        else:
            return "RealBig"


    ###################################################
    # County Housing
    ###################################################
    def getCountyHousingPermCategories(self, debug=False):
        import itertools
        categories  = [self.delim.join(x) for x in itertools.combinations(sorted(self.getCountyHousingCategories(debug)), 2)]
        categories += [self.delim.join([x, x]) for x in sorted(self.getCountyHousingCategories(debug))]
        return categories
    def getCountyHousingPermCategory(self, housings, debug=False):
        category = self.delim.join(sorted([str(x) for x in housings]))
        return category

    def getCountyHousingCategories(self, debug=False):
        return ["RealSmall", "Small", "Mid", "Big", "RealBig"]
    def getCountyHousingCategory(self, housing, debug=False):
        if housing is None:
            return "RealSmall"
        if housing   < 10000:
            return "Small"
        elif housing < 75000:
            return "Mid"
        elif housing < 240000:
            return "Big"
        else:
            return "RealBig"


    ###################################################
    # County Area
    ###################################################
    def getCountyAreaPermCategories(self, debug=False):
        import itertools
        categories  = [self.delim.join(x) for x in itertools.combinations(sorted(self.getCountyAreaCategories(debug)), 2)]
        categories += [self.delim.join([x, x]) for x in sorted(self.getCountyAreaCategories(debug))]
        return categories
    def getCountyAreaPermCategory(self, areas, debug=False):
        category = self.delim.join(sorted([str(x) for x in areas]))
        return category

    def getCountyAreaCategories(self, debug=False):
        return ["RealSmall", "Small", "Mid", "Big", "RealBig"]
    def getCountyAreaCategory(self, area, debug=False):  
        if area is None:
            return "RealSmall"
        if area   < 0.17:
            return "Small"
        elif area < 0.56:
            return "Mid"
        elif area < 1.3:
            return "Big"
        else:
            return "RealBig"

        
    ###################################################
    # County Type
    ###################################################
    def getCountyTypeCategories(self, debug=False):
        return ['A', 'S', 'F', 'N', 'C', 'B', 'G', 'Other']    
    def getCountyTypeCategory(self, countytype, debug=False):
        if countytype in ['A', 'S', 'F', 'N', 'C', 'B', 'G']:
            return countytype
        else:
            return "Other"

    def getCountyTypePermCategories(self, debug=False):
        import itertools
        categories  = [self.delim.join(x) for x in itertools.combinations(sorted(self.getCountyTypeCategories(debug)), 2)]
        categories += [self.delim.join([x, x]) for x in sorted(self.getCountyTypeCategories(debug))]
        return categories
    def getCountyTypePermCategory(self, countytypes, debug=False):
        category = self.delim.join(sorted([str(x) for x in countytypes]))
        return category

        
        
    ###################################################
    # County Features
    ###################################################
    def getCountyFeatures(self, countyData, debug):
        countyFeatures = {}
        if countyData is None:
            countyName         = None
            countyPopCategory  = None
            countyAreaCategory = None
            countyHousingCategory = None

        if isinstance(countyData, dict):
            countyName    = countyData.get("Name")
            countyType    = countyData.get("Type")
            countyPop     = countyData.get("Population")
            countyHousing = countyData.get("Housing")
            countyArea    = countyData.get("Area")
        else:
            countyName    = None
            countyType    = None
            countyPop     = None
            countyArea    = None
            countyHousing = None

        if isinstance(countyPop, list):
            if len(countyPop) > 0:
                countyTotalPop = countyPop[0]
            else:
                countyTotalPop = None
        else:
            countyTotalPop = None

        if isinstance(countyHousing, list):
            if len(countyHousing) > 0:
                countyTotalHousing = countyHousing[0]
            else:
                countyTotalHousing = None
        else:
            countyTotalHousing = None

        countyTypeCategory    = self.getCountyTypeCategory(countyType)
        countyPopCategory     = self.getCountyPopCategory(countyTotalPop)
        countyHousingCategory = self.getCountyHousingCategory(countyTotalHousing)
        countyAreaCategory    = self.getCountyAreaCategory(countyArea)

        countyFeatures["Name"]    = countyName
        countyFeatures["Type"]    = countyTypeCategory
        countyFeatures["Pop"]     = countyPopCategory
        countyFeatures["Housing"] = countyHousingCategory
        countyFeatures["Area"]    = countyAreaCategory
        if debug and False:
            print("  Found the following county features:")
            for k,v in countyFeatures.items():
                print("\t",k,"\t",v)
        return countyFeatures






    ##########################################################################################
    #
    # zip Data Information
    #
    ##########################################################################################        
    def getZipFeatures(self, zipData, debug):
        zipFeatures = {}
        if zipData is None:
            zipName        = None

        if isinstance(zipData, dict):
            zipName    = zipData.get("Name")
        else:
            zipName    = None

        zipFeatures["Name"] = str(zipName)
        if debug and False:
            print("  Found the following Zip features:")
            for k,v in zipFeatures.items():
                print("\t",k,"\t",v)
        return zipFeatures



    ##########################################################################################
    #
    # Airport Data Information
    #
    ##########################################################################################        
    def getAirportFeatures(self, airportData, debug):
        airportFeatures = {}
        if airportData is None:
            airportName        = None

        if isinstance(airportData, str):
            airportName    = airportData
        else:
            airportName    = None

        airportFeatures["Name"] = str(airportName)
        if debug and False:
            print("  Found the following Airport features:")
            for k,v in airportFeatures.items():
                print("\t",k,"\t",v)
        return airportFeatures



    ##########################################################################################
    #
    # Venue Data Information
    #
    ##########################################################################################        
    def getVenueFeatures(self, venueData, debug):
        venueFeatures = {}
        if venueData is None:
            venueName        = None

        if isinstance(venueData, str):
            venueName    = venueData
        else:
            venueName    = None

        venueFeatures["Name"] = str(venueName)
        if debug and False:
            print("  Found the following Venue features:")
            for k,v in venueFeatures.items():
                print("\t",k,"\t",v)
        return venueFeatures



    ##########################################################################################
    #
    # amtrak Data Information
    #
    ##########################################################################################        
    def getAmtrakFeatures(self, amtrakData, debug):
        amtrakFeatures = {}
        if amtrakData is None:
            amtrakName        = None

        if isinstance(amtrakData, str):
            amtrakName    = amtrakData
        else:
            amtrakName    = None

        amtrakFeatures["Name"] = str(amtrakName)
        if debug and False:
            print("  Found the following Amtrak features:")
            for k,v in amtrakFeatures.items():
                print("\t",k,"\t",v)
        return amtrakFeatures



    ##########################################################################################
    #
    # station Data Information
    #
    ##########################################################################################        
    def getStationFeatures(self, stationData, debug):
        stationFeatures = {}
        if stationData is None:
            stationName        = None

        if isinstance(stationData, str):
            stationName    = stationData
        else:
            stationName    = None

        stationFeatures["Name"] = str(stationName)
        if debug and False:
            print("  Found the following Station features:")
            for k,v in stationFeatures.items():
                print("\t",k,"\t",v)
        return stationFeatures



    ##########################################################################################
    #
    # Interstate Data Information
    #
    ##########################################################################################        
    def getInterstateFeatures(self, interstateData, debug):
        interstateFeatures = {}
        if interstateData is None:
            interstateName        = None

        if isinstance(interstateData, str):
            interstateName    = interstateData
        else:
            interstateName    = None

        interstateFeatures["Name"] = str(interstateName)
        if debug and False:
            print("  Found the following interstate features:")
            for k,v in interstateFeatures.items():
                print("\t",k,"\t",v)
        return interstateFeatures



    ##########################################################################################
    #
    # usrte Data Information
    #
    ##########################################################################################        
    def getUSRteFeatures(self, usrteData, debug):
        usrteFeatures = {}
        if usrteData is None:
            usrteName        = None

        if isinstance(usrteData, str):
            usrteName    = usrteData
        else:
            usrteName    = None

        usrteFeatures["Name"] = str(usrteName)
        if debug and False:
            print("  Found the following USRte features:")
            for k,v in usrteFeatures.items():
                print("\t",k,"\t",v)
        return usrteFeatures



    ##########################################################################################
    #
    # localRd Data Information
    #
    ##########################################################################################        
    def getLocalRdFeatures(self, localRdData, debug):
        localRdFeatures = {}
        if localRdData is None:
            localRdName        = None

        if isinstance(localRdData, str):
            localRdName    = localRdData
        else:
            localRdName    = None

        localRdFeatures["Name"] = str(localRdName)
        if debug and False:
            print("  Found the following localRd features:")
            for k,v in localRdFeatures.items():
                print("\t",k,"\t",v)
        return localRdFeatures



    ##########################################################################################
    #
    # staterte Data Information
    #
    ##########################################################################################        
    def getStateRteFeatures(self, staterteData, debug):
        staterteFeatures = {}
        if staterteData is None:
            staterteName        = None

        if isinstance(staterteData, str):
            staterteName    = staterteData
        else:
            staterteName    = None

        staterteFeatures["Name"] = str(staterteName)
        if debug and False:
            print("  Found the following StateRte features:")
            for k,v in staterteFeatures.items():
                print("\t",k,"\t",v)
        return staterteFeatures



    ##########################################################################################
    #
    # POI Data Information
    #
    ##########################################################################################
    def getPOIPermCategories(self, debug=False):
        import itertools
        categories  = [self.delim.join(x) for x in itertools.combinations(sorted(self.getPOICategories(debug)), 2)]
        categories += [self.delim.join([x, x]) for x in sorted(self.getPOICategories(debug))]
        return categories
    def getPOIPermCategory(self, pois, debug=False):
        category = self.delim.join(sorted([str(x) for x in pois]))
        return category

    def getPOICategories(self, debug=False):
        return ["Normal", "VeryLow", "Low", "Mid", "High", "VeryHigh"]
    def getPOICategory(self, poi, debug=False):
        significance = "High"
        avg = poi
        
        category = "Normal"
        if avg >= 500:
            category="VeryHigh"
        elif avg >= 200:
            category="High"
        elif avg >= 50:
            category="Mid"
        elif avg >= 25:
            category="Low"
        elif avg >= 10:
            category="VeryLow"

        return category, significance    

    def getPOIFeatures(self, poiData, debug):
        poiFeatures = {}
        if poiData is None:
            poiName        = None

        if isinstance(poiData, (float, int)):
            poiName, _  = self.getPOICategory(poiData)
        else:
            poiName     = None

        poiFeatures["Name"] = poiName
        if debug and False:
            print("  Found the following POI features:")
            for k,v in poiFeatures.items():
                print("\t",k,"\t",v)
        return poiFeatures




    ##########################################################################################
    #
    # DwellTime Data Information
    #
    ##########################################################################################
    def getDwellTimePermCategories(self, debug=False):
        import itertools
        categories  = [self.delim.join(x) for x in itertools.combinations(sorted(self.getDwellTimeCategories(debug)), 2)]
        categories += [self.delim.join([x, x]) for x in sorted(self.getDwellTimeCategories(debug))]
        return categories
    def getDwellTimePermCategory(self, dwell, debug=False):
        category = self.delim.join(sorted([str(x) for x in dwell]))
        return category

    def getDwellTimeCategories(self, debug=False):
        return ["VeryHigh", "High", "Mid", "Low", "VeryLow"]
    def getDwellTimeCategory(self, dwell, debug=False):
        try:
            avg = dwell['Avg']
            std = dwell['Std']
        except:
            print("Could not get dwell time information from {0}".format(dwell))

        category     = None
        significance = None
        if avg >= 6:
            category="VeryHigh"
        elif avg >= 2:
            category="High"
        elif avg >= 0.5:
            category="Mid"
        elif avg >= 0.1:
            category="Low"
        else:
            category="VeryLow"

        if std is not None:
            if std > 0:
                sig = avg/std
                if sig < 1:
                    significance = "Low"
                elif sig > 3:
                    significance = "High"
                else:
                    significance = "Mid"
            else:
                significance = "High"

        return category, significance      

    def getDwellTimeFeatures(self, dwelltimeData, debug):
        dwelltimeFeatures = {}
        if dwelltimeData is None:
            dwellCategory   = None
            dwellSignifance = None

        if isinstance(dwelltimeData, dict):
            dwellCategory, dwellSignifance = self.getDwellTimeCategory(dwelltimeData, debug)
        elif isinstance(dwelltimeData, float):
            dwellCategory, dwellSignifance = self.getDwellTimeCategory({"Avg": dwelltimeData, "Std": None}, debug)
            
        else:
            dwellCategory   = None
            dwellSignifance = None

        dwelltimeFeatures["Name"]         = dwellCategory
        dwelltimeFeatures["Significance"] = dwellSignifance
        if debug and False:
            print("  Found the following dwelltime features:")
            for k,v in dwelltimeFeatures.items():
                print("\t",k,"\t",v)
        return dwelltimeFeatures




    ##########################################################################################
    #
    # Duration Data Information
    #
    ##########################################################################################
    def getDurationCategories(self, debug=False):
        return ["VeryHigh", "High", "Mid", "Low", "VeryLow"]
    def getDurationCategory(self, duration, debug=False):
        try:
            avg = duration['Avg']
            std = duration['Std']
        except:
            print("Could not get duration information from {0}".format(duration))

        category     = None
        significance = None
        if avg >= 4:
            category="VeryHigh"
        if avg >= 2:
            category="High"
        elif avg >= 0.5:
            category="Mid"
        elif avg >= 0.1:
            category="Low"
        else:
            category="VeryLow"

        if std is not None:
            if std > 0:
                sig = avg/std
                if sig < 1:
                    significance = "Low"
                elif sig > 3:
                    significance = "High"
                else:
                    significance = "Mid"
            else:
                significance = "High"

        return category, significance  

    def getDurationFeatures(self, durationData, debug):
        durationFeatures = {}
        if durationData is None:
            durationCategory   = None
            durationSignifance = None

        if isinstance(durationData, dict):
            durationCategory, durationSignifance = self.getDurationCategory(durationData, debug)
        elif isinstance(durationData, float):
            durationCategory, durationSignifance = self.getDurationCategory({"Avg": durationData, "Std": None}, debug)
        else:
            durationCategory   = None
            durationSignifance = None

        durationFeatures["Name"]         = durationCategory
        durationFeatures["Significance"] = durationSignifance
        if debug and False:
            print("  Found the following duration features:")
            for k,v in durationFeatures.items():
                print("\t",k,"\t",v)
        return durationFeatures







    ##########################################################################################
    #
    # Distance Data Information
    #
    ##########################################################################################
    def getDistanceCategories(self, debug=False):
        return ["VeryHigh", "High", "Mid", "Low", "VeryLow"]
    def getDistanceCategory(self, distance, debug=False):
        try:
            avg = distance['Avg']
            std = distance['Std']
        except:
            print("Could not get distance information from {0}".format(distance))

        category     = None
        significance = None
        if avg >= 50:
            category="VeryHigh"
        elif avg >= 20:
            category="High"
        elif avg >= 10:
            category="Mid"
        elif avg >= 5:
            category="Low"
        else:
            category="VeryLow"

        if std is not None:
            if std > 0:
                sig = avg/std
                if sig < 1:
                    significance = "Low"
                elif sig > 3:
                    significance = "High"
                else:
                    significance = "Mid"
            else:
                significance = "High"

        return category, significance

    def getDistanceFeatures(self, distanceData, debug):
        distanceFeatures = {}
        if distanceData is None:
            distanceCategory   = None
            distanceSignifance = None

        if isinstance(distanceData, dict):
            distanceCategory, distanceSignifance = self.getDistanceCategory(distanceData, debug)
        elif isinstance(distanceData, float):
            distanceCategory, distanceSignifance = self.getDistanceCategory({"Avg": distanceData, "Std": None}, debug)
        else:
            distanceCategory   = None
            distanceSignifance = None

        distanceFeatures["Name"]         = distanceCategory
        distanceFeatures["Significance"] = distanceSignifance
        if debug and False:
            print("  Found the following distance features:")
            for k,v in distanceFeatures.items():
                print("\t",k,"\t",v)
        return distanceFeatures



    ##########################################################################################
    #
    # DistanceRatio Data Information
    #
    ##########################################################################################
    def getDistanceRatioCategories(self, debug=False):
        return ["VeryHigh", "High", "Mid", "Low", "VeryLow"]
    def getDistanceRatioCategory(self, distanceRatio, debug=False):
        try:
            avg = distanceRatio['Avg']
            std = distanceRatio['Std']
        except:
            print("Could not get distance information from {0}".format(distance))

        category     = None
        significance = None
        if avg >= 2:
            category="VeryHigh"
        elif avg >= 4.0/3.0:
            category="High"
        elif avg >= 2.0/3.0:
            category="Mid"
        elif avg >= 0.5:
            category="Low"
        else:
            category="VeryLow"

        if std is not None:
            if std > 0:
                sig = avg/std
                if sig < 1:
                    significance = "Low"
                elif sig > 3:
                    significance = "High"
                else:
                    significance = "Mid"
            else:
                significance = "High"

        return category, significance

    def getDistanceRatioFeatures(self, distanceRatioData, debug):
        distanceRatioFeatures = {}
        if distanceRatioData is None:
            distanceRatioCategory   = None
            distanceRatioSignifance = None

        if isinstance(distanceRatioData, dict):
            distanceRatioCategory, distanceRatioSignifance = self.getDistanceRatioCategory(distanceRatioData, debug)
        elif isinstance(distanceRatioData, float):
            distanceRatioCategory, distanceRatioSignifance = self.getDistanceRatioCategory({"Avg": distanceRatioData, "Std": None}, debug)
        else:
            distanceRatioCategory   = None
            distanceRatioSignifance = None

        distanceRatioFeatures["Name"]         = distanceRatioCategory
        distanceRatioFeatures["Significance"] = distanceRatioSignifance
        if debug and False:
            print("  Found the following distance ratio features:")
            for k,v in distanceRatioFeatures.items():
                print("\t",k,"\t",v)
        return distanceRatioFeatures







    ##########################################################################################
    #
    # Weight Data Information
    #
    ##########################################################################################
    def getWeightCategories(self, debug=False):
        return ["VeryHigh", "High", "Mid", "Low", "VeryLow"]
    def getWeightCategory(self, weight, debug=False):
        avg = weight

        category     = None
        significance = None
        if avg >= 100:
            category="VeryHigh"
        elif avg >= 50:
            category="High"
        elif avg >= 25:
            category="Mid"
        elif avg >= 10:
            category="Low"
        else:
            category="VeryLow"

        return category, significance
    
    def getWeightFeatures(self, weightData, debug):
        weightFeatures = {}
        if weightData is None:
            weightCategory   = None
            weightSignifance = None
        else:
            weightCategory, weightSignifance = self.getWeightCategory(weightData, debug)

        weightFeatures["Name"]         = weightCategory
        weightFeatures["Significance"] = weightSignifance
        if debug and False:
            print("  Found the following weight features:")
            for k,v in weightFeatures.items():
                print("\t",k,"\t",v)
        return weightFeatures




    ##########################################################################################
    #
    # Interval Data Information
    #
    ##########################################################################################
    def getIntervalCategories(self, debug=False):
        return ["Long", "Mid", "Short"]
    def getIntervalCategory(self, interval, debug=False):
        avg = interval
        std = 0
        if interval is None:
            category = "Short"
            significance = "Low"
            return category, significance


        category     = None
        significance = None
        if avg >= 90:
            category="Long"
        elif avg >= 30:
            category="Mid"
        else:
            category="Short"

        if std is not None:
            if std > 0:
                sig = avg/std
                if sig < 1:
                    significance = "Low"
                elif sig > 3:
                    significance = "High"
                else:
                    significance = "Mid"
            else:
                significance = "High"

        return category, significance

    def getIntervalFeatures(self, intervalData, debug):
        intervalFeatures = {}
        if intervalData is None:
            intervalCategory   = None
            intervalSignifance = None
        else:
            intervalCategory, intervalSignifance = self.getIntervalCategory(intervalData, debug)

        intervalFeatures["Name"]         = intervalCategory
        intervalFeatures["Significance"] = intervalSignifance
        if debug and False:
            print("  Found the following interval features:")
            for k,v in intervalFeatures.items():
                print("\t",k,"\t",v)
        return intervalFeatures




    ##########################################################################################
    #
    # FractionActive Data Information
    #
    ##########################################################################################
    def getFractionActiveCategories(self, debug=False):
        return ["Low", "Mid", "High"]
    def getFractionActiveCategory(self, fracact, debug=False):
        avg = fracact
        std = 0
        if fracact is None:
            category = "Low"
            significance = None
            return category, significance


        category     = None
        significance = None
        if avg >= 0.8:
            category="High"
        elif avg >= 0.6:
            category="Mid"
        else:
            category="Low"

        return category, significance

    def getFractionActiveFeatures(self, fractionActiveData, debug):
        fractionActiveFeatures = {}
        if fractionActiveData is None:
            fractionActiveCategory   = None
            fractionActiveSignifance = None
        else:
            fractionActiveCategory, fractionActiveSignifance = self.getFractionActiveCategory(fractionActiveData, debug)

        fractionActiveFeatures["Name"]         = fractionActiveCategory
        fractionActiveFeatures["Significance"] = fractionActiveSignifance
        if debug and False:
            print("  Found the following fraction active features:")
            for k,v in fractionActiveFeatures.items():
                print("\t",k,"\t",v)
        return fractionActiveFeatures




    ##########################################################################################
    #
    # FractionActive Data Information
    #
    ##########################################################################################
    def getFractionVisitsCategories(self, debug=False):
        return ["Daily", "Weekly", "Monthly", "Infrequently"]
    def getFractionVisitsCategory(self, fracact, debug=False):
        avg = fracact
        std = 0
        if fracact is None:
            category = "Infrequently"
            significance = None
            return category, significance


        category     = None
        significance = None
        if avg >= 10.0/30.0:
            category="Daily"
        elif avg >= 3.0/30.0:
            category="Weekly"
        elif avg >= 0.5/30.0:
            category="Monthly"
        else:
            category="Infrequently"
            

        return category, significance

    def getFractionVisitsFeatures(self, fractionActiveData, debug):
        fractionActiveFeatures = {}
        if fractionActiveData is None:
            fractionActiveCategory   = None
            fractionActiveSignifance = None
        else:
            fractionActiveCategory, fractionActiveSignifance = self.getFractionVisitsCategory(fractionActiveData, debug)

        fractionActiveFeatures["Name"]         = fractionActiveCategory
        fractionActiveFeatures["Significance"] = fractionActiveSignifance
        if debug and False:
            print("  Found the following fraction active features:")
            for k,v in fractionActiveFeatures.items():
                print("\t",k,"\t",v)
        return fractionActiveFeatures




    ##########################################################################################
    #
    # DailyVisits Data Information
    #
    ##########################################################################################
    def getDailyVisitsCategories(self, debug=False):
        return ["Long", "Mid", "Short"]
    def getDailyVisitsCategory(self, dailyVisits, debug=False):
        avg = dailyVisits
        std = 0
        if dailyVisits is None:
            category = "Short"
            significance = "Low"
            return category, significance


        category     = None
        significance = None
        if avg >= 90:
            category="Long"
        elif avg >= 30:
            category="Mid"
        else:
            category="Short"

        if std is not None:
            if std > 0:
                sig = avg/std
                if sig < 1:
                    significance = "Low"
                elif sig > 3:
                    significance = "High"
                else:
                    significance = "Mid"
            else:
                significance = "High"

        return category, significance

    def getDailyVisitsFeatures(self, dailyVisitsData, debug):
        dailyVisitsFeatures = {}
        if dailyVisitsData is None:
            dailyVisitsCategory   = None
            dailyVisitsSignifance = None
        else:
            dailyVisitsCategory, dailyVisitsSignifance = self.getDailyVisitsCategory(dailyVisitsData, debug)

        dailyVisitsFeatures["Name"]         = dailyVisitsCategory
        dailyVisitsFeatures["Significance"] = dailyVisitsSignifance
        if debug and False:
            print("  Found the following daily visits features:")
            for k,v in dailyVisitsFeatures.items():
                print("\t",k,"\t",v)
        return dailyVisitsFeatures




    ##########################################################################################
    #
    # Overnight Stays Data Information
    #
    ##########################################################################################
    def getOvernightStaysCategories(self, debug=False):
        return ["Long", "Mid", "Short"]
    def getOvernightStaysCategory(self, overnightStays, debug=False):
        avg = overnightStays
        std = 0
        if overnightStays is None:
            category = "Short"
            significance = "Low"
            return category, significance


        category     = None
        significance = None
        if avg >= 90:
            category="Long"
        elif avg >= 30:
            category="Mid"
        else:
            category="Short"

        if std is not None:
            if std > 0:
                sig = avg/std
                if sig < 1:
                    significance = "Low"
                elif sig > 3:
                    significance = "High"
                else:
                    significance = "Mid"
            else:
                significance = "High"

        return category, significance

    def getOvernightStaysFeatures(self, overnightStaysData, debug):
        overnightStaysFeatures = {}
        if overnightStaysData is None:
            overnightStaysCategory   = None
            overnightStaysSignifance = None
        else:
            overnightStaysCategory, overnightStaysSignifance = self.getOvernightStaysCategory(overnightStaysData, debug)

        overnightStaysFeatures["Name"]         = overnightStaysCategory
        overnightStaysFeatures["Significance"] = overnightStaysSignifance
        if debug and False:
            print("  Found the following overnight stays features:")
            for k,v in overnightStaysFeatures.items():
                print("\t",k,"\t",v)
        return overnightStaysFeatures




    ##########################################################################################
    #
    # DayOfWeek Data Information
    #
    ##########################################################################################
    def getDayOfWeekCategories(self, debug=False):
        return ["Weekend", "Weekday", "Week"]
    def getDayOfWeekCategory(self, day, debug=False):
        try:
            avg = day['Avg']
            std = day['Std']
        except:
            print("Could not get day information from {0}".format(day))

        category = None
        significance = None
        if avg >= 3.0/7.0:
            category="Weekend"
        elif avg <= 1.0/7.0:
            category="Weekday"
        else:
            category="Week"

        if std is not None:
            if std > 0:
                sig = avg/std
                if sig < 1:
                    significance = "Low"
                elif sig > 3:
                    significance = "High"
                else:
                    significance = "Mid"
            else:
                significance = "High"

        return category, significance

    def getDayOfWeekFeatures(self, dayofweekData, debug):
        dayofweekFeatures = {}
        if dayofweekData is None:
            dayofweekCategory   = None
            dayofweekSignifance = None

        if isinstance(dayofweekData, dict):
            dayofweekCategory, dayofweekSignifance = self.getDayOfWeekCategory(dayofweekData, debug)
        elif isinstance(dayofweekData, float):
            dayofweekCategory, dayofweekSignifance = self.getDayOfWeekCategory({"Avg": dayofweekData, "Std": None}, debug)
        else:
            dayofweekCategory   = None
            dayofweekSignifance = None

        dayofweekFeatures["Name"]         = dayofweekCategory
        dayofweekFeatures["Significance"] = dayofweekSignifance
        if debug and False:
            print("  Found the following DayOfWeek features:")
            for k,v in dayofweekFeatures.items():
                print("\t",k,"\t",v)
        return dayofweekFeatures




    ##########################################################################################
    #
    # N Data Information
    #
    ##########################################################################################
    def getNCategories(self, debug=False):
        return ["Low", "Mid", "High"]
    def getNCategory(self, n, debug=False):
        try:
            avg = day['Avg']
            std = day['Std']
        except:
            print("Could not get N information from {0}".format(n))

        category = None
        significance = None
        if avg >= 50:
            category="High"
        elif avg <= 10:
            category="Low"
        else:
            category="Mid"

        return category, significance

    def getNFeatures(self, nData, debug):
        nFeatures = {}
        if nData is None:
            nCategory   = None
            nSignifance = None

        if isinstance(nData, dict):
            nCategory, nSignifance = self.getNCategory(nData, debug)
        elif isinstance(nData, float):
            nCategory, nSignifance = self.getNCategory({"Avg": nData, "Std": None}, debug)
        else:
            nCategory   = None
            nSignifance = None

        nFeatures["Name"]         = nCategory
        nFeatures["Significance"] = nSignifance
        if debug and False:
            print("  Found the following N features:")
            for k,v in nFeatures.items():
                print("\t",k,"\t",v)
        return nFeatures




    ##########################################################################################
    #
    # ITA Data Information
    #
    ##########################################################################################
    def getITACategories(self, debug=False):
        return ["VeryHigh", "High", "Mid", "Low", "VeryLow"]
    def getITACategory(self, ita, debug=False):
        try:
            avg = ita['Avg']
            std = ita['Std']
        except:
            print("Could not get ITA information from {0}".format(ita))

        category     = None
        significance = None
        if avg <= 1:
            category="VeryHigh"
        elif avg <= 2:
            category="High"
        elif avg <= 7:
            category="Mid"
        elif avg <= 14:
            category="Low"
        else:
            category="VeryLow"

        if std is not None:
            if std > 0:
                sig = avg/std
                if sig < 1:
                    significance = "Low"
                elif sig > 3:
                    significance = "High"
                else:
                    significance = "Mid"
            else:
                significance = "High"

        return category, significance

    def getITAFeatures(self, itaData, debug):
        itaFeatures = {}
        if itaData is None:
            itaCategory   = None
            itaSignifance = None

        if isinstance(itaData, dict):
            itaCategory, itaSignifance = self.getITACategory(itaData, debug)
        else:
            itaCategory   = None
            itaSignifance = None

        itaFeatures["Name"]         = itaCategory
        itaFeatures["Significance"] = itaSignifance
        if debug and False:
            print("  Found the following ita features:")
            for k,v in itaFeatures.items():
                print("\t",k,"\t",v)
        return itaFeatures




    ##########################################################################################
    #
    # Numerical Data Information
    #
    ##########################################################################################