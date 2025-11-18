import arcpy
import math
from typing import List, Tuple
from collections import defaultdict
import numpy as np


# === USTAWIENIA ŚRODOWISKA ===
arcpy.env.workspace = r"D:\GIS\Rok_2025_26\PPA_ArcGIS\PPA_Gr1.gdb"
warstwa_punktowa = "GDA2020_OT_OIPR_P"

# === FUNKCJE DLA WARSTWY PUNKTOWEJ ===
def odczytywanie_wspolrzednych(warstwa):
    lista_wsp = []
    with arcpy.da.SearchCursor(warstwa, ['SHAPE@X', 'SHAPE@Y']) as cursor:
        for row in cursor:
            lista_wsp.append(row)
    return lista_wsp

def aktualizowanie_wspolrzednych(warstwa):
    with arcpy.da.UpdateCursor(warstwa, ['SHAPE@X', 'SHAPE@Y']) as cursor:
        for row in cursor:
            row[0] += 100
            row[1] += 100
            cursor.updateRow(row)

def wstawianie_wspolrzednych(warstwa, lista_wsp, field):
    with arcpy.da.InsertCursor(warstwa, ['SHAPE@X', 'SHAPE@Y', 'SHAPE@Z', field]) as cursor:
        for wsp in lista_wsp:
            X = wsp[0]
            Y = wsp[1]
            Z = wsp[2]
            cursor.insertRow([X, Y, Z, Z])

# === WYWOŁYWANIE FUNKCJI ===

# ### Tworzenie pustej warstwy
# lista_wybranych = odczytywanie_wspolrzednych(warstwa_punktowa)[:150]
# print(lista_wybranych)
# nowa_warstwa = "GDA2020_OT_OIPR_P_150pierwszych"
# arcpy.management.CreateFeatureclass(arcpy.env.workspace, nowa_warstwa, "POINT", "", "DISABLED", "DISABLED", warstwa_punktowa)
# wstawianie_wspolrzednych(nowa_warstwa, lista_wybranych)
# # aktualizowanie_wspolrzednych(warstwa_punktowa)

## wybierzmy X punktów najbliższych do średniej wartości X i Y z zbioru punktów

# # Krok 1: Obliczenie środka (średnich współrzędnych)
# coordinates = odczytywanie_wspolrzednych(warstwa_punktowa)
# n = len(coordinates)
# x_mean = sum(x for x, y in coordinates) / n
# y_mean = sum(y for x, y in coordinates) / n
# center = (x_mean, y_mean)

# print(f"Środek: ({x_mean:.3f}, {y_mean:.3f})")

# # Krok 2: Obliczenie odległości każdego punktu do środka + sortowanie
# def distance_to_center(point: Tuple[float, float]) -> float:
#     x, y = point
#     return math.sqrt((x - x_mean)**2 + (y - y_mean)**2)

# # Dodajemy odległość jako trzeci element, żeby później łatwo sortować
# points_with_dist = [(x, y, distance_to_center((x, y))) for x, y in coordinates]

# # Sortujemy po odległości (rosnąco)
# points_with_dist.sort(key=lambda p: p[2])

# # Krok 3: Wybierz ile chcesz najbliższych punktów, np. 150
# k = 150  # zmień na ile potrzebujesz
# nearest_points = points_with_dist[:k]

# # # Jeśli chcesz tylko same współrzędne (bez odległości):
# # nearest_coordinates = [(x, y) for x, y, dist in nearest_points]

# # Opcjonalnie: wypisz wyniki z odległościami
# print(f"\n{k} punktów najbliższych do środka:")
# for i, (x, y, dist) in enumerate(nearest_points, 1):
#     print(f"{i:3}. ({x:.2f}, {y:.2f}) → odległość: {dist:.2f} m")

# nowa_warstwa = "GDA2020_OT_OIPR_P_150dist"
# arcpy.management.CreateFeatureclass(arcpy.env.workspace, nowa_warstwa, "POINT", "", "DISABLED", "DISABLED", warstwa_punktowa)
# arcpy.management.AddField(nowa_warstwa, "dist", "FLOAT")
# wstawianie_wspolrzednych(nowa_warstwa, nearest_points, "dist")

### Konwersja danych z txt do warstwy wektorowej punktowej


# wczytuje plik i od razu tworzy listę [[x, y, z], ...]
with open('data.txt', 'r') as f:
    points = []
    for line in f:
        line = line.strip()          # usuwa \n i ewentualne spacje na końcach
        if line:                     # pomija puste linie
            x, y, z = map(float, line.split())
            points.append([x+470856, y+741111, z])

# print(points[:50])

# nowa_warstwa = "Silos02"
# arcpy.management.CreateFeatureclass(arcpy.env.workspace, nowa_warstwa, "POINT", "", "DISABLED", "ENABLED", warstwa_punktowa)
# arcpy.management.AddField(nowa_warstwa, "wsp_z", "FLOAT")
# wstawianie_wspolrzednych(nowa_warstwa, points, "wsp_z")


from collections import defaultdict
import numpy as np

# ------------------- ROZWIĄZANIE -------------------

# 1. Znajdź minimalne Z
z_values = [p[2] for p in points]
z_min = min(z_values)
z_max = max(z_values)

print(f"Z od {z_min:.3f} do {z_max:.3f} m")

# 2. Grupowanie punktów w przedziały co 2 m
interval = 2.0

# Słownik: klucz = dolna granica przedziału (np. -2.0, 0.0, 2.0, ...)
layers = defaultdict(list)

# for x, y, z in points:
#     # Oblicz dolną granicę przedziału, do którego należy z
#     layer_key = (z // interval) * interval    # dla z >= 0
#     if z < 0:
#         layer_key = ((z // interval) - 1) * interval if z % interval != 0 else (z // interval) * interval
    
#     layers[layer_key].append([x, y, z])

# Alternatywnie – bardziej czytelne i uniwersalne (działa dla dowolnych z):
layers = defaultdict(list)
for x, y, z in points:
    layer_key = interval * np.floor(z / interval)   # to jest najprostsze i zawsze działa poprawnie
    layers[layer_key].append([x, y, z])

# 3. Oblicz średnie dla każdej warstwy
result = []

for z_bottom in sorted(layers.keys()):
    pts_in_layer = layers[z_bottom]
    xs = [p[0] for p in pts_in_layer]
    ys = [p[1] for p in pts_in_layer]
    
    avg_x = sum(xs) / len(xs)
    avg_y = sum(ys) / len(ys)
    avg_z = (z_bottom + z_bottom + interval) / 2   # środek przedziału (opcjonalnie)
    count = len(pts_in_layer)
    
    result.append({
        'z_from': z_bottom,
        'z_to':   z_bottom + interval,
        'z_mid':  avg_z,
        'avg_x':  avg_x,
        'avg_y':  avg_y,
        'count':  count,
        'points': pts_in_layer
    })

# 4. Wyświetl wyniki
print("\nŚrednie współrzędne co 2 m wysokości:")
print("Z od-do      |   średnie X   |   średnie Y   | liczba punktów")
print("-" * 60)
for r in result:
    print(f"{r['z_from']:6.2f}–{r['z_to']:6.2f} | {r['avg_x']:12.4f} | {r['avg_y']:12.4f} | {r['count']:6d}")

# Jeśli chcesz tylko listę [avg_x, avg_y, z_mid]
average_points = [[r['avg_x'], r['avg_y'], r['z_mid']] for r in result]
print("\nLista średnich punktów:", average_points)

nowa_warstwa = "Silos04"
arcpy.management.CreateFeatureclass(arcpy.env.workspace, nowa_warstwa, "POINT", "", "DISABLED", "ENABLED", warstwa_punktowa)
arcpy.management.AddField(nowa_warstwa, "wsp_z", "FLOAT")
wstawianie_wspolrzednych(nowa_warstwa, average_points, "wsp_z")



print("KONIEC")