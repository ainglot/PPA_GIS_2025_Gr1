import arcpy
import math
from typing import List, Tuple


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

def wstawianie_wspolrzednych(warstwa, lista_wsp):
    with arcpy.da.InsertCursor(warstwa, ['SHAPE@X', 'SHAPE@Y']) as cursor:
        for wsp in lista_wsp:
            cursor.insertRow(wsp)

# === WYWOŁYWANIE FUNKCJI ===

# ### Tworzenie pustej warstwy
# lista_wybranych = odczytywanie_wspolrzednych(warstwa_punktowa)[:150]
# print(lista_wybranych)
# nowa_warstwa = "GDA2020_OT_OIPR_P_150pierwszych"
# arcpy.management.CreateFeatureclass(arcpy.env.workspace, nowa_warstwa, "POINT", "", "DISABLED", "DISABLED", warstwa_punktowa)
# wstawianie_wspolrzednych(nowa_warstwa, lista_wybranych)
# # aktualizowanie_wspolrzednych(warstwa_punktowa)

## wybierzmy X punktów najbliższych do średniej wartości X i Y z zbioru punktów

# Krok 1: Obliczenie środka (średnich współrzędnych)
coordinates = odczytywanie_wspolrzednych(warstwa_punktowa)
n = len(coordinates)
x_mean = sum(x for x, y in coordinates) / n
y_mean = sum(y for x, y in coordinates) / n
center = (x_mean, y_mean)

print(f"Środek: ({x_mean:.3f}, {y_mean:.3f})")

# Krok 2: Obliczenie odległości każdego punktu do środka + sortowanie
def distance_to_center(point: Tuple[float, float]) -> float:
    x, y = point
    return math.sqrt((x - x_mean)**2 + (y - y_mean)**2)

# Dodajemy odległość jako trzeci element, żeby później łatwo sortować
points_with_dist = [(x, y, distance_to_center((x, y))) for x, y in coordinates]

# Sortujemy po odległości (rosnąco)
points_with_dist.sort(key=lambda p: p[2])

# Krok 3: Wybierz ile chcesz najbliższych punktów, np. 150
k = 150  # zmień na ile potrzebujesz
nearest_points = points_with_dist[:k]

# # Jeśli chcesz tylko same współrzędne (bez odległości):
# nearest_coordinates = [(x, y) for x, y, dist in nearest_points]

# Opcjonalnie: wypisz wyniki z odległościami
print(f"\n{k} punktów najbliższych do środka:")
for i, (x, y, dist) in enumerate(nearest_points, 1):
    print(f"{i:3}. ({x:.2f}, {y:.2f}) → odległość: {dist:.2f} m")


print("KONIEC")