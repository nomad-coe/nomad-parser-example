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

import logging

import pytest
from nomad.datamodel import EntryArchive

from exampleparser import ExampleParser


@pytest.fixture
def parser():
    return ExampleParser()


def test_example(parser):
    archive = EntryArchive()
    parser.parse('tests/data/example.out', archive, logging)

    sim = archive.data
    assert len(sim.model) == 2
    assert len(sim.output) == 2
    assert archive.workflow2.x_example_magic_value == 42
