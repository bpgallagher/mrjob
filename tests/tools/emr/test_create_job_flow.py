# Copyright 2009-2012 Yelp
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Test the idle job flow terminator"""

from __future__ import with_statement

from datetime import datetime
from datetime import timedelta
from StringIO import StringIO
import sys

from mrjob.tools.emr.create_job_flow import main as create_job_flow_main
from mrjob.tools.emr.create_job_flow import runner_kwargs

from tests.quiet import no_handlers_for_logger
from tests.test_emr import MockEMRAndS3TestCase


class JobFlowInspectionTestCase(MockEMRAndS3TestCase):

    def setUp(self):
        super(JobFlowInspectionTestCase, self).setUp()
        self._original_argv = sys.argv
        self._original_stdout = sys.stdout
        self.stdout = StringIO()
        sys.stdout = self.stdout

    def tearDown(self):
        super(JobFlowInspectionTestCase, self).tearDown()
        sys.argv = self._original_argv
        sys.stdout = self._original_stdout

    def monkey_patch_argv(self, *args):
        sys.argv = [sys.argv[0]] + list(args)

    def test_runner_kwargs(self):
        sys.argv = [sys.argv[0], '--verbose']
        self.assertEqual(
            runner_kwargs(),
            {'additional_emr_info': None,
             'aws_availability_zone': None,
             'aws_region': None,
             'bootstrap_actions': [],
             'bootstrap_cmds': [],
             'bootstrap_files': [],
             'bootstrap_mrjob': None,
             'bootstrap_python_packages': [],
             'conf_path': None,
             'ec2_core_instance_bid_price': None,
             'ec2_core_instance_type': None,
             'ec2_instance_type': None,
             'ec2_key_pair': None,
             'ec2_master_instance_bid_price': None,
             'ec2_master_instance_type': None,
             'ec2_task_instance_bid_price': None,
             'ec2_task_instance_type': None,
             'emr_endpoint': None,
             'emr_job_flow_pool_name': None,
             'enable_emr_debugging': None,
             'hadoop_version': None,
             'label': None,
             'num_ec2_core_instances': None,
             'num_ec2_instances': None,
             'num_ec2_task_instances': None,
             'owner': None,
             'pool_emr_job_flows': None,
             's3_endpoint': None,
             's3_log_uri': None,
             's3_scratch_uri': None,
             's3_sync_wait_time': None})

    def test_create_job_flow(self):
        self.add_mock_s3_data({'walrus': {}})
        self.monkey_patch_argv(
            '--quiet', '--no-conf',
            '--s3-sync-wait-time', '0',
            '--s3-scratch-uri', 's3://walrus/tmp')
        create_job_flow_main()
        self.assertEqual(list(self.mock_emr_job_flows.keys()), ['j-MOCKJOBFLOW0'])
        self.assertEqual(self.stdout.getvalue(), 'j-MOCKJOBFLOW0\n')
