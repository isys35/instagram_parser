import csv


def create_file(file_name):
    with open(file_name, "w", newline="") as file:
        csv.writer(file)


def add_data(file_name, data):
    with open(file_name, "a", newline="") as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(data)

