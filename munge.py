import csv

from collections import defaultdict

ROOT_FOLDER = "/Users/Scott/Desktop/DATA/SORT/CodingProgrammingPython/digital_nomad_city_ranking/"
ATTRIBUTE_FILES = [
    {"attribute": "safety", "filename": "safety.csv"},
    {"attribute": "cost_of_living", "filename": "cost_of_living.csv"}
]
# {"attribute": "internet_speed", "filename": "internet_speed.csv"},]


# file_location = ROOT_FOLDER + FILE_NAMES[0]["filename"]


def read_data_from_csv(file_location, attribute, data_read_in_from_csvs):

    # data = defaultdict(dict)

    with open(file_location, newline='') as f:
        spamreader = csv.reader(f, dialect='excel')
        for city, score in spamreader:
            # print(data[city][str(attribute)])
            data_read_in_from_csvs[city][str(attribute)] = score

    return data_read_in_from_csvs


def write_data_to_csv(file_location, data_to_be_written_out):

    with open(file_location, "w", newline='') as f:
        fieldnames = ["city"] + \
            list(next(iter(data_to_be_written_out.values())).keys())
        print(f"{fieldnames = }")
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        writer.writeheader()
        for k, v in data_to_be_written_out.items():
            dict_line_to_write = {'city': k}
            dict_line_to_write.update(v)
            writer.writerow(dict_line_to_write)


def main():
    data_read_in_from_csvs = defaultdict(dict)
    for attribute_file in ATTRIBUTE_FILES:
        file_location = ROOT_FOLDER + attribute_file['filename']
        attribute = attribute_file['attribute']
        data_read_in_from_csvs = read_data_from_csv(
            file_location=file_location, attribute=attribute, data_read_in_from_csvs=data_read_in_from_csvs)

    print(f"{data_read_in_from_csvs = }")

    selection = {c: v for c, v in data_read_in_from_csvs.items()
                 if len(v) == 2}
    print(f"{selection = }")

    write_data_to_csv(ROOT_FOLDER + "city_stats.csv", selection)


if __name__ == "__main__":
    main()
