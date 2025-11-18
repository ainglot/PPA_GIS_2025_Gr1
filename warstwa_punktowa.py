import arcpy


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
lista_wybranych = odczytywanie_wspolrzednych(warstwa_punktowa)[:150]
print(lista_wybranych)

### Tworzenie pustej warstwy
nowa_warstwa = "GDA2020_OT_OIPR_P_150pierwszych"
arcpy.management.CreateFeatureclass(arcpy.env.workspace, nowa_warstwa, "POINT", "", "DISABLED", "DISABLED", warstwa_punktowa)
wstawianie_wspolrzednych(nowa_warstwa, lista_wybranych)
# aktualizowanie_wspolrzednych(warstwa_punktowa)

print("KONIEC")