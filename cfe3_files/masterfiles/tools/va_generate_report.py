#!/usr/bin/env python2.7

import csv
import re
import json
from argparse import ArgumentParser
from sys import exit
from os import listdir, path
from time import time


# Filename of the final host info report.
REPORT_NAME = "va_host_info_report.json"

# A dict of subreports, used to create proper data structs (dict, list) for
# the final json report.
SUBREPORTS = dict(
        cfengine={},
        identity={},
        network_interfaces=[],
        network_ports=[],
        os={},
        software=[]
)

def get_csv_files(report_dir, regex):

    csv_files = []
    rc = re.compile(regex)
    for f in listdir(report_dir):
       found = rc.search(f)
       if found:
           csv_files.append(
                   dict(
                       filename="{}/{}".format(report_dir,found.group()),
                       json_key=rc.findall(found.group())[0]))

    return csv_files


def generate_report(report_dir, csv_files):

    global SUBREPORTS    
    final_report = {}
    final_report['_meta'] = {
                "timestamp": int(time())
            }
    for csv_file in csv_files:
        # Take care of proper type for final_report key values.
        # Default is an empty list if there's a csv file that provides an
        # unkown subreport (subreport = json_key).
        if csv_file['json_key'] in SUBREPORTS.keys():
            final_report[csv_file['json_key']] = SUBREPORTS[csv_file['json_key']]
        else:
            final_report[csv_file['json_key']] = []

        with open(csv_file['filename']) as fp:
            reader = csv.DictReader(fp)
            fieldnames = reader.fieldnames
            for row in reader:
                if isinstance(final_report[csv_file['json_key']], list):
                    final_report[csv_file['json_key']].append(row)
                else:
                    for k, v in row.iteritems():
                        final_report[csv_file['json_key']][k] = v

    return final_report


if __name__ == '__main__':

    # Parse passed arguments.
    parser = ArgumentParser(description="Generate final host info report")
    parser.add_argument(
            '-d',
            help='Destination directory (default: /var/cfengine/reports)',
            type=str,
            default='/var/cfengine/vacana/host_info')
    parser.add_argument(
            '-r',
            help='Regex to find separate csv report files (default: "^va_host_info_report_(.*)\.csv$")',
            type=str,
            default='^va_host_info_report_(.*)\.csv$')  # The matching group is used as JSON key
    args = parser.parse_args()

    # Get list of CSV files based on provided regex.
    csv_files = get_csv_files(path.normpath(args.d), args.r)

    # Generate the report and write to destination.
    report = generate_report(path.normpath(args.d), csv_files)
    report_file = "{}/{}".format(path.normpath(args.d), REPORT_NAME)
    with open(report_file, 'w') as fp:
        json.dump(report, fp, indent=2, sort_keys=True)

    exit(0)
