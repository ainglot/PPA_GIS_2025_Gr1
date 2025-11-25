import arcpy


# === USTAWIENIA ŚRODOWISKA ===
arcpy.env.workspace = r"D:\GIS\Rok_2025_26\PPA_ArcGIS\PPA_Gr1.gdb"
warstwa_liniowa = "GDA2020_OT_SWRS_L"

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

# def wstawianie_wspolrzednych(warstwa, lista_wsp):
#     with arcpy.da.InsertCursor(warstwa, ['SHAPE@X', 'SHAPE@Y']) as cursor:
#         for wsp in lista_wsp:
#             X = wsp[0]
#             Y = wsp[1]
#             cursor.insertRow([X, Y])

lista_wsp = odczytywanie_wspolrzednych(warstwa_liniowa)
# print(lista_wsp)
print(len(lista_wsp), len(lista_wsp[0]))

# nowa_warstwa = "Centroidy_SWRS_01"
# arcpy.management.CreateFeatureclass(arcpy.env.workspace, nowa_warstwa, "POINT", "", "DISABLED", "DISABLED", warstwa_liniowa)
# wstawianie_wspolrzednych(nowa_warstwa, lista_wsp)

print("KONIEC")