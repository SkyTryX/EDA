import csv

def load_map_from_csv(file_path):
    map_data = []
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            map_data.append(row)
    return map_data
