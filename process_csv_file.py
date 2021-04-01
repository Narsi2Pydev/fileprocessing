
import csv
import constants as cons
import os
import datetime
import logging

logger = logging.getLogger(__name__)

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
        row[0] = datetime.datetime.strptime(row[0], '%d %b %Y').strftime('%d-%m-%Y')
        row[2] = int(row[2]) * int(row[3])
        row.append(row.pop(4))
        remove_column = row.pop(3)
        data[index + 1] = row
    return data

def update_in_csv_file(path, data):
    file_name = cons.OUTPUT_FILE_NAME
    fields = data[0]
    rows = data[1:]
    with open(path+file_name, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        # writing the fields
        csvwriter.writerow(fields)
        # writing the data rows
        csvwriter.writerows(rows)
    logger.info(f"file{file_name} is saved in the path{path}")

def run():
    path = cons.PATH
    files = os.listdir(path)
    output = []
    csv_files  = [f for f in files if f.endswith(".csv")]
    logger.info(f"bank csv files{''.join(csv_files)}")
    for file in csv_files:
            with open(path+file, 'r') as csvfile:
                file_reader = csv.reader(csvfile)
                file_data = [row for row in file_reader]

                if 'timestamp' in file_data[0]:
                   file1_data = process_bank1_file(file_data)
                   if len(output) > 0:
                       output.extend(file1_data[1:])
                   else:
                       output.extend(file1_data)
                elif 'date' in file_data[0]:
                    file2_data = process_bank2_file(file_data)
                    if len(output) > 0:
                        output.extend(file1_data[1:])
                    else:
                        output.extend(file1_data)
                elif 'date_readable' in file_data[0]:
                    file3_data = process_bank3_file(file_data)
                    if len(output) > 0:
                        output.extend(file3_data[1:])
                    else:
                        output.extend(file3_data)
                else:
                    pass

    if len(output) > 0:
        logger.info(f"all files are processed updating in the unified csv file")
        update_in_csv_file(path, output)

if __name__ == '__main__':
    run()
