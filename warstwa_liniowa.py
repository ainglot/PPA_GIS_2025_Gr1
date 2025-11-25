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

def wstawianie_wspolrzednych(warstwa, lista_ob):
    with arcpy.da.InsertCursor(warstwa, ['SHAPE@']) as cursor:
        pnt = arcpy.Point()
        array = arcpy.Array()
        for ob in lista_ob:
            for pkt in ob:
                pnt.X = pkt[0]
                pnt.Y = pkt[1]
                array.add(pnt)
            poly = arcpy.Polyline(array)
            array.removeAll()
            cursor.insertRow([poly])

lista_wsp = odczytywanie_wspolrzednych(warstwa_liniowa)
print(lista_wsp[:2])
print(len(lista_wsp), len(lista_wsp[0]))

simplified_lines = [[line[0], line[-1]] for line in lista_wsp]

nowa_warstwa = "Linie_SWRS_02"
arcpy.management.CreateFeatureclass(arcpy.env.workspace, nowa_warstwa, "POLYLINE", "", "DISABLED", "DISABLED", warstwa_liniowa)
wstawianie_wspolrzednych(nowa_warstwa, simplified_lines)

print("KONIEC")