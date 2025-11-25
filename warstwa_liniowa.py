import arcpy


# === USTAWIENIA ŚRODOWISKA ===
arcpy.env.workspace = r"D:\GIS\Rok_2025_26\PPA_ArcGIS\PPA_Gr1.gdb"
warstwa_liniowa = "GDA2020_OT_SWRS_L"

# === FUNKCJE DLA WARSTWY PUNKTOWEJ ===
def odczytywanie_wspolrzednych(warstwa):
    lista_wsp = []
    with arcpy.da.SearchCursor(warstwa, ['SHAPE@X', 'SHAPE@Y']) as cursor:
        for row in cursor:
            lista_wsp.append(row)
    return lista_wsp

lista_wsp = odczytywanie_wspolrzednych(warstwa_liniowa)

print("KONIEC")