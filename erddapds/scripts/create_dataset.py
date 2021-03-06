from __future__ import (absolute_import,
                        division,
                        print_function,
                        unicode_literals)

import argparse

import yaml

import erddapds


def get_arguments():
    parser = argparse.ArgumentParser(description='Create new ERDDAP Dataset')
    parser.add_argument('dsid', metavar='DATASETID', type=str,
                        help='Dataset ID')
    parser.add_argument('configfile', metavar='CONFIGFILE',
                        help='Config yaml file')
    parser.add_argument('gdsloc', metavar='GDSLOC', type=str,
                        help='GenerateDatasetsXml.sh (Full path)')
    parser.add_argument('datasetsxml', metavar='DATASETSXML', type=str,
                        help='Datasets xml file (Full path)')
    parser.add_argument('bpd', metavar='BIGPARENTDIRECTORY', type=str,
                        help='Path to Big Parent Directory')
    parser.add_argument('datadir', metavar='DATADIRECTORY', type=str,
                        help='Data Directory')

    # Optionals
    parser.add_argument('-v','--version', action='version', version=erddapds.__version__)
    parser.add_argument('--infourl',
                        metavar='INFOURL',
                        type=str,
                        default='http://example.com',
                        help='infoUrl')
    parser.add_argument('--institution',
                        metavar='INSTITUTION',
                        type=str,
                        default='Some Organization',
                        help='institution')
    parser.add_argument('--summary',
                        metavar='SUMMARY',
                        type=str,
                        default='This is some data',
                        help='summary')
    parser.add_argument('--title',
                        metavar='TITLE',
                        type=str,
                        default='NETCDF File',
                        help='title')

    return parser.parse_args()


def parse_yaml(yaml_file):
    with open(yaml_file, 'r') as yml:
        ymldct = yaml.load(yml.read())

    assert 'details' in ymldct

    return ymldct


def main():
    args = get_arguments()
    print(args)
    ymldct = parse_yaml(args.configfile)
    edd = erddapds.ERDDAPDATASET(args.dsid, **ymldct)
    # TODO: Generalize this for other Type of EDD
    tree = edd.generate_datasetxml('EDDTableFromNcCFFiles',
                                   args.datadir,
                                   ymldct['details']['fileNameRegex'],
                                   '',
                                   '',
                                   '',
                                   '',
                                   '',
                                   '',
                                   '',
                                   'http://example.com',
                                   'Some Organization',
                                   'This is Some Data',
                                   'NetCDF File',
                                   gds_loc=args.gdsloc,
                                   big_parent_directory=args.bpd)

    edd.add_to_datasetsxml(dsxml=args.datasetsxml)


if __name__ == '__main__':
    main()