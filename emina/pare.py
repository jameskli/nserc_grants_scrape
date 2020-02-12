#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv

INPUT_FILE = 'result_400001_500000.csv'
CHECK_STRING = 'N/A'


def main():
    count = 0
    output_filename = 'pared_'+INPUT_FILE
    error_filename = 'error_'+INPUT_FILE
    with open(INPUT_FILE, 'rU') as work_file:
        csv_reader = csv.reader(work_file, delimiter=',', quotechar='"')

        for row in csv_reader:
            if CHECK_STRING in row:
                count += 1
                print("Error in Row {}".format(row[0]))
                with open(error_filename, 'a+') as error_file:
                    # error_csv_writer = csv.writer(error_file, quoting=csv.QUOTE_ALL)
                    error_file.write(row[0])
                    error_file.write('\n')
            else:
                with open(output_filename, 'a+') as output_file:
                    out_csv_writer = csv.writer(
                        output_file, quoting=csv.QUOTE_ALL)
                    out_csv_writer.writerow(row)

        print("{} Errors found".format(count))


main()
