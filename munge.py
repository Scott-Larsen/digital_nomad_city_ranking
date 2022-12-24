import csv

from collections import defaultdict

ROOT_FOLDER = "/Users/Scott/Desktop/DATA/SORT/CodingProgrammingPython/digital_nomad_city_ranking/"
ATTRIBUTE_FILES = [{"attribute": "safety", "filename": "safety.csv"}, {
    "attribute": "cost_of_living", "filename": "cost_of_living.csv"}]  # {"attribute": "internet_speed", "filename": "internet_speed.csv"},]

data = defaultdict(dict)

# file_location = ROOT_FOLDER + FILE_NAMES[0]["filename"]


def read_data_from_csv(file_location, attribute):
    with open(file_location, newline='') as f:
        spamreader = csv.reader(f, dialect='excel')
        for city, score in spamreader:
            # print(data[city][str(attribute)])
            data[city][str(attribute)] = score


def write_data_to_csv(file_location, data):

    with open(file_location, "w", newline='') as f:
        fieldnames = ["city"] + list(next(iter(data.values())).keys())
        print(f"{fieldnames = }")
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        writer.writeheader()
        for k, v in data.items():
            dict_line_to_write = {'city': k}
            dict_line_to_write.update(v)
            writer.writerow(dict_line_to_write)


for attribute_file in ATTRIBUTE_FILES:
    file_location = ROOT_FOLDER + attribute_file['filename']
    attribute = attribute_file['attribute']
    read_data_from_csv(file_location=file_location, attribute=attribute)

selection = {c: v for c, v in data.items() if len(v) == 2}
print(selection)

write_data_to_csv(ROOT_FOLDER + "city_stats.csv", selection)
