from datetime import datetime, timedelta, time
import csv
import json


def load():
    reader = csv.DictReader(open('data.csv'))
    data = list(reader)
    entries = []
    for row in data:
        date = datetime.strptime(row['Date'], '%m-%d-%Y')
        weekday = date.weekday()
        start = datetime.strptime(row['Start'].replace('00:', '12:'), '%I:%M %p')
        duration = int(row['Duration [min]'])
        entries.append({
            'x': weekday,
            'y': start.hour * 60 + start.minute,
            'r': duration,
        })


def parse():
    reader = csv.DictReader(open('data.csv'))
    data = list(reader)
    entries = []
    for row in data:
        date = datetime.strptime(row['Date'], '%m-%d-%Y')
        weekday = date.weekday()
        start = datetime.strptime(row['Start'].replace('00:', '12:'), '%I:%M %p')
        duration = int(row['Duration [min]'])
        entries.append({
            'date': date,
            'duration': duration,
            'start': start,
        })
    return entries


def write_json(entries):
    with open('data.json', 'w') as handle:
        json.dump(entries, handle, indent=4)


def write_svg(entries):
    svg_width = 1000
    with open('output1.svg', 'w') as handle:
        #  <svg width="100" height="100">
        handle.write("""
        <svg xmlns="http://www.w3.org/2000/svg"
    xmlns:xlink="http://www.w3.org/1999/xlink">
    width="{width}" height="10000">

   <style>
   .feed {{fill:#54a9a3}}
   .day-part {{fill: #f4f2e9}}
   </style>
""".format(width=svg_width))

        #  entries[0:0] = [{
        #      'date': datetime(2017,6,13),
        #      'duration': 60*24,
        #      'start': datetime.strptime('0', '%H'),
        #  }]
        first = entries[0]
        last = entries[-1]

        first_start = datetime.strptime('0', '%H')
        first_date = first['date']
        last_date = last['date']

        seconds_per_day = timedelta(days=1).total_seconds()

        def date_y(date):
            return (date - first_date).total_seconds() / seconds_per_day * 25

        def time_x(time):
            return (time - first_start).total_seconds() /seconds_per_day * svg_width + 100

        def minute_width(minute):
            return svg_width * minute / (24*60)

        for offset in [0, svg_width / 2]:
            handle.write(
                '<rect class="day-part" x="{x}" y="{y}" width="{width}" height="{height}"/>\n'.format(
                    x=time_x(first_start) + offset,
                    y=date_y(first_date),
                    width=minute_width(60*6),
                    height=date_y(last_date),
                )
            )

        for entry in entries:
            y = date_y(entry['date'])
            #  import pdb; pdb.set_trace()
            x = time_x(entry['start'])
            width = minute_width(entry['duration'])
            handle.write(
                ' <text x="10" y="{y}" font-size="15" font-family="Georgia">{date}</text>\n'.format(
                    date=entry['date'].date(),
                    y=y + 20,
                )
            )
            handle.write(
                '<rect class="feed" x="{x}" y="{y}" width="{width}" height="20"/>\n'.format(
                    x=x,
                    y=y,
                    width=width,
                )
            )

        handle.write("</svg>")


def main():
    #  write_json(load())
    write_svg(parse())


if __name__ == '__main__':
    main()