import arcpy


# === USTAWIENIA ŚRODOWISKA ===
arcpy.env.workspace = r"D:\GIS\Rok_2025_26\PPA_ArcGIS\PPA_Gr1.gdb"
warstwa_poligonowa = "Budynek"

# === FUNKCJE DLA WARSTWY PUNKTOWEJ ===
### [Poligon1[granica[pkt1[x1, y1], [x2, y2]...], dziure[pkt1[x1, y1]...], Poligon2[...], ...]
def odczytywanie_wspolrzednych_poligonu(warstwa):
    lista_ob = []
    with arcpy.da.SearchCursor(warstwa, ['SHAPE@']) as cursor:
        for row in cursor:
            lista_part = []
            for part in row[0]:
                lista_wsp = []
                for pnt in part:
                    if pnt:
                        # print(pnt)
                        lista_wsp.append([pnt.X, pnt.Y])
                    else:
                        lista_part.append(lista_wsp)
                        lista_wsp = []
                lista_part.append(lista_wsp)
            lista_ob.append(lista_part)
    return lista_ob

listaPOLIGON = odczytywanie_wspolrzednych_poligonu(warstwa_poligonowa)
print(listaPOLIGON)




print("KONIEC")