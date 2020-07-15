import datetime
import covidCastReader
import utils
def getDataFromCovidCast():
    # dataToPull = ['doctor-visitsState', 'fb-surveyState', 'fb-survey-communityState', 'ghtState', 'doctor-visitsMetro', 'fb-surveyMetro']
    dataToPull = ['doctor-visitsState', 'fb-surveyState', 'fb-survey-communityState', 'away6+hours', 'away3-6hours', 'hospital-admissions']


    # address = ['doctor-visits', 'fb-survey', 'fb-survey', 'ght', 'doctor-visits', 'fb-survey']
    address = ['doctor-visits', 'fb-survey', 'fb-survey', 'safegraph', 'safegraph', 'hospital-admissions']

    # signal = ['raw_cli', 'raw_cli', 'raw_hh_cmnty_cli', 'raw_search', 'raw_adj_cli', 'raw_cli']
    # signal = ['smoothed_adj_cli', 'smoothed_cli', 'smoothed_hh_cmnty_cli', 'smoothed_search', 'smoothed_adj_cli', 'smoothed_cli']
    signal = ['smoothed_adj_cli', 'smoothed_cli', 'smoothed_hh_cmnty_cli', 'full_time_work_prop', 'part_time_work_prop', 'smoothed_adj_covid19']

    # location = ['state', 'state', 'state', 'state', 'metro', 'metro']
    location = ['state', 'state', 'state', 'state', 'state', 'state']

    start = datetime.datetime(2020, 2, 1)
    nowInt = int(datetime.datetime.now().strftime("%Y%m%d"))
    numDays = (datetime.datetime.now() - start).days
    dates = covidCastReader.genDates(start, numDays)
    metAreas, metCodesDict = utils.getMetCodes()
    for i, data in enumerate(dataToPull):
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


