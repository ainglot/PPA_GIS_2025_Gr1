import arcpy
import numpy as np

# === USTAWIENIA ŚRODOWISKA I DANE WEJŚCIOWE ===
arcpy.env.workspace = r"D:\GIS\Rok_2025_26\PPA_ArcGIS\NMT"
arcpy.env.overwriteOutput = True  # ważne, żeby nadpisywał pliki
RasterIn = "81440_1641696_M-34-101-A-c-4-3.asc"

# Ustawienie układu współrzędnych wyjściowego (2180 - PUWG 1992)
arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(2180)

# === WCZYTYWANIE RASTRA ===
R = arcpy.Raster(RasterIn)

print(f"Raster wczytany: {RasterIn}")
print(f"Minimum: {R.minimum:.3f}, Maximum: {R.maximum:.3f}")
print(f"Rozdzielczość: {R.meanCellWidth} x {R.meanCellHeight}")
print(f"Zakres rastra: X: {R.extent.XMin} - {R.extent.XMax}, Y: {R.extent.YMin} - {R.extent.YMax}")

# === PARAMETRY RASTRA ===
lower_left = arcpy.Point(R.extent.XMin, R.extent.YMin)   # lewy dolny róg
cell_size = R.meanCellWidth                              # zakładamy kwadratowe komórki
nodata_val = 0  # w Twoim pliku ASC NoData to zazwyczaj -9999 albo inna wartość – sprawdź!

# === KONWERSJA DO NUMPY ===
# Używamy nodata_to_value tylko jeśli naprawdę chcesz zamienić NoData na 0
# Lepiej zachować oryginalne NoData, więc najczęściej wystarczy:
R_array = arcpy.RasterToNumPyArray(R)  # bez parametru nodata_to_value

# Jeśli w Twoim ASC NoData to np. -9999, a chcesz je wykluczyć z min/max:
# R_array = arcpy.RasterToNumPyArray(R, nodata_to_value=np.nan)  # wtedy nan nie będzie brany pod uwagę

# === ZNAJDOWANIE POZYCJI MIN I MAX ===
# Maskujemy ewentualne NoData (jeśli występują jako bardzo niskie wartości)
masked_array = np.ma.masked_equal(R_array, R.noDataValue)  # poprawnie maskuje NoData

min_val = float(masked_array.min())
max_val = float(masked_array.max())

# Współrzędne indeksów (wiersz, kolumna)
min_idx = np.unravel_index(np.argmin(masked_array), R_array.shape)  # (wiersz, kolumna)
max_idx = np.unravel_index(np.argmax(masked_array), R_array.shape)  # (wiersz, kolumna)

# Przeliczenie indeksów [wiersz, kolumna] na współrzędne X, Y (środek komórki!)
def cell_to_coord(row, col, lower_left_corner, cell_size):
    x = lower_left_corner.X + col * cell_size + cell_size / 2
    y = lower_left_corner.Y + (R_array.shape[0] - 1 - row) * cell_size + cell_size / 2
    # ^ odwracamy wiersz, bo NumPy ma początek w lewym GÓRNYM rogu
    return x, y

min_x, min_y = cell_to_coord(min_idx[0], min_idx[1], lower_left, cell_size)
max_x, max_y = cell_to_coord(max_idx[0], max_idx[1], lower_left, cell_size)

# === WYNIK ===
print("\n" + "="*60)
print(f"MINIMUM: {min_val:.3f} m n.p.m.")
print(f"   położenie: X = {min_x:.3f}, Y = {min_y:.3f} (układ 2180)")
print(f"   indeks w tablicy: wiersz {min_idx[0]}, kolumna {min_idx[1]}")

print(f"MAKSYMUM: {max_val:.3f} m n.p.m.")
print(f"   położenie: X = {max_x:.3f}, Y = {max_y:.3f} (układ 2180)")
print(f"   indeks w tablicy: wiersz {max_idx[0]}, kolumna {max_idx[1]}")
print("="*60)

# === OPCJONALNIE: zapisanie punktów min i max jako shapefile ===
point_fc = "MinMax_Punkty.shp"
if arcpy.Exists(point_fc):
    arcpy.Delete_management(point_fc)

# Tworzymy punkty
points = arcpy.Array([
    arcpy.Point(min_x, min_y),
    arcpy.Point(max_x, max_y)
])

point_geometry = [
    arcpy.PointGeometry(p, arcpy.SpatialReference(2180)) for p in points
]

arcpy.CopyFeatures_management(point_geometry, point_fc)

# Dodajemy atrybuty
arcpy.AddField_management(point_fc, "Typ", "TEXT", field_length=10)
arcpy.AddField_management(point_fc, "Wartosc", "DOUBLE")

with arcpy.da.UpdateCursor(point_fc, ["Typ", "Wartosc", "SHAPE@XY"]) as cur:
    for i, row in enumerate(cur):
        if i == 0:
            row[0] = "Minimum"
            row[1] = min_val
        else:
            row[0] = "Maksimum"
            row[1] = max_val
        cur.updateRow(row)

print(f"Punkty min i max zapisane do: {point_fc}")

# === Przykład modyfikacji rastra (jeśli nadal chcesz) ===
# R_array[100:200, 100:500] = 100
# outR = arcpy.NumPyArrayToRaster(R_array, lower_left, cell_size, value_to_nodata=R.noDataValue)
# outR.save("NowyRaster03.tif")

print("\nKONIEC – wszystko poszło dobrze!")