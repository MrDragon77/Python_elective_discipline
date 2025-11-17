import csv

def read_data(file_path):
    data = None
    with open(file_path) as csv_file:
        reader = csv.reader(csv_file)
        data = dict(reader)
        data = {int(i):float(key) for i,key in data.items()}
    return data