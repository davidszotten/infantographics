"""
Chart with days going down and hours going across

     0 1 2 ...  23
day1  ###
day2        ##
day3     ##    #
...
"""
from datetime import datetime, timedelta, time, date
import math

from .load import load_spreadsheet
from .templates import render


def generate(args):
    input_filename = args.input_filename
    output_filename = args.output_filename
    data = load_spreadsheet(input_filename)
    write_svg(data, output_filename)


def polar_to_cartesian(center_x, center_y, radius, angle_in_degrees):
    angle_in_radians = (angle_in_degrees-90) * math.pi / 180.0

    return {
      'x': center_x + (radius * math.cos(angle_in_radians)),
      'y': center_y + (radius * math.sin(angle_in_radians))
    }


def describe_arc(x, y, radius, start_angle, end_angle):
    # https://stackoverflow.com/questions/5736398/
    # how-to-calculate-the-svg-path-for-an-arc-of-a-circle

    start = polar_to_cartesian(x, y, radius, end_angle)
    end = polar_to_cartesian(x, y, radius, start_angle)

    large_arc_flag = "0" if end_angle - start_angle <= 180 else "1"

    return "M {sx} {sy} A {r} {r} 0 {flag} 0 {ex} {ey}".format(
        sx=start['x'],
        sy=start['y'],
        r=radius,
        flag=large_arc_flag,
        ex=end['x'],
        ey=end['y'],
    )


def time_diff(start, end):
    return datetime.combine(date.min, end) - datetime.combine(date.min, start)


def write_svg(entries, handle):
    day_width = 10000
    date_column_width = 100
    radius_width = 25
    width = day_width + date_column_width

    first = entries[0]
    last = entries[-1]

    first_start = first['start']
    base = datetime.combine(first_start.date(), time())
    last_start = last['start']

    seconds_per_day = timedelta(days=1).total_seconds()

    n_days = (last_start.date() - first_start.date()).days + 1

    height = radius_width * n_days * 2

    def date_radius(dt):
        return (
            dt.date() - base.date()
        ).total_seconds() / seconds_per_day * radius_width

    def time_angle(dt):
        return time_diff(
            base.time(), dt.time()
        ).total_seconds() / seconds_per_day * 360

    def minute_width(minute):
        return day_width * minute / (24*60)

    #  day_shades = [
    #      dict(
    #          path=describe_arc(
    #               height/2, height/2, radius, start_angle, end_angle
    #           )
    #          x=time_x(base) + offset,
    #          y=date_y(base),
    #          width=minute_width(60 * 6),
    #          height=date_y(last_start) + row_height,
    #      )
    #      for offset in [0, day_width / 2]
    #  ]

    rows = [
        dict(
            path=describe_arc(
                height/2,
                height/2,
                date_radius(entry['start']),
                time_angle(entry['start']),
                time_angle(
                    entry['start'] + timedelta(minutes=entry['duration'])
                ),
            )
        ) for entry in entries
    ]
    handle.write(render('calendar_circle.jinja', {
        'width': width,
        'height': height,
        #  'day_shades': day_shades,
        'rows': rows,
    }))
