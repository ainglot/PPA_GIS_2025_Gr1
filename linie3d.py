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

def punkt_na_rastrze(punkt, zakres_rastra):
    x, y = punkt
    xmin, ymin, xmax, ymax = zakres_rastra

    return xmin <= x <= xmax and ymin <= y <= ymax

Wsp_Linie = odczytywanie_wspolrzednych(warstwa_liniowa)
# print(Wsp_Linie)

arcpy.env.workspace = r"D:\GIS\Rok_2025_26\PPA_ArcGIS\NMT pod ZTM\ZTM197_NMT_TIF"
rasters = arcpy.ListRasters("*", "TIF")

listR = []
for raster in rasters:
    print(raster)
    R = arcpy.Raster(raster)
    listR.append([raster, [R.extent.XMin, R.extent.YMin, R.extent.XMax, R.extent.YMax]])
# print(listR)

PKT = [473592., 721195.]

for ras in listR:
    if punkt_na_rastrze(PKT, ras[1]):
        XMIN = ras[1][0]
        YMAX = ras[1][3]
        dx = PKT[0] - XMIN
        dy = YMAX - PKT[1]
        print(dx, dy)



print("KONIEC")