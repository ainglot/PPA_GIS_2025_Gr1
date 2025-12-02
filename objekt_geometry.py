import arcpy


# === USTAWIENIA ŚRODOWISKA ===
arcpy.env.workspace = r"D:\GIS\Rok_2025_26\PPA_ArcGIS\PPA_Gr1.gdb"
warstwa_poligonowa = "Budynki"

geometries = arcpy.management.CopyFeatures(warstwa_poligonowa, arcpy.Geometry())

i = 0
for geo1 in geometries:
    j = 0
    for geo2 in geometries:
        if i < j:
            print(i, j, geo1.touches(geo2))
        j += 1
    i += 1


# Otoczka = []
# for geo in geometries:
#     AREA = geo.area
#     print(AREA)
#     if AREA>100:
#         Otoczka.append(geo.buffer(2))
#     else:
#         Otoczka.append(geo.buffer(5))


# warstwa_wyjsciowa = "Budynki_Otoczka_04"
# arcpy.management.CopyFeatures(Otoczka, warstwa_wyjsciowa)
print("KONIEC")