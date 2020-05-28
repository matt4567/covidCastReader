import csv
import pandas as pd
import xlrd

# def getMetCodes():
#     metAreas = []
#     metAreaDict = {}
#     with open('codes.csv') as csvfile:
#         codeReader = csv.reader(csvfile, delimiter = ',')
#         for row in codeReader:
#             if (row[6] == "NAMELSAD"):continue
#             metAreas.append(row[6])
#             metAreaDict[row[6]] = row[4]
#     return metAreas, metAreaDict

# metAreas, metAreaDict = getMetCodes()
#
# print(metAreas)
# print(metAreaDict["New York County"])

def getMetCodes():
    codeSet = {"set"}
    metAreas = []
    metAreasDict = {}
    loc = ("codes.xls")

    # To open Workbook
    wb = xlrd.open_workbook(loc)
    sheet = wb.sheet_by_index(0)

    for i in range(3, sheet.nrows):
        if sheet.cell_value(i, 0) in codeSet: continue
        else:
            codeSet.add(sheet.cell_value(i, 0))
            metAreas.append(sheet.cell_value(i, 3))
            metAreasDict[sheet.cell_value(i, 3)] = sheet.cell_value(i, 0)

    return metAreas, metAreasDict


# print(getMetCodes()[0])