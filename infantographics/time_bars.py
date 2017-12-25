import json

from .load import load_csv


def write_json(entries):
    with open('data.json', 'w') as handle:
        json.dump(entries, handle, indent=4)


def format_data(filename):
    entries = []
    for entry in load_csv(filename):
        start = entry['start']
        duration = entry['duration']

        entries.append({
            'x': start.weekday(),
            'y': start.hour * 60 + start.minute,
            'r': duration,
        })
