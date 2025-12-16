import arcpy


# === USTAWIENIA ŚRODOWISKA ===
arcpy.env.workspace = r"D:\GIS\Rok_2025_26\PPA_ArcGIS\Geobaza ZTM\ZTM197.gdb"
warstwa_liniowa = "ZTM_195_PL92"

# === FUNKCJE DLA WARSTWY PUNKTOWEJ ===
def odczytywanie_wspolrzednych(warstwa):
    lista_ob = []
    with arcpy.da.SearchCursor(warstwa, ['SHAPE@']) as cursor:
        for row in cursor:
            lista_wsp = []
            for part in row[0]:
                for pnt in part:
                    lista_wsp.append([pnt.X, pnt.Y])
            lista_ob.append(lista_wsp)
    return lista_ob


Wsp_Linie = odczytywanie_wspolrzednych(warstwa_liniowa)
# print(Wsp_Linie)

arcpy.env.workspace = r"D:\GIS\Rok_2025_26\PPA_ArcGIS\NMT pod ZTM\ZTM197_NMT_TIF"
rasters = arcpy.ListRasters("*", "TIF")

listR = []
for raster in rasters:
    print(raster)
    R = arcpy.Raster(raster)
    listR.append([raster, [R.extent.XMin, R.extent.YMin, R.extent.XMiax, R.extent.YMax]])
print(listR)

print("KONIEC")