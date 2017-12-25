"""
Chart with days going down and hours going across

     0 1 2 ...  23
day1  ###
day2        ##
day3     ##    #
...
"""
from datetime import datetime, timedelta, time, date

from .load import load_csv


def generate(args):
    input_filename = args.input_filename
    output_filename = args.output_filename
    data = load_csv(input_filename)
    write_svg(data, output_filename)


def time_diff(start, end):
    return datetime.combine(date.min, end) - datetime.combine(date.min, start)


def write_svg(entries, handle):
    day_width = 1000
    date_column_width = 100
    row_height = 25
    width = day_width + date_column_width

    first = entries[0]
    last = entries[-1]

    first_start = first['start']
    base = datetime.combine(first_start.date(), time())
    last_start = last['start']

    seconds_per_day = timedelta(days=1).total_seconds()

    n_days = (last_start.date() - first_start.date()).days + 1

    height = row_height * n_days

    handle.write("""<svg xmlns="http://www.w3.org/2000/svg"
xmlns:xlink="http://www.w3.org/1999/xlink"
width="{width}" height="{height}">

<style>
.feed {{fill:#54a9a3}}
.day-part {{fill: #f4f2e9}}
text {{font-size: 15; font-family: "Georgia"}}
</style>
""".format(
        width=width,
        height=height,
    ))

    #  entries[0:0] = [{
    #      'date': datetime(2017,6,13),
    #      'duration': 60*24,
    #      'start': datetime.strptime('0', '%H'),
    #  }]
    def date_y(dt):
        return (
            dt.date() - base.date()
        ).total_seconds() / seconds_per_day * row_height

    def time_x(dt):
        return time_diff(
            base.time(), dt.time()
        ).total_seconds() / seconds_per_day * day_width + date_column_width

    def minute_width(minute):
        return day_width * minute / (24*60)

    for offset in [0, day_width / 2]:
        handle.write(
            (
                '<rect class="day-part" x="{x}" y="{y}" '
                'width="{width}" height="{height}"/>\n'
            ).format(
                x=time_x(base) + offset,
                y=date_y(base),
                width=minute_width(60*6),
                height=date_y(last_start) + row_height,
            )
        )

    for entry in entries:
        y = date_y(entry['start'])
        #  import pdb; pdb.set_trace()
        x = time_x(entry['start'])
        width = minute_width(entry['duration'])
        handle.write(
            ' <text x="10" y="{y}">{date}</text>\n'.format(
                date=entry['start'].date(),
                y=y + 20,
            )
        )
        handle.write(
            (
                '<rect class="feed" x="{x}" y="{y}" '
                'width="{width}" height="20"/>\n'
            ).format(
                x=x,
                y=y,
                width=width,
            )
        )

    handle.write("</svg>\n")
