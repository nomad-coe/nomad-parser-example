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

from . import metainfo  # pylint: disable=unused-import

'''
This is a hello world style example for an example parser/converter.
'''


def str_to_sites(string):
    sym, pos = string.split('(')
    pos = np.array(pos.split(')')[0].split(',')[:3], dtype=float)
    return sym, pos


calculation_parser = UnstructuredTextFileParser(quantities=[
    Quantity('sites', r'([A-Z]\([\d\.\, \-]+\))', str_operation=str_to_sites),
    Quantity(
        System.lattice_vectors,
        r'(?:latice|cell): \((\d)\, (\d), (\d)\)\,?\s*\((\d)\, (\d), (\d)\)\,?\s*\((\d)\, (\d), (\d)\)\,?\s*',
        repeats=False),
    Quantity('energy', r'energy: (\d\.\d+)'),
    Quantity('magic_source', r'done with magic source\s*\*{3}\s*\*{3}\s*[^\d]*(\d+)', repeats=False)])

mainfile_parser = UnstructuredTextFileParser(quantities=[
    Quantity('date', r'(\d\d\d\d\/\d\d\/\d\d)', repeats=False),
    Quantity('program_version', r'super\_code\s*v(\d+)\s*', repeats=False),
    Quantity(
        'calculation', r'\s*system \d+([\s\S]+?energy: [\d\.]+)([\s\S]+\*\*\*)*',
        sub_parser=calculation_parser,
        repeats=True)
])


class ExampleParser(FairdiParser):
    def __init__(self):
        super().__init__(
            name='parsers/example', code_name='EXAMPLE', code_homepage='https://www.example.eu/',
            mainfile_mime_re=r'(application/.*)|(text/.*)',
            mainfile_contents_re=(r'^\s*#\s*This is example output'),
            supported_compressions=['gz', 'bz2', 'xz']
        )

    def run(self, mainfile: str, archive: EntryArchive, logger):
        # Log a hello world, just to get us started. TODO remove from an actual parser.
        logger.info('Hello World')

        # Use the previously defined parsers on the given mainfile
        mainfile_parser.mainfile = mainfile
        mainfile_parser.parse()

        # Output all parsed data into the given archive.
        run = archive.m_create(Run)
        run.program_name = 'super_code'
        run.program_version = str(mainfile_parser.get('program_version'))
        date = datetime.datetime.strptime(
            mainfile_parser.get('date'),
            '%Y/%m/%d') - datetime.datetime(1970, 1, 1)
        run.program_compilation_datetime = date.total_seconds()

        for calculation in mainfile_parser.get('calculation'):
            system = run.m_create(System)

            system.lattice_vectors = calculation.get('lattice_vectors')
            sites = calculation.get('sites')
            system.atom_labels = [site[0] for site in sites]
            system.atom_positions = [site[1] for site in sites]

            scc = run.m_create(SCC)
            scc.single_configuration_calculation_to_system_ref = system
            scc.energy_total = calculation.get('energy') * units.eV
            scc.single_configuration_calculation_to_system_ref = system
            magic_source = calculation.get('magic_source')
            if magic_source is not None:
                scc.x_example_magic_value = magic_source
