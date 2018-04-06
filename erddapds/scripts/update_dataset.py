from __future__ import (absolute_import,
                        division,
                        print_function,
                        unicode_literals)

import argparse

import yaml

import erddapds


def get_arguments():
    parser = argparse.ArgumentParser(description='Updates ERDDAP Dataset')
    parser.add_argument('dsid', metavar='DATASETID', type=str,
                        help='Dataset ID')
    parser.add_argument('bpd', metavar='BIGPARENTDIRECTORY', type=str,
                        help='Path to Big Parent Directory')
    parser.add_argument('datadir', metavar='DATADIRECTORY', type=str,
                        help='Data Directory')
    parser.add_argument('newnc', metavar='NEWNCFILE', type=str,
                        help='New NetCDF File to be added (full path)')

    parser.add_argument('--version', action='version', version=erddapds.__version__)

    return parser.parse_args()


def parse_yaml(yaml_file):
    with open(yaml_file, 'r') as yml:
        ymldct = yaml.load(yml.read())

    assert 'details' in ymldct

    return ymldct


def main():
    args = get_arguments()
    print(args)
    edd = erddapds.ERDDAPDATASET(args.dsid)
    edd.update_dataset(args.datadir, args.newnc, args.bpd)


if __name__ == '__main__':
    main()