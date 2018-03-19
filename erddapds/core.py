from __future__ import (absolute_import,
                        division,
                        print_function,
                        unicode_literals)

import os
import sys
from collections import OrderedDict
import subprocess

from lxml import etree

from erddapds.utils import (update_xml, print_tree)

METADATA = OrderedDict([
    ('infoUrl', {
        'text':
            'http://example.com/',
    }),
    ('institution', {
        'text': 'My Institution',
    }),
    ('institution_fullname', {
        'text': 'ERDDAP Institution, Some University',
        'after': 'institution',
    }),
    ('license', {
        'text': '''This is a license.
        Please use with care.
        ''',
    }),
    ('project', {
        'text': 'My wonderful project',
        'after': 'title',
    }),
    ('creator_name', {
        'text': 'John Doe',
        'after': 'project',
    }),
    ('creator_email', {
        'text': 'johndoe@someuniversity.edu',
        'after': 'creator_name',
    }),
    ('creator_url', {
        'text': 'http://example.com/johndoe',
        'after': 'creator_email',
    }),
    ('acknowledgement', {
        'text': 'AI, PC',
        'after': 'creator_url',
    }),
    ('drawLandMask', {
        'text': 'over',
        'after': 'acknowledgement',
    }),
])


class ERDDAPDATASET(object):
    def __init__(self, dsid, details, variables, metadata=METADATA):
        self.dsid = dsid
        self.details = details
        self.variables = variables
        self.metadata = metadata
        self.__dsfragment = None
        self.__bpd = None

        try:
            self.__check_type()
        except TypeError as e:
            print(e)

    def __repr__(self):
        return f'<ERDDAPDATASET: {self.dsid}>'

    def __check_type(self):
        assert isinstance(self.dsid, str), f'{self.dsid} is not a string'
        assert isinstance(self.details, dict), f'{self.details} is not a dictionary'
        assert isinstance(self.variables, dict), f'{self.variables} is not a dictionary'
        assert isinstance(self.metadata, dict), f'{self.metadata} is not a dictionary'

    def generate_datasetxml(self, *args, gds_loc='', big_parent_directory=''):
        if gds_loc:
            if os.path.basename(gds_loc) == 'GenerateDatasetsXml.sh':
                try:
                    os.chdir(os.path.dirname(gds_loc))
                    prog = ['/bin/bash', gds_loc]
                    cmd = prog + list(map(lambda x: str(x), args))

                    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                    out, err = p.communicate()

                    if p.returncode == 0:
                        self.__bpd = big_parent_directory
                        outlog = os.path.join(os.path.abspath(big_parent_directory),
                                              'logs', 'GenerateDatasetsXml.out')

                        print(f'Dataset template sucessfully generated. See: {outlog}')

                        parser = etree.XMLParser(remove_blank_text=True)
                        tree = etree.parse(outlog, parser)
                        self.__dsfragment = tree.getroot()
                        # finalizing dataset fragment
                        update_xml(root=self.__dsfragment,
                                   datasetID=self.dsid,
                                   metadata=self.metadata,
                                   details=self.details,
                                   dataset_vars=self.variables)

                        return self.__dsfragment
                    else:
                        print(f'Dataset template generation failed, '
                              f'exit-code={int(p.returncode)} error = {str(err)}')

                except OSError as e:
                    sys.exit(f'failed to execute program \'{prog}\': {str(e)}')

    def export_datasetxml(self):
        if self.__dsfragment is not None:
            with open(f'{self.dsid}.xml', 'wb') as f:
                f.write(etree.tostring(self.__dsfragment, pretty_print=True))

    def get_xmlroot(self):
        print_tree(self.__dsfragment)
        return self.__dsfragment

    def add_to_datasetsxml(self, dsxml):
        if dsxml:
            if os.path.basename(dsxml) == 'datasets.xml':
                try:
                    with open(dsxml, 'rb') as xml:
                        tree = etree.XML(xml.read())

                    if self.__dsfragment is not None:
                        tree.append(self.__dsfragment)

                    with open(dsxml, 'wb') as fil:
                        rtree = tree.getroottree()
                        rtree.write(fil, xml_declaration=True, encoding='ISO-8859-1')

                    cmd = ['touch', os.path.join(os.path.abspath(self.__bpd), 'flag', self.dsid)]
                    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                    out, err = p.communicate()

                    if p.returncode == 0:
                        print(f'Dataset sucessfully added.')
                    else:
                        print(f'Dataset generation failed, '
                              f'exit-code={int(p.returncode)} error = {str(err)}')
                except OSError as e:
                    sys.exit(f'failed to execute program {str(e)}')
