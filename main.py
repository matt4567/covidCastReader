import datetime
import covidCastReader
import utils
def getDataFromCovidCast():
    dataToPull = ['doctor-visitsState', 'fb-surveyState', 'fb-survey-communityState', 'ghtState', 'doctor-visitsMetro', 'fb-surveyMetro']
    address = ['doctor-visits', 'fb-survey', 'fb-survey', 'ght', 'doctor-visits', 'fb-survey']
    signal = ['smoothed_adj_cli', 'smoothed_cli', 'smoothed_hh_cmnty_cli', 'smoothed_search', 'smoothed_adj_cli', 'smoothed_cli']
    location = ['state', 'state', 'state', 'state', 'metro', 'metro']

    start = datetime.datetime(2020, 2, 1)
    nowInt = int(datetime.datetime.now().strftime("%Y%m%d"))
    numDays = (datetime.datetime.now() - start).days
    dates = covidCastReader.genDates(start, numDays)
    metAreas, metCodesDict = utils.getMetCodes()
    for i, data in enumerate(dataToPull):
        if i != 2: continue
        worksheet, workbook = covidCastReader.openWorksheet(data)
        if (location[i] == 'state'):
            covidCastReader.prepWorksheet(worksheet, dates)
            print(address[i], nowInt, signal[i])
            covidCastReader.buildUpExcelForStates(worksheet, address[i], nowInt, signal[i])
        else:
            covidCastReader.prepWorksheetMetCodes(worksheet, dates)
            # print(address[i], nowInt, signal[i])
            covidCastReader.buildUpExcelForMetro(worksheet, address[i], nowInt, signal[i])

        workbook.close()

getDataFromCovidCast()


