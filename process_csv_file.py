
import csv
import constants as cons
import os
import datetime

def process_bank1_file(data):
    headers = data[0]
    headers[0]= 'date'
    data[0] = headers
    print(data)
    for index, row in enumerate(data[1:]):
        print(row[0])
        row[0] = datetime.datetime.strptime(row[0], '%b %d %Y').strftime('%d-%m-%Y')
        data[index+1] = row
    return data

def process_bank2_file(data):
    headers = data[0]
    headers[1] = 'type'
    data[0] = headers
    #for index, row in enumerate(data[1:]):
    #    row[0] = datetime.datetime.strptime(row[0], '%b %d %Y').strftime('%d-%m-%Y')
    #    data[index + 1] = row
    return data

def process_bank3_file(data):
    headers = data[0]
    headers[0] = 'date'
    headers.append(headers.pop(4))
    remove_column = headers.pop(3)
    headers[2] = 'amount'
    data[0] = headers

    for index, row in enumerate(data[1:]):
        print(row[0])
        row[0] = datetime.datetime.strptime(row[0], '%d %b %Y').strftime('%d-%m-%Y')
        row[2] = int(row[2]) * int(row[3])
        row.append(row.pop(4))
        remove_column = row.pop(3)
        data[index + 1] = row
    return data

def update_in_csv_file(path, data):
    file_name = 'unified_bank_data_file.csv'
    fields = data[0]
    rows = data[1:]
    with open(path+file_name, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        # writing the fields
        csvwriter.writerow(fields)
        # writing the data rows
        csvwriter.writerows(rows)

def run():
    path = cons.PATH
    files = os.listdir(path)
    output = []
    for file in files:
        if file.endswith(".csv"):
            with open(path+file, 'r') as csvfile:
                file_reader = csv.reader(csvfile)
                file_data = [row for row in file_reader]

                print(file_data)
                if 'timestamp' in file_data[0]:
                   file1_data = process_bank1_file(file_data)
                   print(file1_data)
                   output.extend(file1_data)
                   print(output)
                elif 'date' in file_data[0]:
                    file2_data = process_bank2_file(file_data)
                    output.extend(file2_data[1:])
                elif 'date_readable' in file_data[0]:
                    file3_data = process_bank3_file(file_data)
                    output.extend(file3_data[1:])
                else:
                    pass

    if len(output) > 0:
        print(output)
        update_in_csv_file(path,output)

if __name__ == '__main__':
    run()
