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

from nomad.metainfo import Section, Quantity, MSection, SubSection
import numpy as np

from nomad.datamodel import EntryArchive
from nomad.metainfo.metainfo import Datetime


class DeviceSettings(MSection):
    device_name = Quantity(type=str)
    analysis_method = Quantity(type=str)
    analyzer_lens = Quantity(type=str)
    analyzer_slit = Quantity(type=str)
    scan_mode = Quantity(type=str)
    detector_voltage = Quantity(type=str)
    workfunction = Quantity(type=str)
    channel_id = Quantity(type=str)


class Sample(MSection):
    spectrum_region = Quantity(type=str, shape=[])
    sample_id = Quantity(type=str)
    formula = Quantity(type=str)
    elements = Quantity(type=str, shape=['*'])


class Experiment(MSection):
    method_name = Quantity(type=str)
    experiment_id = Quantity(type=str)
    experiment_start_time = Quantity(
        type=Datetime, description='The datetime of the beginning of the experiment.')
    experiment_publish_time = Quantity(
        type=Datetime, description='The datetime when this experiment was published.')
    experiment_end_time = Quantity(
        type=Datetime, description='The datetime of the experiment end.')
    edges = Quantity(type=str, shape=['*'])


class Instrument(MSection):
    n_scans = Quantity(type=str)
    dwell_time = Quantity(type=str)
    excitation_energy = Quantity(type=str)
    source_label = Quantity(type=str)

    section_device_settings = SubSection(sub_section=DeviceSettings, repeats=True)


class AuthorGenerated(MSection):
    author_name = Quantity(type=str)
    group_name = Quantity(type=str)


class DataHeader(MSection):
    channel_id = Quantity(type=str)
    label = Quantity(type=str)
    unit = Quantity(type=str)


class Origin(MSection):
    permalink = Quantity(type=str)
    api_permalink = Quantity(type=str)
    repository_name = Quantity(
        type=str, description='The name of the repository, where the data is stored.')

    repository_url = Quantity(
        type=str, description='An URL to the repository, where the data is stored.')

    preview_url = Quantity(
        type=str, description='An URL to an image file that contains a preview.')

    entry_repository_url = Quantity(
        type=str, description='An URL to the entry on the repository, where the data is stored.')


class Spectrum(MSection):
    n_values = Quantity(type=int)
    kinetic_energy = Quantity(type=np.dtype(np.float64), shape=['n_values'], unit='J', description='The kinetic energy range of the spectrum')
    binding_energy = Quantity(type=np.dtype(np.float64), shape=['n_values'], unit='J', description='The binding energy range of the spectrum')
    count = Quantity(type=np.dtype(np.float64), shape=['n_values'], description='The count at each energy value, dimensionless')


class Metadata(MSection):
    section_sample = SubSection(sub_section=Sample, repeats=True)
    section_experiment = SubSection(sub_section=Experiment, repeats=True)
    section_instrument = SubSection(sub_section=Instrument, repeats=True)
    section_author_generated = SubSection(sub_section=AuthorGenerated, repeats=True)
    section_data_header = SubSection(sub_section=DataHeader, repeats=True)
    section_origin = SubSection(sub_section=Origin, repeats=True)


class Data(MSection):
    section_spectrum = SubSection(sub_section=Spectrum, repeats=True)


class Measurement(MSection):
    section_metadata = SubSection(sub_section=Metadata, repeats=True)
    section_data = SubSection(sub_section=Data, repeats=True)


class MyEntryArchive(EntryArchive):
    m_def = Section(extends_base_section=True)
    section_measurement = SubSection(sub_section=Measurement, repeats=True)
