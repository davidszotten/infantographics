from datetime import datetime, time
from itertools import groupby

from .templates import render
from .load import load_csv


def generate(args):
    input_filename = args.input_filename
    output_filename = args.output_filename
    data = load_csv(input_filename)
    write_svg(data, output_filename)


def write_svg(entries, handle):
    day_width = 15

    first = entries[0]

    first_start = first['start']
    base = datetime.combine(first_start.date(), time())

    def date_x(date):
        return (
            date - base.date()
        ).days * day_width

    bars = []
    max_duration = 0
    for date, day_entries in groupby(entries, lambda e: e['start'].date()):
        total_time = sum(e['duration'] for e in day_entries)
        max_duration = max(max_duration, total_time)

        bars.append({
            'x': date_x(date),
            'height': total_time,
        })

    width = day_width * len(bars)
    height = 1000

    handle.write(render('time_bars.jinja', {
        'width': width,
        'height': height,
        'day_width': day_width,
        'max_duration': max_duration,
        'bars': bars,
    }))


#  def write_json(entries):
#      with open('data.json', 'w') as handle:
#          json.dump(entries, handle, indent=4)


#  def format_data(filename):
#      entries = []
#      for entry in load_csv(filename):
#          start = entry['start']
#          duration = entry['duration']

#          entries.append({
#              'x': start.weekday(),
#              'y': start.hour * 60 + start.minute,
#              'r': duration,
#          })
