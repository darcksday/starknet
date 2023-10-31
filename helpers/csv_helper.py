import csv
import os


def start_csv(csv_name):
    source_file = "config/wallets.csv"
    destination_file = f'results/{csv_name}.csv'
    if not os.path.isfile(destination_file):
        # Read data from the source CSV file
        with open(source_file, 'r') as source_csv:
            source_lines = source_csv.readlines()

        # Write data to the destination CSV file
        with open(destination_file, 'w') as dest_csv:
            dest_csv.writelines(source_lines)


def write_csv_success(index, data):
    index = index + 1
    function_name = data['function']
    csv_name = data['csv_name']

    with open(f'results/{csv_name}.csv', 'r') as file:
        reader = csv.reader(file)
        rows = list(reader)

        if index < len(rows):
            rows[index][4] = data['status']
            rows[index][5] = function_name
            rows[index][6] = data['date']

    with open(f'results/{csv_name}.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerows(rows)


def write_csv_error(csv_name, data):
    with open(f'results/error_{csv_name}.csv', 'a') as file:
        writer = csv.writer(file)

        if file.tell() == 0:
            writer.writerow(['address', 'private_key', 'function', 'params', 'error', 'time'])

        writer.writerow(data)


def write_csv_volume(csv_name, data):
    with open(f'results/{csv_name}.csv', 'a') as file:
        writer = csv.writer(file)

        if file.tell() == 0:
            writer.writerow(['address', 'private_key', 'path', 'total_volume USD', 'tx_sum(w-ot approves)', 'start_time', 'end_time'])

        writer.writerow(data)


def get_csv_separator():
    with open('config/wallets.csv', newline='') as csvfile:
        return ';' if ';' in csvfile.readline() else ','
