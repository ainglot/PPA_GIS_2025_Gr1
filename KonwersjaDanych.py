# -*- coding: utf-8 -*-
"""
Skrypt: Importowanie plików SHP z folderu do geobazy danych (GDB)
1. Kopiowanie i czyszczenie nazw plików SHP (z kropkami na podkreślenia)
2. Eksportowanie plików SHP do GDB jako warstwy z prefiksem "GDA2014_"
3. Sprawdzanie istnienia folderów, plików i warstw w GDB
"""

import arcpy
import os
import shutil

# === USTAWIENIA ŚCIEŻEK ===
folder_SHP = r"D:\GIS\Rok_2025_26\PPA_ArcGIS\2261_SHP_2014"
folder_new_SHP = r"D:\GIS\Rok_2025_26\PPA_ArcGIS\new_2261_SHP_2014"
gdb_path = r"D:\GIS\Rok_2025_26\PPA_ArcGIS\PPA_Gr1.gdb"
rocznik = "2014"

arcpy.env.workspace = gdb_path
# arcpy.env.overwriteOutput = True  # Zezwalaj na nadpisywanie w GDB

# === KROK 0: SPRAWDZENIE ISTNIENIA FOLDERÓW I GDB ===
def check_path(path, path_type="folder"):
    """Sprawdza, czy ścieżka istnieje. Jeśli nie — tworzy (dla folderów) lub zgłasza błąd."""
    if not os.path.exists(path):
        if path_type == "folder":
            print(f"Folder nie istnieje: {path}")
            print(f"Tworzenie folderu...")
            os.makedirs(path)
            print(f"Utworzono: {path}")
        else:
            raise FileNotFoundError(f"Nie znaleziono: {path}")
    else:
        print(f"{path_type.capitalize()} istnieje: {path}")

# Sprawdzenie folderów
check_path(folder_SHP, "folder")
check_path(folder_new_SHP, "folder")
check_path(gdb_path, "geobaza danych")

# Sprawdzenie, czy GDB jest dostępna dla ArcPy
if not arcpy.Exists(gdb_path):
    raise EnvironmentError(f"Geobaza danych nie jest dostępna dla ArcPy: {gdb_path}")

print("\nŚrodowisko skonfigurowane poprawnie.\n")

# === KROK 1: KOPIOWANIE I CZYSZCZENIE NAZW PLIKÓW SHP ===
print("Krok 1: Kopiowanie i czyszczenie nazw plików SHP...")

copied_count = 0
for file in os.listdir(folder_SHP):
    file_path = os.path.join(folder_SHP, file)
    if os.path.isfile(file_path):
        name, ext = os.path.splitext(file)
        
        # POMIJAJ PLIKI TYMCZASOWE (locki ArcGIS, indeksy, itp.)
        if ext.lower() in (".lock", ".sr.lock"):
            print(f"Pominięto plik pomocniczy: {file}")
            continue
        
        # Zamiana kropek na podkreślenia (np. "plik.1.shp" → "plik_1.shp")
        new_name = name.replace(".", "_") + ext
        src = file_path
        dst = os.path.join(folder_new_SHP, new_name)
        
        # Kopiuj tylko jeśli nie istnieje lub jest nowszy
        if not os.path.exists(dst) or os.path.getmtime(src) > os.path.getmtime(dst):
            try:
                shutil.copy2(src, dst)
                print(f"Skopiowano: {file} → {new_name}")
                copied_count += 1
            except PermissionError as pe:
                print(f"PermissionError – pominięto plik tymczasowy/zablokowany: {file}")
                print(f"  Szczegóły: {pe}")
                continue  # Pomija tylko ten plik
            except Exception as e:
                print(f"Nieoczekiwany błąd przy kopiowaniu {file}: {e}")
                continue
        else:
            print(f"Pominięto (już istnieje): {new_name}")

if copied_count == 0:
    print("Brak nowych plików SHP do skopiowania.")
else:
    print(f"Skopiowano {copied_count} plików SHP.\n")

# === KROK 2: IMPORT DO GDB Z SPRAWDZENIEM ISTNIENIA WARSTW ===
print("Krok 2: Eksportowanie plików SHP do geobazy danych...")

exported_count = 0
skipped_count = 0

for file in os.listdir(folder_new_SHP):
    file_path = os.path.join(folder_new_SHP, file)
    name, ext = os.path.splitext(file)

    if ext.lower() == ".shp" and os.path.isfile(file_path):
        # Nazwa warstwy: "GDA2014_nazwa_po_podwójnym_podkreśleniu"
        if "__" in name:
            new_name = name.split("__")[1]
        else:
            new_name = name  # fallback

        output_feature_class = f"GDA{rocznik}_" + new_name

        # Sprawdzenie, czy warstwa już istnieje w GDB
        if arcpy.Exists(output_feature_class):
            print(f"Pominięto (już istnieje w GDB): {output_feature_class}")
            skipped_count += 1
            continue

        # Eksport do GDB
        try:
            print(f"Eksportuję: {file} → {output_feature_class}")
            arcpy.conversion.ExportFeatures(
                in_features=file_path,
                out_features=output_feature_class
            )
            print(f"Utworzono warstwę: {output_feature_class}")
            exported_count += 1
        except arcpy.ExecuteError:
            print(f"BŁĄD ArcPy przy eksporcie {file}:")
            print(arcpy.GetMessages())
        except Exception as e:
            print(f"Nieoczekiwany błąd przy {file}: {str(e)}")

# === PODSUMOWANIE ===
print("\n" + "="*50)
print("PODSUMOWANIE:")
print(f"  Skopiowano plików SHP: {copied_count}")
print(f"  Eksportowano do GDB: {exported_count}")
print(f"  Pominięto (już istnieje): {skipped_count}")
print("="*50)
print("KONIEC SKRYPTU")