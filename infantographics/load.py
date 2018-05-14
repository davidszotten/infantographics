from datetime import datetime
import csv

import xlrd


def parse_row(row):
    datetime_str = '{Date} {Start}'.format(**row)
    # export contains malformed am/pm times (e.g. "00:01 am")
    datetime_str = datetime_str.replace('00:', '12:')
    start = datetime_str
    start = datetime.strptime(datetime_str, '%m-%d-%Y %I:%M %p')
    duration = int(row['Duration [min]'])
    return (start, duration)


def load_csv(file_handle):
    reader = csv.DictReader(file_handle)
    data = list(reader)
    entries = []
    for row in data:
        start, duration = parse_row(row)
        entries.append({
            'duration': duration,
            'start': start,
        })
    return entries


def load_spreadsheet(file_handle):
    contents = file_handle.read()
    wb = xlrd.open_workbook(file_contents=contents)
    (sheet,) = wb.sheets()
    header = None
    for row_index in range(sheet.nrows):
        row = sheet.row_values(row_index)
        if row[0] == 'Date':
            header = row
            break

    entries = []
    for row_index in range(row_index + 1, sheet.nrows):
        row = sheet.row_values(row_index)
        start, duration = parse_row(dict(zip(header, row)))
        entries.append({
            'duration': duration,
            'start': start,
        })
    return entries
