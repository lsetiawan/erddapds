from __future__ import (absolute_import,
                        division,
                        print_function,
                        unicode_literals)

import os
import sys
import logging
from collections import OrderedDict
import subprocess

from lxml import etree
import yaml

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
    def __init__(self, id, details, variables, metadata=METADATA):
        self.id = id
        self.details = details
        self.variables = variables
        self.metadata = metadata

        try:
            self.__check_type()
        except Exception as e:
            print(e)

    def __check_type(self):
        assert isinstance(self.id, str), f'{self.id} is not a string'
        assert isinstance(self.details, dict), f'{self.details} is not a dictionary'
        assert isinstance(self.variables, dict), f'{self.variables} is not a dictionary'
        assert isinstance(self.metadata, dict), f'{self.metadata} is not a dictionary'

    def generate_datasetxml(self, *args, gds_loc=''):
        if os.path.basename(gds_loc) == 'GenerateDatasetsXml.sh':
            try:
                prog = ['/bin/bash', gds_loc]
                cmd = prog + list(map(lambda x: str(x), args))
                print(cmd)

                p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                out, err = p.communicate()

                if p.returncode == 0:
                    print(f'command \'{prog} {args}\' succeeded, returned: {str(out)}')
                else:
                    print(f'command \'{prog} {args}\' failed, '
                          f'exit-code={int(p.returncode)} error = {str(err)}')
            except OSError as e:
                sys.exit(f'failed to execute program \'{prog}\': {str(e)}')





