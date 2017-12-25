from datetime import datetime
import csv


def load_csv(file_handle):
    reader = csv.DictReader(file_handle)
    data = list(reader)
    entries = []
    for row in data:
        datetime_str = '{Date} {Start}'.format(**row)
        # export contains malformed am/pm times (e.g. "00:01 am")
        datetime_str = datetime_str.replace('00:', '12:')
        start = datetime_str
        start = datetime.strptime(datetime_str, '%m-%d-%Y %I:%M %p')
        duration = int(row['Duration [min]'])
        entries.append({
            'duration': duration,
            'start': start,
        })
    return entries
