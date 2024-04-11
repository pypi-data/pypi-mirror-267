# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2017-2021 European Synchrotron Radiation Facility
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# ###########################################################################*/

__authors__ = ["H. Payno"]
__license__ = "MIT"
__date__ = "18/06/2021"


import os
import shutil
import tempfile
import unittest

from tomwer.core.process.script.python import PythonScript
from tomwer.core.utils.scanutils import MockNXtomo


class TestPythonScript(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.mkdtemp()
        dim = 10
        mock = MockNXtomo(
            scan_path=os.path.join(self.tempdir, "scan1"),
            n_proj=10,
            n_ini_proj=10,
            scan_range=180,
            dim=dim,
        )
        self.scan = mock.scan

    def tearDown(self):
        shutil.rmtree(self.tempdir)

    def test(self):
        process = PythonScript(inputs={"data": self.scan})
        process.definition()
        process.program_version()
        process.program_name()
        # TODO: configuration should be passed in inputs during construction
        process.set_configuration(
            {
                "scriptText": "print('toto')",
            }
        )

        process.run()
