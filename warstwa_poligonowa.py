import arcpy


# === USTAWIENIA ŚRODOWISKA ===
arcpy.env.workspace = r"D:\GIS\Rok_2025_26\PPA_ArcGIS\PPA_Gr1.gdb"
warstwa_poligonowa = "Budynki"

# === FUNKCJE DLA WARSTWY PUNKTOWEJ ===
### [Poligon1[granica[pkt1[x1, y1], [x2, y2]...], dziure[pkt1[x1, y1]...], Poligon2[...], ...]
def odczytywanie_wspolrzednych_poligonu(warstwa):
    lista_ob = []
    lista_centr = []
    with arcpy.da.SearchCursor(warstwa, ['SHAPE@', "SHAPE@XY"]) as cursor:
        for row in cursor:
            lista_centr.append(row[1])
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
    return lista_ob, lista_centr

def wstawianie_wspolrzednych_poligonu(warstwa, lista_ob):
    with arcpy.da.InsertCursor(warstwa, ['SHAPE@']) as cursor:
        pnt = arcpy.Point()
        array = arcpy.Array()
        part = arcpy.Array()
        for ob in lista_ob:
            for cze in ob:
                for pkt in cze:
                    pnt.X = pkt[0]
                    pnt.Y = pkt[1]
                    part.add(pnt)
                array.add(part)
                part.removeAll()
            poly = arcpy.Polygon(array)
            array.removeAll()
            cursor.insertRow([poly])

listaPOLIGON, listaCENTROID = odczytywanie_wspolrzednych_poligonu(warstwa_poligonowa)
print(listaPOLIGON)

i = 0
for ob in listaPOLIGON:
    for part in ob:
        for pkt in part:
            pkt[0] = (pkt[0]-listaCENTROID[i][0])*0.5 + listaCENTROID[i][0]
            pkt[1] = (pkt[1]-listaCENTROID[i][1])*0.5 + listaCENTROID[i][1]
    i += 1


Nowe_budynki = "Bydynki01"
arcpy.management.CreateFeatureclass(arcpy.env.workspace, Nowe_budynki, "POLYGON", "", "DISABLED", "DISABLED", warstwa_poligonowa)
wstawianie_wspolrzednych_poligonu(Nowe_budynki, listaPOLIGON)

print("KONIEC")