import arcpy


# === USTAWIENIA ŚRODOWISKA ===
arcpy.env.workspace = r"D:\GIS\Rok_2025_26\PPA_ArcGIS\PPA_Gr1.gdb"
warstwa_poligonowa = "Budynki"

geometries = arcpy.management.CopyFeatures(warstwa_poligonowa, arcpy.Geometry())

Otoczka = []
for geo in geometries:
    
    Otoczka.append(geo.convexHull())

warstwa_wyjsciowa = "Budynki_Otoczka_01"
arcpy.management.CopyFeatures(Otoczka, warstwa_wyjsciowa)
print("KONIEC")