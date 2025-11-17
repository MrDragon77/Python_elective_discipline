import csv

def write_data(file_path, data):
    with open(file_path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in data.items():
            writer.writerow([key, value])