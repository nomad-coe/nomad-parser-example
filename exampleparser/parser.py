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

# import datetime
# import numpy as np
import json

from nomad.datamodel import EntryArchive
from nomad.parsing import FairdiParser
from nomad.units import ureg as units
from nomad.datamodel.metainfo.public import section_run as Run
from nomad.datamodel.metainfo.public import section_system as System
from nomad.datamodel.metainfo.public import section_single_configuration_calculation as SCC

from . import metainfo  # pylint: disable=unused-import
# from .metainfo import Measurement, Sample, Metadata, Instrument
from .metainfo import *
'''
This is a hello world style example for an example parser/converter.
'''


class ExampleParser(FairdiParser):
    def __init__(self):
        super().__init__(
            name='parsers/example', code_name='EXAMPLE', code_homepage='https://www.example.eu/',
            mainfile_mime_re=r'(application/json)'
        )

    def run(self, mainfile: str, archive: EntryArchive, logger):
        # Log a hello world, just to get us started. TODO remove from an actual parser.
        logger.info('Testing the World')

        #Read the JSON file into a dictionary
        with open(mainfile, 'rt') as f:
            file_data = json.load(f)

        #Reading a measurement
        measurement = archive.m_create(Measurement)

        #Create the hierarchical structure
        metadata = measurement.m_create(Metadata)
        data = measurement.m_create(Data)

        # Create the hierarchical structure inside metadata
        sample = metadata.m_create(Sample)
        experiment = metadata.m_create(Experiment)
        instrument = metadata.m_create(Instrument)
        data_header = metadata.m_create(DataHeader)
        author_generated = metadata.m_create(AuthorGenerated)

        #Load entries into each above hierarchical structure
        #Sample
        sample.spectrum_region = file_data[0]['metadata']['spectrum_region']

        #Experiment
        experiment.method_type = file_data[0]['metadata']['method_type']

        #Instrument
        instrument.n_scans = file_data[0]['metadata']['n_scans']
        instrument.dwell_time = file_data[0]['metadata']['dwell_time']
        instrument.excitation_energy = file_data[0]['metadata']['excitation_energy']

        if file_data[0]['metadata']['source_label']:
            instrument.source_label = file_data[0]['metadata']['source_label']
        
        author_generated.author_name = file_data[0]['metadata']['author']
        author_generated.group_name = file_data[0]['metadata']['group_name']
        author_generated.sample_id = file_data[0]['metadata']['sample']
        author_generated.experiment_id = file_data[0]['metadata']['experiment_id']
        author_generated.timestamp = file_data[0]['metadata']['timestamp']

        #Data Header
        for dlabel in file_data[0]['metadata']['data_labels']: 
            data_header.channel_id = str(dlabel['channel_id'])
            data_header.label = dlabel['label']
            data_header.unit = dlabel['unit']

        #Reading columns
        numerical_values = data.m_create(NumericalValues)
        numerical_values.data = file_data[0]['data'][0]
        


        # for item in file_data:

        #     measurement = archive.m_create(Measurement)
        #     # measurement.timestamp = datetime.datetime.now()

        #     metadata = measurement.m_create(Metadata)

        #     sample = metadata.m_create(Sample)
        #     sample.spectrum_region = item['metadata']['spectrum_region']

        #     # experiment = metadata.m_create(Experiment)
        #     # experiment.method_type = data[i]['metadata']['method_type']

        #     # instrument = metadata.m_create(Instrument)
        #     # instrument.n_scans = data[i]['metadata']['n_scans']
        #     # instrument.dwell_time = data[i]['metadata']['dwell_time']
        #     # instrument.excitation_energy = data[i]['metadata']['excitation_energy']
            

        #     # try:
        #     #     instrument.source_label = data[i]['metadata']['source_label']
        #     # except KeyError:
        #     #     print("Couldn't find key")

        #     # author_generated = metadata.m_create(AuthorGenerated)
        #     # author_generated.author_name = data[i]['metadata']['author']
        #     # author_generated.group_name = data[i]['metadata']['group_name']
        #     # author_generated.sample_id = data[i]['metadata']['sample']
        #     # author_generated.experiment_id = data[i]['metadata']['experiment_id']
        #     # author_generated.timestamp = data[i]['metadata']['timestamp']

        #     data_header = metadata.m_create(DataHeader)
        #     for dlabel in item['metadata']['data_labels']: 
        #         data_header.channel_id = str(dlabel['channel_id'])
        #         data_header.label = dlabel['label']
        #         data_header.unit = dlabel['unit']

        #     # data = measurement.m_create(Data)

        #     # numerical_values = data.m_create(NumericalValues)
        #     # # numerical_values.data_values = data[0]['data'][0]
        