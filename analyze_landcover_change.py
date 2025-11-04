# -*- coding: utf-8 -*-
"""
Analiza zmian pokrycia terenu między dwoma warstwami (2014 i 2020)
- Scalanie warstw
- Obliczanie przecięcia (Intersect)
- Analiza zmian klas pokrycia terenu
- Wykresy: udział zmian i szczegółowe typy zmian
"""

import arcpy
import matplotlib.pyplot as plt
from collections import defaultdict
import os

# === USTAWIENIA ŚRODOWISKA ===
arcpy.env.workspace = r"D:\GIS\Rok_2025_26\PPA_ArcGIS\PPA_Gr1.gdb"
# arcpy.env.overwriteOutput = True  # Nadpisuj istniejące warstwy

# Sprawdź, czy GDB istnieje
if not arcpy.Exists(arcpy.env.workspace):
    raise FileNotFoundError(f"Nie znaleziono geobazy danych: {arcpy.env.workspace}")

print("Środowisko ArcPy skonfigurowane.")

# === KROK 1: Wybór warstw wejściowych ===
featureclasses = arcpy.ListFeatureClasses()

input_lay_2014 = []
input_lay_2020 = []

print("\nWyszukiwanie warstw pokrycia terenu...")
for fc in featureclasses:
    if "OT_PT" in fc:
        if "2014" in fc:
            input_lay_2014.append(fc)
            print(f"Znaleziono warstwę 2014: {fc}")
        elif "2020" in fc:
            input_lay_2020.append(fc)
            print(f"Znaleziono warstwę 2020: {fc}")

# Sprawdzenie, czy warstwy istnieją
if not input_lay_2014:
    raise ValueError("Nie znaleziono warstw z 2014 rokiem (GDA2020 + OT_PT + 2014)")
if not input_lay_2020:
    raise ValueError("Nie znaleziono warstw z 2020 rokiem (GDA2020 + OT_PT + 2020)")

# === KROK 2: Scalanie warstw (Merge) ===
out2014 = "PT_2014"
out2020 = "PT_2020"

# Funkcja pomocnicza: sprawdź i utwórz warstwę
def create_if_not_exists(input_layers, output_name, description=""):
    if arcpy.Exists(output_name):
        print(f"Warstwa istnieje: {output_name}")
    else:
        print(f"Tworzenie warstwy: {output_name}...")
        arcpy.management.Merge(input_layers, output_name)
        print(f"Utworzono: {output_name}")
    return output_name

# Tworzenie warstw scalonych
out2014 = create_if_not_exists(input_lay_2014, out2014, "Scalona warstwa PT 2014")
out2020 = create_if_not_exists(input_lay_2020, out2020, "Scalona warstwa PT 2020")

# === KROK 3: Przecięcie (Intersect) ===
inter = "PT_2014_2020"

if arcpy.Exists(inter):
    print(f"Warstwa przecięcia istnieje: {inter}")
else:
    print(f"Tworzenie warstwy przecięcia: {inter}...")
    arcpy.analysis.Intersect(
        in_features=[out2014, out2020],
        out_feature_class=inter,
        join_attributes="ALL",
        output_type="INPUT"
    )
    print(f"Utworzono: {inter}")

# Sprawdzenie, czy warstwa przecięcia ma rekordy
if int(arcpy.GetCount_management(inter)[0]) == 0:
    raise ValueError(f"Warstwa {inter} jest pusta! Sprawdź dane wejściowe.")

# === KROK 4: Analiza zmian pokrycia terenu ===
area_pary = defaultdict(float)  # Słownik: para kodów -> suma powierzchni zmian
area_all = 0.0                  # Całkowita powierzchnia przecięcia
area_change = 0.0               # Powierzchnia gdzie nastąpiła zmiana

print("\nAnaliza zmian pokrycia terenu...")
with arcpy.da.SearchCursor(inter, ["OID@", 'X_KOD', 'X_KOD_1', "SHAPE@AREA"]) as cursor:
    for row in cursor:
        oid, kod_2014, kod_2020, area = row
        area_all += area
        if kod_2014 != kod_2020:  # Zmiana klasy
            para = f"{kod_2014}-{kod_2020}"
            area_pary[para] += area
            area_change += area

# === KROK 5: Wyniki procentowe ===
if area_all > 0:
    proc_bez_zmian = ((area_all - area_change) / area_all) * 100
    proc_zmiany = (area_change / area_all) * 100
else:
    proc_bez_zmian = proc_zmiany = 0.0

print(f"\nUdział powierzchni bez zmian: {proc_bez_zmian:.2f}%")
print(f"Udział powierzchni ze zmianą: {proc_zmiany:.2f}%")
print(f"Liczba unikalnych typów zmian: {len(area_pary)}")

# === KROK 6: Przygotowanie danych do wykresu 2 (szczegółowe zmiany) ===
area_pary_sort = sorted(area_pary.items(), key=lambda x: x[1], reverse=True)
separator = 15  # Liczba największych zmian do wyświetlenia osobno
new_list = []
proc_inne = 0.0
i = 0

for kod, powierzchnia in area_pary_sort:
    proc_pow = (powierzchnia / area_change) * 100 if area_change > 0 else 0
    if i < separator:
        new_list.append([kod, proc_pow])
    else:
        proc_inne += proc_pow
    i += 1

if proc_inne > 0:
    new_list.append(["inne", proc_inne])

# === WYKRES 1: Kołowy - udział zmian vs bez zmian ===
plt.figure(figsize=(8, 8))
wartosci_pie = [proc_bez_zmian, proc_zmiany]
etykiety_pie = ['Bez zmian', 'Zmiany']
plt.pie(wartosci_pie, labels=etykiety_pie, autopct='%1.1f%%', startangle=90, colors=['#66c2a5', '#fc8d62'])
plt.axis('equal')
plt.title("Udział zmian pokrycia terenu (2014 → 2020) - WYKRES 1")
plt.tight_layout()
plt.show()

# === WYKRES 2: Słupkowy - szczegółowe typy zmian ===
wartosci_bar = [x[1] for x in new_list]
etykiety_bar = [x[0] for x in new_list]

plt.figure(figsize=(12, 7))
bars = plt.bar(etykiety_bar, wartosci_bar, color='#1f78b4', edgecolor='black', alpha=0.8)
plt.xlabel("Typ zmiany (kod 2014 → kod 2020)")
plt.ylabel("Udział w zmianach [%]")
plt.title(f"Najczęstsze zmiany pokrycia terenu (Top {separator} + inne) - WYKRES 2")
plt.xticks(rotation=90, ha='center')
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Dodanie wartości na słupkach
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2.0, height + 0.1,
             f'{height:.1f}%', ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.show()

print("\nKONIEC ANALIZY. Wykresy wygenerowane pomyślnie.")