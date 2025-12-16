import arcpy


# === USTAWIENIA ŚRODOWISKA ===
arcpy.env.workspace = r"D:\GIS\Rok_2025_26\PPA_ArcGIS\Geobaza ZTM\ZTM197.gdb"
warstwa_liniowa = "ZTM_195"

# === FUNKCJE DLA WARSTWY PUNKTOWEJ ===
def odczytywanie_wspolrzednych(warstwa):
    lista_ob = []
    with arcpy.da.SearchCursor(warstwa, ['SHAPE@']) as cursor:
        for row in cursor:
            lista_wsp = []
            for part in row[0]:
                for pnt in part:
                    lista_wsp.append([pnt.X, pnt.Y])
            lista_ob.append(lista_wsp)
    return lista_ob


Wsp_Linie = odczytywanie_wspolrzednych(warstwa_liniowa)

print(Wsp_Linie)


print("KONIEC")