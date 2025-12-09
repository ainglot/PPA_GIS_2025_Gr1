import arcpy

arcpy.env.workspace = r"C:\GIS\GeoportalDane\NMTwyk11"
RasterIn = "4228_280105_M-34-101-A-c-3-2.asc"
arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(2180) #przypisanie układu współrzędnych do rastra wyjściowego
R = arcpy.Raster(RasterIn)
LewyDolnyPunkt = arcpy.Point(R.extent.XMin, R.extent.YMin) #przechowanie współrzędnych do lokalizacji rastra wyjściowego
RozdzielczoscPrzestrzenna = R.meanCellWidth #rozdzielczość przestrzenna rastra
NoData = 0 #wartość NoData - w tym rastrze minimalna wartość jest większa niż 0, można tak wykonać
R_array = arcpy.RasterToNumPyArray(R, nodata_to_value = NoData)
R_array[100:200, 100:200] = 0 # W lewym gónym rógó rastra "wycinamy" prostokąt
outR = arcpy.NumPyArrayToRaster(R_array, LewyDolnyPunkt, RozdzielczoscPrzestrzenna, value_to_nodata = NoData)
# zapisać nowy raster trzeba podać - dane (R_array), współrzędne lewego dolnego naroża, rozdzielczość przestrzenną i jaką wartość przyjmuje NoData
outR.save("NowyRaster")
print("KONIEC")