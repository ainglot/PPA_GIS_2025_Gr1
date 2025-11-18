# Analiza Zmian Pokrycia Terenu (2014 → 2020) – PPA ArcGIS

Projekt zawiera dwa skrypty Pythona do przetwarzania danych przestrzennych w formacie SHP i analizy zmian pokrycia terenu z wykorzystaniem **ArcGIS Pro / ArcPy**.

---

## Skrypt 1: `import_shp_to_gdb.py`
### Importowanie plików SHP do geobazy danych (GDB)

**Cel:**  
Kopiowanie plików `.shp` z folderu, czyszczenie nazw (kropki → podkreślenia), eksport do GDB z prefiksem `GDA2014_`.

**Funkcjonalności:**
- Sprawdzenie istnienia folderów i GDB
- Pomijanie plików tymczasowych (`.lock`, indeksy)
- Kopiowanie tylko nowych/nowszych plików
- Eksport do GDB jako warstwy `Feature Class`
- Zabezpieczenie przed nadpisywaniem istniejących warstw

---

## Skrypt 2: `analyze_landcover_change.py`
### Analiza zmian pokrycia terenu (2014 vs 2020)

**Cel:**  
Porównanie warstw `OT_PT` z lat 2014 i 2020, wykrycie zmian klas pokrycia terenu, generowanie wykresów.

**Funkcjonalności:**
- Automatyczne wyszukiwanie warstw `OT_PT` z `2014` i `2020`
- Scalanie warstw (Merge)
- Przecięcie (Intersect)
- Obliczenie powierzchni zmian
- Dwa wykresy:
  1. **Kołowy** – udział zmian vs brak zmian
  2. **Słupkowy** – top 15 typów zmian + "inne"

---

## Skrypts: `warstwa_punktowa.py`
### Przetwarzanie chmury punktów 3D (LiDAR) – analiza i generalizacja pionowa silosu

**Cel:**  
Automatyczne przetworzenie pełnej chmury punktów 3D (plik tekstowy `.txt`) reprezentującej skanowanie silosu zbożowego, a następnie wygenerowanie uogólnionej warstwy punktowej zawierającej średnie współrzędne XY dla kolejnych poziomów wysokościowych (co 2 metry).

**Główne funkcjonalności:**

- Wczytywanie współrzędnych X, Y, Z z pliku tekstowego (`data.txt`)
- Przesunięcie współrzędnych do lokalnego układu (dodanie offsetu +470856 / +741111)
- Grupowanie punktów w poziome warstwy wysokościowe co **2 metry**
- Obliczenie średnich współrzędnych X i Y dla każdego przedziału wysokościowego
- Zapis średniego punktu (X_śr, Y_śr, Z_środek_przedziału) do nowej warstwy punktowej w geobazie
- Dodanie atrybutu `wsp_z` zawierającego wysokość środka przedziału

**Dodatkowe funkcje pomocnicze (zakomentowane w kodzie):**
- Odczytywanie współrzędnych z istniejącej warstwy punktowej
- Przesunięcie wszystkich punktów o stałą wartość (+100 m w X i Y)
- Tworzenie podzbioru N najbliższych punktów do geometrycznego środka chmury
- Eksport wybranej liczby punktów (np. 150 pierwszych lub 150 najbliższych środka)

**Wynik końcowy:**
Warstwa punktowa `Silos04` (lub inna nazwa podana w zmiennej `nowa_warstwa`) zawierająca po jednym punkcie na każdy 2-metrowy poziom wysokości silosu – idealna do dalszej analizy przekroju pionowego, modelowania 3D lub wizualizacji warstw materiału.

**Przykładowe zastosowanie:**
- Ocena kształtu i objętości zasypu zboża w silosie
- Wykrywanie deformacji ścian
- Tworzenie uproszczonego modelu 3D silosu na podstawie skanów LiDAR

---

## Wymagania

| Narzędzie | Wersja |
|---------|--------|
| **ArcGIS Pro** | 3.5.2 (z modułem ArcPy) |
| **Python** | 3.11.11 (wbudowany w ArcGIS Pro) |
| **Biblioteki** | `arcpy`, `matplotlib`, `os`, `shutil` |

> `matplotlib` musi być zainstalowany w środowisku Pythona ArcGIS Pro.

---

## Struktura projektu
