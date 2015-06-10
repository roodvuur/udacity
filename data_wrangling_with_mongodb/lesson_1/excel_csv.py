# -*- coding: utf-8 -*-
# Find the time and value of max load for each of the regions
# COAST, EAST, FAR_WEST, NORTH, NORTH_C, SOUTHERN, SOUTH_C, WEST
# and write the result out in a csv file, using pipe character | as the delimiter.
# An example output can be seen in the "example.csv" file.

import xlrd
import os
import csv
import numpy

datafile = "2013_ERCOT_Hourly_Load_Data.xls"
outfile = "2013_Max_Loads.csv"


def parse_file(datafile):
    workbook = xlrd.open_workbook(datafile)
    sheet = workbook.sheet_by_index(0)
    data = []

    # Loop through every column
    for i, numcol in enumerate(range(1, sheet.ncols)):
        # Set dummy values
        vmax = {'region' : sheet.cell_value(0, numcol), 'value' : 0, 'date' : ()}
        # Loop through all rows, excluding row 1
        for numrow in range(1, sheet.nrows):
            # If value is higher than last found high value, set data
            if sheet.cell_value(numrow, numcol) > vmax['value']:
                vmax['value'] = sheet.cell_value(numrow, numcol)
                vmax['date'] = xlrd.xldate_as_tuple(sheet.cell_value(numrow, 0), 0)
        data.append(vmax)

    return data

def save_file(data, filename):
    with open(filename, 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter = '|')
        # Header
        writer.writerow(['Station', 'Year', 'Month', 'Day', 'Hour', 'Max Load'])
        for line in data:
            writer.writerow([line['region'], line['date'][0], line['date'][1], line['date'][2], line['date'][3], line['value']])
        
def test():
    data = parse_file(datafile)
    save_file(data, outfile)

    number_of_rows = 0
    stations = []

    ans = {'FAR_WEST': {'Max Load': '2281.2722140000024',
                        'Year': '2013',
                        'Month': '6',
                        'Day': '26',
                        'Hour': '17'}}
    correct_stations = ['COAST', 'EAST', 'FAR_WEST', 'NORTH',
                        'NORTH_C', 'SOUTHERN', 'SOUTH_C', 'WEST']
    fields = ['Year', 'Month', 'Day', 'Hour', 'Max Load']

    with open(outfile) as of:
        csvfile = csv.DictReader(of, delimiter="|")
        for line in csvfile:
            station = line['Station']
            if station == 'FAR_WEST':
                for field in fields:
                    # Check if 'Max Load' is within .1 of answer
                    if field == 'Max Load':
                        max_answer = round(float(ans[station][field]), 1)
                        max_line = round(float(line[field]), 1)
                        assert max_answer == max_line

                    # Otherwise check for equality
                    else:
                        assert ans[station][field] == line[field]

            number_of_rows += 1
            stations.append(station)

        # Output should be 8 lines not including header
        assert number_of_rows == 8

        # Check Station Names
        assert set(stations) == set(correct_stations)

        
if __name__ == "__main__":
    test()
