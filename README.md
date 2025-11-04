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

## Wymagania

| Narzędzie | Wersja |
|---------|--------|
| **ArcGIS Pro** | 2.9+ (z modułem ArcPy) |
| **Python** | 3.9+ (wbudowany w ArcGIS Pro) |
| **Biblioteki** | `arcpy`, `matplotlib`, `os`, `shutil` |

> `matplotlib` musi być zainstalowany w środowisku Pythona ArcGIS Pro.

---

## Struktura projektu
