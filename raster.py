import arcpy

# === USTAWIENIA ŚRODOWISKA  I DANE WEJŚCIOWE ===
arcpy.env.workspace = r"D:\GIS\Rok_2025_26\PPA_ArcGIS\NMT"
RasterIn = "81440_1641696_M-34-101-A-c-4-3.asc"
arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(2180) #przypisanie układu współrzędnych do rastra wyjściowego

# === WCZYTYWANIE RASTRA JAKO OBIEKT RASTER ===
R = arcpy.Raster(RasterIn)
print(f"Minimum: {R.minimum} i maximum {R.maximum} na rastrze.")
print(f"Rozdzielczość przestrzenna rastra: {R.meanCellWidth}")

# # === PARAMETRY RASTRA ===
# LewyDolnyPunkt = arcpy.Point(R.extent.XMin, R.extent.YMin) #przechowanie współrzędnych do lokalizacji rastra wyjściowego
# RozdzielczoscPrzestrzenna = R.meanCellWidth #rozdzielczość przestrzenna rastra
# NoData = 0 #wartość NoData - w tym rastrze minimalna wartość jest większa niż 0, można tak wykonać

# # === ZAPISUJEMY RASTER DO TABLICY NUMPY ===
# R_array = arcpy.RasterToNumPyArray(R, nodata_to_value = NoData)

# # === PROWADZIMY OBLICZENIA ===
# R_array[100:200, 100:200] = 0 # W lewym gónym rógó rastra "wycinamy" prostokąt

# # === WRACAMY Z TABLICY NUMPY DO RASTRA I ZAPISUJEMY DO NOWEGO PLIKU ===
# outR = arcpy.NumPyArrayToRaster(R_array, LewyDolnyPunkt, RozdzielczoscPrzestrzenna, value_to_nodata = NoData)
# # zapisać nowy raster trzeba podać - dane (R_array), współrzędne lewego dolnego naroża, rozdzielczość przestrzenną i jaką wartość przyjmuje NoData
# outR.save("NowyRaster")
print("KONIEC")