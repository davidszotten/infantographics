from .load import load_csv


def generate(args):
    input_filename = args.input_filename
    output_filename = args.output_filename
    data = load_csv(input_filename)
    write_svg(data, output_filename)


def write_svg(entries, handle):
    width = 100
    height = 100
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
