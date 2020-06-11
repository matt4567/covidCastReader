import csv
import pandas as pd
import xlrd
import matplotlib.pyplot as plt
from delphi_epidata import Epidata

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

def getDataForStates(state, type):
    res = Epidata.covidcast(type, "smoothed_adj_cli", 'day', 'state', Epidata.range(20200523, 20200528),
                            state)

    # print(datetime.datetime.strptime(str(res['epidata'][0]['time_value']), '%Y%m%d'))
    return res['epidata']

# print(getDataForStates("FL", "doctor-visits"))

def openWorkbook(addr):
    wb = xlrd.open_workbook(addr)
    sheet = wb.sheet_by_index(0)
    return sheet

def returnFloatOrNegativeOne(sheet, x, y):
    try:
        return float(sheet.cell_value(x, y))
    except:
        return -1

def plotComparableDatasets():
    data1 = './08.06/doctor-visitsState.xlsx'
    data2 = './28.05/doctor-visitsState.xlsx'
    data3 = './01.06/doctor-visitsState.xlsx'
    fbData = './08.06/fb-surveyState.xlsx'

    sheet1 = openWorkbook(data1)
    sheet2 = openWorkbook(data2)
    sheet3 = openWorkbook(data3)
    fbSheet = openWorkbook(fbData)

    list1 = []
    list2 = []
    list3 = []
    fbList = []
    dates = []


    # dates.append(sheet1.cell_value(i, 0))
    dates = [sheet1.cell_value(i, 0) for i in range(1, sheet1.nrows)]
    # value1 = returnFloatOrNegativeOne(sheet1, i, 5)
    # if value1 != -1
    list1 = [returnFloatOrNegativeOne(sheet1, i, 5) for i in range(1, sheet1.nrows) if returnFloatOrNegativeOne(sheet1, i, 5) != -1]
    list2 = [returnFloatOrNegativeOne(sheet2, i, 5) for i in range(1, sheet2.nrows) if returnFloatOrNegativeOne(sheet2, i, 5) != -1]
    list3 = [returnFloatOrNegativeOne(sheet3, i, 5) for i in range(1, sheet3.nrows) if returnFloatOrNegativeOne(sheet3, i, 5) != -1]
    fbList = [returnFloatOrNegativeOne(fbSheet, i, 5) for i in range(66, fbSheet.nrows) if returnFloatOrNegativeOne(fbSheet, i, 5) != -1]

        # list1.append(returnFloatOrZero(sheet1, i, 5))
        # if i < sheet2.nrows:list2.append(returnFloatOrZero(sheet2, i, 5))
        # if i < sheet3.nrows:list3.append(returnFloatOrZero(sheet3, i, 5))


    plt.plot(dates[:len(list1)], list1, label = "data from 8th June")
    plt.plot(dates[:len(list2)], list2, label = "data from 28th May")
    plt.plot(dates[:len(list3)], list3, label = "data from 1st June")
    plt.plot(dates[66:66+len(fbList)], fbList, label="Facebook data from 8th June")
    plt.title("Arizona doctors visits pulled on 3 different dates")
    ticks = [x for x in range(len(dates)) if x % 10 == 0]
    plt.xticks(ticks, rotation = 45)
    plt.legend()
    plt.show()


# plotComparableDatasets()

