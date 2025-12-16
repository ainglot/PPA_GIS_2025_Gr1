import arcpy
import numpy as np
import math

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

def wstawianie_wspolrzednych(warstwa, lista_wsp, field):
    with arcpy.da.InsertCursor(warstwa, ['SHAPE@X', 'SHAPE@Y', 'SHAPE@Z', field]) as cursor:
        for wsp in lista_wsp:
            X = wsp[0]
            Y = wsp[1]
            Z = wsp[2]
            cursor.insertRow([X, Y, Z, Z])

def odleglosc_2d(p1, p2):
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    return math.hypot(x2 - x1, y2 - y1)

def odleglosc_3d(p1, p2):
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    return math.sqrt(
        (x2 - x1)**2 +
        (y2 - y1)**2 +
        (z2 - z1)**2
    )

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

PKT = [473593., 721194.]
PKT = [474432.81, 718876.37] #45.669998

listaWSP = []
for linia in Wsp_Linie:
    for PKT in linia:
        for ras in listR:
            if punkt_na_rastrze(PKT, ras[1]):
                R = arcpy.Raster(ras[0])
                R_array = arcpy.RasterToNumPyArray(R, nodata_to_value = np.nan) 
                XMIN = ras[1][0]
                YMAX = ras[1][3]
                CellSIZE = R.meanCellWidth

                dx = (PKT[0] - XMIN) * CellSIZE
                dy = (YMAX - PKT[1]) * CellSIZE

                row = int(dy)
                col = int(dx)
                print(dx, dy, row, col, R_array[row, col])
                if not np.isnan(R_array[row, col]):
                    listaWSP.append([PKT[0], PKT[1], R_array[row, col]])

nowa_warstwa = "PunktyNaRastrze03"
# arcpy.env.workspace = r"D:\GIS\Rok_2025_26\PPA_ArcGIS\Geobaza ZTM\ZTM197.gdb"
# arcpy.management.CreateFeatureclass(arcpy.env.workspace, nowa_warstwa, "POINT", "", "DISABLED", "ENABLED", warstwa_liniowa)
# arcpy.management.AddField(nowa_warstwa, "wsp_z", "FLOAT")
# wstawianie_wspolrzednych(nowa_warstwa, listaWSP, "wsp_z")

s2d = 0.
s3d = 0.
for i in range(len(listaWSP)-1):
    xyz0 = listaWSP[i]
    xyz1 = listaWSP[i+1]
    s2d += odleglosc_2d(xyz0, xyz1)
    s3d += odleglosc_3d(xyz0, xyz1)

print("KONIEC")