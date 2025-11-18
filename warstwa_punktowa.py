import arcpy


# === USTAWIENIA ŚRODOWISKA ===
arcpy.env.workspace = r"D:\GIS\Rok_2025_26\PPA_ArcGIS\PPA_Gr1.gdb"

with arcpy.da.SearchCursor(fc, ['OID@', 'SHAPE@AREA']) as cursor:

