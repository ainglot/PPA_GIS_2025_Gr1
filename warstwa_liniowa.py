import arcpy


# === USTAWIENIA ŚRODOWISKA ===
arcpy.env.workspace = r"D:\GIS\Rok_2025_26\PPA_ArcGIS\PPA_Gr1.gdb"
warstwa_2014 = "GDA2014_OT_SWRS_L"
warstwa_2020 = "GDA2020_OT_SWRS_L"

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

def wstawianie_wspolrzednych_linie(warstwa, lista_ob):
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

def wstawianie_wspolrzednych_punkty(warstwa, lista_wsp):
    with arcpy.da.InsertCursor(warstwa, ['SHAPE@X', 'SHAPE@Y']) as cursor:
        for wsp in lista_wsp:
            X = wsp[0]
            Y = wsp[1]
            cursor.insertRow([X, Y])

# lista_wsp = odczytywanie_wspolrzednych(warstwa_liniowa)
# print(lista_wsp[:2])
# print(len(lista_wsp), len(lista_wsp[0]))

# simplified_lines = [[line[0], line[-1]] for line in lista_wsp]

# nowa_warstwa = "Linie_SWRS_02"
# arcpy.management.CreateFeatureclass(arcpy.env.workspace, nowa_warstwa, "POLYLINE", "", "DISABLED", "DISABLED", warstwa_liniowa)
# wstawianie_wspolrzednych(nowa_warstwa, simplified_lines)

lista_2014 = odczytywanie_wspolrzednych(warstwa_2014)
lista_2020 = odczytywanie_wspolrzednych(warstwa_2020)

from typing import List, Tuple

def extract_all_vertices(lines: List[list]) -> set:
    """Zwraca zbiór wszystkich wierzchołków z listy linii jako krotki zaokrąglonych współrzędnych"""
    vertices = set()
    for line in lines:
        for x, y in line:
            # Zaokrąglamy do 2 miejsc po przecinku → dokładność ~1 cm (dla układów PUWG/ESRI)
            vertices.add((round(x, 2), round(y, 2)))
    return vertices

# Wyciągamy wszystkie wierzchołki z obu warstw
verts_2014 = extract_all_vertices(lista_2014)
verts_2020 = extract_all_vertices(lista_2020)

# Różnice
only_in_2014 = list(verts_2014 - verts_2020)   # zniknęły w 2020
only_in_2020 = list(verts_2020 - verts_2014)   # pojawiły się w 2020

print(f"Zniknęło (były w 2014, nie ma w 2020): {len(only_in_2014)} punktów")
print(f"Pojawiło się (nie było w 2014, jest w 2020): {len(only_in_2020)} punktów")

print(only_in_2014[:5])

nowa_warstwa = "Punkty_2014_01"
arcpy.management.CreateFeatureclass(arcpy.env.workspace, nowa_warstwa, "POINT", "", "DISABLED", "DISABLED", warstwa_2020)
wstawianie_wspolrzednych_punkty(nowa_warstwa, only_in_2014)
nowa_warstwa = "Punkty_2020_01"
arcpy.management.CreateFeatureclass(arcpy.env.workspace, nowa_warstwa, "POINT", "", "DISABLED", "DISABLED", warstwa_2020)
wstawianie_wspolrzednych_punkty(nowa_warstwa, only_in_2020)


print("KONIEC")