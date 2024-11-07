import re
import datetime
from dateutil.relativedelta import relativedelta

guess = 'September 2021 to December 2021'

def remove(string):
    pattern = re.compile(r'\s+')
    masterString = string.replace('’', "'")
    return re.sub(pattern, '', masterString).lower()


def extract_start_end_date(date_string):
    print(f'Iteration {date_string}')
    date_pointer = re.split(' to| to till| till|-|–| ­ |\s{3,}', date_string,maxsplit=1)
    start_date, end_date = "", ""
    for index, each_Date in enumerate(date_pointer):
        if index == 1 and remove(each_Date) == 'till' or remove(each_Date) == 'present' or remove(
                each_Date) == 'current' or remove(each_Date) == 'tilldate' or remove(each_Date) == 'now':
            each_Date = "Nov 2021"
        try:
            v  = removeDatesForExp([each_Date])
            myDate = guess_date_format(v,index)
            if index == 0:
                start_date = myDate
            else:
                end_date = myDate
        except:
            print(f'unable to get date for {each_Date}')
    if end_date == "":
        end_date = start_date
    temp_tuple = (start_date, end_date)
    return temp_tuple

#m - 05
#b - Jul
#B - July
#y -18
#Y - 2018


def guess_date_format(forDate,index):
    currentIteration = str(forDate[0])
    if currentIteration.__contains__('September'.casefold()):
        currentIteration = currentIteration.replace('Sept', 'sep')
    date_patterns = ['%d%B%Y','%d%B%y','%Y','%m%y','%b%y','%B%y','%m%Y','%b%Y','%B%Y',]
    for pattern in date_patterns:
        try:
            date = datetime.datetime.strptime(currentIteration, pattern).date()
            if index == 1:
                date += relativedelta(days=29)
            return date

        except Exception as e:
            print(f'{e} IS exception')

def removeDatesForExp(fromArray):
    filteredDates =[]
    for eachDate in fromArray:
        val = ''.join(e for e in str(eachDate) if e.isalnum())
        filteredDates.append(val)
    return filteredDates


# val = extract_start_end_date(guess)
# print(val)
