#
# Copyright The NOMAD Authors.
#
# This file is part of NOMAD. See https://nomad-lab.eu for further info.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import datetime
import numpy as np

from nomad.datamodel import EntryArchive
from nomad.parsing import FairdiParser
from nomad.units import ureg as units
from nomad.datamodel.metainfo.public import section_run as Run
from nomad.datamodel.metainfo.public import section_system as System
from nomad.datamodel.metainfo.public import section_single_configuration_calculation as SCC

from nomad.parsing.file_parser import UnstructuredTextFileParser, Quantity

from . import metainfo

'''
This is a hello world style example for an example parser/converter.
'''


class ExampleParser(FairdiParser):
    def __init__(self):
        super().__init__(name='parsers/example', code_name='EXAMPLE')

    def run(self, mainfile: str, archive: EntryArchive, logger):
        # Log a hello world, just to get us started. TODO remove from an actual parser.
        logger.info('Hello World')

        run = archive.m_create(Run)
        run.program_name = 'EXAMPLE'
