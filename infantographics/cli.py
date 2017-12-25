import argparse
import sys

from . import calendar_circle, calendar_grid, time_bars


modules = {
    'calendar-circle': calendar_circle.generate,
    'calendar-grid': calendar_grid.generate,
    'time-bars': time_bars.generate,
}


def get_module(name):
    try:
        return modules[name]
    except KeyError:
        raise argparse.ArgumentTypeError(f'Invalid type `{name}`')


def setup_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--type', type=get_module)

    parser.add_argument(
        'input_filename',
        nargs='?',
        type=argparse.FileType('r'),
        default=sys.stdin,
    )
    parser.add_argument(
        'output_filename',
        nargs='?',
        type=argparse.FileType('w'),
        default=sys.stdout,
    )
    return parser


def main():
    parser = setup_parser()
    args = parser.parse_args()
    args.type(args)
