from delphi_epidata import Epidata
import pprint as pp
import xlsxwriter
import datetime
import utils


# res = Epidata.covidcast('doctor-visits', 'smoothed_adj_cli', 'day', 'state',  Epidata.range(20200510, 20200520), 'CT')
# print(res['result'], res['message'], len(res['epidata']))
# pp.pprint(res)

# dataIwant = res['epidata'][5]['value']
# print(dataIwant)

states = ['AK', 'AL', 'AR', 'AS', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA', 'GU', 'HI', 'IA', 'ID', 'IL', 'IN',
          'KS', 'KY', 'LA', 'MA', 'MD', 'ME', 'MI', 'MN', 'MO', 'MP', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM',
          'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'PR', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VA', 'VI', 'VT', 'WA', 'WI',
          'WV', 'WY']

signalsDict = {
    "doctor-visits": "smoothed_adj_cli",
    # "fb-survey": "smoothed_hh_cmnty_cli",
    "fb-survey": "smoothed_cli",
    "google-survey": "smoothed_cli",
    "ght": "smoothed_search"
}

def genDates(start, noDays):
    dates = []
    dates.append(start)
    timeDelta = datetime.timedelta(days = 1)
    for n in range(noDays):
        start += timeDelta
        dates.append(start)
    return dates

start = datetime.datetime(2020, 2, 1)
dates = genDates(start, 117)

def getStateFromCode(stateCode):
    us_state_abbrev = {
        'Alabama': 'AL',
        'Alaska': 'AK',
        'American Samoa': 'AS',
        'Arizona': 'AZ',
        'Arkansas': 'AR',
        'California': 'CA',
        'Colorado': 'CO',
        'Connecticut': 'CT',
        'Delaware': 'DE',
        'District of Columbia': 'DC',
        'Florida': 'FL',
        'Georgia': 'GA',
        'Guam': 'GU',
        'Hawaii': 'HI',
        'Idaho': 'ID',
        'Illinois': 'IL',
        'Indiana': 'IN',
        'Iowa': 'IA',
        'Kansas': 'KS',
        'Kentucky': 'KY',
        'Louisiana': 'LA',
        'Maine': 'ME',
        'Maryland': 'MD',
        'Massachusetts': 'MA',
        'Michigan': 'MI',
        'Minnesota': 'MN',
        'Mississippi': 'MS',
        'Missouri': 'MO',
        'Montana': 'MT',
        'Nebraska': 'NE',
        'Nevada': 'NV',
        'New Hampshire': 'NH',
        'New Jersey': 'NJ',
        'New Mexico': 'NM',
        'New York': 'NY',
        'North Carolina': 'NC',
        'North Dakota': 'ND',
        'Northern Mariana Islands': 'MP',
        'Ohio': 'OH',
        'Oklahoma': 'OK',
        'Oregon': 'OR',
        'Pennsylvania': 'PA',
        'Puerto Rico': 'PR',
        'Rhode Island': 'RI',
        'South Carolina': 'SC',
        'South Dakota': 'SD',
        'Tennessee': 'TN',
        'Texas': 'TX',
        'Utah': 'UT',
        'Vermont': 'VT',
        'Virgin Islands': 'VI',
        'Virginia': 'VA',
        'Washington': 'WA',
        'West Virginia': 'WV',
        'Wisconsin': 'WI',
        'Wyoming': 'WY'
    }

    # thank you to @kinghelix and @trevormarburger for this idea
    abbrev_us_state = dict(map(reversed, us_state_abbrev.items()))

    return abbrev_us_state[stateCode]


whatReading = input("what are we reading?: ")
# whatReading = "test"
def openWorksheet(name):
    workbook = xlsxwriter.Workbook(name + '.xlsx')
    worksheet = workbook.add_worksheet()
    return worksheet, workbook

worksheet, workbook = openWorksheet(whatReading)
metAreas, metCodesDict = utils.getMetCodes()

def prepWorksheet(worksheet, dates):
    for i, state in enumerate(states):
        worksheet.write(0, i+1, getStateFromCode(state))
    for d, date in enumerate(dates):
        worksheet.write(d+1, 0, date.strftime("%d %m %Y"))

# prepWorksheet(worksheet, dates)

# print(len(metAreas))
def prepWorksheetMetCodes(worksheet, dates):
    for i, metArea in enumerate(metAreas):
        worksheet.write(0, i + 1, metArea)
    for d, date in enumerate(dates):
        worksheet.write(d + 1, 0, date.strftime("%d %m %Y"))

prepWorksheetMetCodes(worksheet, dates)
def getDataForStates(state, type):
    res = Epidata.covidcast(type, signalsDict[type], 'day', 'state', Epidata.range(20200201, 20200528),
                            state)

    # print(datetime.datetime.strptime(str(res['epidata'][0]['time_value']), '%Y%m%d'))
    return res['epidata']

def getDataForMetAreas(metCode, type):
    res = Epidata.covidcast(type, signalsDict[type], 'day', 'msa', Epidata.range(20200201, 20200528),
                            metCode)

    # print(datetime.datetime.strptime(str(res['epidata'][0]['time_value']), '%Y%m%d'))
    return res['epidata']




def buildUpExcel(worksheet):
    offset = 0
    # for i, state in enumerate(states):
    for i, metArea in enumerate(metAreas):
        try:
            # res = getDataForStates(state, whatReading)
            res = getDataForMetAreas(metCodesDict[metArea], whatReading)
            dataList = res
            for n, data in enumerate(dataList):
                if n == 0:
                    startDate = datetime.datetime.strptime(str(res[0]['time_value']), '%Y%m%d')
                    difference = startDate - datetime.datetime(2020, 2, 1)
                    offset = difference.days
                    # print(offset)
                worksheet.write(n + 1+offset, i + 1, data['value'])
            print(metCodesDict[metArea], " worked!")
        except:
            print(metCodesDict[metArea])
            # print(state)


buildUpExcel(worksheet)
# signals = ['raw_cli', 'raw_ili', 'raw_wcli', 'raw_wili', 'raw_hh_cmnty_cli', 'raw_nohh_cmnty_cli', 'smoothed_cli']
# for sig in signals:
#     print(getData('FL', sig)[-1])
# for i, metArea in enumerate(metAreas):
#     print(metArea, getDataForMetAreas(metCodesDict[metArea], "fb-survey"))
workbook.close()









