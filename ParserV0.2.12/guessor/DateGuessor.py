from guessor import *
from dateutil.relativedelta import relativedelta


def guess_date_format(fromArray):
    all_dates = []
    for each_date in fromArray:
        all_dates.append(extract_start_end_date(str(each_date)))  # Returns start and end date in tuple format.
    print(all_dates.reverse())
    return calculate_gap_period(all_dates)

def calculate_exp_years(fromArray):
    all_dates = []
    for each_date in fromArray:
        all_dates.append(extract_start_end_date(f'{each_date}'))  # Returns start and end date in tuple format.
    exp = 0
    for each_tuple in all_dates:
        start_date = each_tuple[0]
        end_date = each_tuple[1]
        try:
            exp += (end_date - start_date).days
        except:
            exp += 0
    return exp




def calculate_gap_period(inArray):
    cursor = 0
    days = 0
    for index, value in enumerate(inArray):
        cursor += 1
        if cursor > len(inArray) - 1:
            total_months = days/30
            if total_months < 0:
                return 0
            else:
                return total_months
        one = (inArray[index])[1]
        two = inArray[cursor][0]
        try:
            differenceDates = (two - one).days
            if differenceDates > 0:
                days += differenceDates
            print(f'days are {days}')
        except: return 0


def removeDatesWithOutMonths(fromArray):
    filteredDates =[]
    for eachDate in fromArray:
        val = ''.join(e for e in str(eachDate) if e.isalnum())
        if not val.isdigit():
            filteredDates.append(eachDate)
    return filteredDates




