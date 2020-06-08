import yaml,csv

csvfile = open('custInfo.csv', 'r')
datareader = csv.reader(csvfile, delimiter=",", quotechar='"')
result = list()
type_index = -1
child_fields_index = -1

for row_index, row in enumerate(datareader):
  if row_index == 0:
    # let's do this once here
    data_headings = list()
    for heading_index, heading in enumerate(row):
      fixed_heading = heading.lower().replace(" ", "_").replace("-", "")
      data_headings.append(fixed_heading)
      if fixed_heading == "type":
        type_index = heading_index
      elif fixed_heading == "childfields":
        child_fields_index = heading_index
  else:
    content = dict()
    is_array = False
    for cell_index, cell in enumerate(row):
      if cell_index == child_fields_index and is_array:
        content[data_headings[cell_index]] = [{
            "source" : "fra:" + value.capitalize(),
            "destination" : value,
            "type" : "string",
            "childfields" : "null"
          } for value in cell.split(",")]
      else:
        content[data_headings[cell_index]] = cell
        is_array = (cell_index == type_index) and (cell == "array")
    result.append(content)
print yaml.dump(result)