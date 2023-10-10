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
from nomad.units import ureg as units
from nomad.datamodel.metainfo.simulation.run import Run, Program
from nomad.datamodel.metainfo.simulation.system import System, Atoms
from nomad.datamodel.metainfo.simulation.calculation import Calculation, Energy, EnergyEntry

from nomad.parsing.file_parser import TextParser, Quantity

from . import metainfo  # pylint: disable=unused-import

'''
This is a hello world style example for an example parser/converter.
'''


def str_to_sites(string):
    sym, pos = string.split('(')
    pos = np.array(pos.split(')')[0].split(',')[:3], dtype=float)
    return sym, pos


calculation_parser = TextParser(quantities=[
    Quantity('sites', r'([A-Z]\([\d\.\, \-]+\))', str_operation=str_to_sites, repeats=True),
    Quantity(
        Atoms.lattice_vectors,
        r'(?:latice|cell): \((\d)\, (\d), (\d)\)\,?\s*\((\d)\, (\d), (\d)\)\,?\s*\((\d)\, (\d), (\d)\)\,?\s*',
        repeats=False),
    Quantity('energy', r'energy: (\d\.\d+)'),
    Quantity('magic_source', r'done with magic source\s*\*{3}\s*\*{3}\s*[^\d]*(\d+)', repeats=False)])

mainfile_parser = TextParser(quantities=[
    Quantity('date', r'(\d\d\d\d\/\d\d\/\d\d)', repeats=False),
    Quantity('program_version', r'super\_code\s*v(\d+)\s*', repeats=False),
    Quantity(
        'calculation', r'\s*system \d+([\s\S]+?energy: [\d\.]+)([\s\S]+\*\*\*)*',
        sub_parser=calculation_parser,
        repeats=True)
])


class ExampleParser:
    def parse(self, mainfile: str, archive: EntryArchive, logger):
        # Log a hello world, just to get us started. TODO remove from an actual parser.
        logger.info('Hello World')

        # Use the previously defined parsers on the given mainfile
        mainfile_parser.mainfile = mainfile
        mainfile_parser.parse()

        run = Run()
        date = datetime.datetime.strptime(mainfile_parser.date, '%Y/%m/%d')
        run.program = Program(
            name='super_code', version=mainfile_parser.get('program_version'),
            compilation_datetime=date.timestamp())

        for calculation in mainfile_parser.get('calculation', []):
            system = System(atoms=Atoms())

            system.atoms.lattice_vectors = calculation.get('lattice_vectors')
            sites = calculation.get('sites')
            system.atoms.labels = [site[0] for site in sites]
            system.atoms.positions = [site[1] for site in sites]
            run.system.append(system)

            calc = Calculation(energy=Energy())
            calc.system_ref = system
            calc.energy.total = EnergyEntry(value=calculation.get('energy') * units.eV)
            magic_source = calculation.get('magic_source')
            if magic_source is not None:
                calc.x_example_magic_value = magic_source
            run.calculation.append(calc)
        archive.run.append(run)
