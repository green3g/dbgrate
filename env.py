from os.path import join

DB_CONNECTION = 'gisdata.sde'
import arcpy
arcpy.env.overwriteOutput = True
if not arcpy.Exists(join(arcpy.env.scratchFolder, DB_CONNECTION)):
    arcpy.CreateDatabaseConnection_management(
        arcpy.env.scratchFolder,
        DB_CONNECTION,
        'POSTGRESQL',
        'gisdata.wsbeng.com',
        'DATABASE_AUTH',
        'dbo',
        'secret',
        'SAVE_USERNAME',
        'wsb_inspect_sde',
        'dbo'
    )
arcpy.env.workspace = '{}/gisdata.sde'.format(arcpy.env.scratchFolder)