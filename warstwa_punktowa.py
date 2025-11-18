import arcpy


# === USTAWIENIA ŚRODOWISKA ===
arcpy.env.workspace = r"D:\GIS\Rok_2025_26\PPA_ArcGIS\PPA_Gr1.gdb"
warstwa_punktowa = "GDA2020_OT_OIPR_P"

def odczytywanie_wspolrzednych(warstwa):
    lista_wsp = []
    with arcpy.da.SearchCursor(warstwa_punktowa, ['SHAPE@X', 'SHAPE@Y']) as cursor:
        for row in cursor:
            lista_wsp.append([row])
    return lista_wsp

print(odczytywanie_wspolrzednych(warstwa_punktowa)[:50])

print("KONIEC")