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
nodata_val = np.nan  # w Twoim pliku ASC NoData to zazwyczaj -9999 albo inna wartość – sprawdź!

# === KONWERSJA DO NUMPY ===
# Używamy nodata_to_value tylko jeśli naprawdę chcesz zamienić NoData na 0
# Lepiej zachować oryginalne NoData, więc najczęściej wystarczy:
R_array = arcpy.RasterToNumPyArray(R, nodata_to_value = nodata_val)  # bez parametru nodata_to_value

# === MIN i MAX z ignorowaniem np.nan ===
min_val = np.nanmin(R_array)
max_val = np.nanmax(R_array)

# Pozycje (wiersz, kolumna) – liczone od lewego GÓRNEGO rogu!
min_row, min_col = np.unravel_index(np.nanargmin(R_array), R_array.shape)
max_row, max_col = np.unravel_index(np.nanargmax(R_array), R_array.shape)

# === Przeliczenie indeksów na współrzędne X,Y (środek komórki) ===
def array_to_xy(row, col, lower_left_corner, cell_size, rows_total):
    x = lower_left_corner.X + col * cell_size + cell_size / 2.0
    # Odwracamy wiersz: NumPy zaczyna od góry, raster od dołu
    y = lower_left_corner.Y + (rows_total - 1 - row) * cell_size + cell_size / 2.0
    return x, y

rows_total = R_array.shape[0]

min_x, min_y = array_to_xy(min_row, min_col, lower_left, cell_size, rows_total)
max_x, max_y = array_to_xy(max_row, max_col, lower_left, cell_size, rows_total)

# === WYNIK ===
print("\n" + "="*65)
print(f"MINIMUM: {min_val:.3f} m n.p.m.")
print(f"   → X = {min_x:.3f}, Y = {min_y:.3f} (układ 2180)")
print(f"   → wiersz: {min_row}, kolumna: {min_col}")

print(f"MAKSYMUM: {max_val:.3f} m n.p.m.")
print(f"   → X = {max_x:.3f}, Y = {max_y:.3f} (układ 2180)")
print(f"   → wiersz: {max_row}, kolumna: {max_col}")
print("="*65)

print("\nKONIEC – wszystko poszło dobrze!")