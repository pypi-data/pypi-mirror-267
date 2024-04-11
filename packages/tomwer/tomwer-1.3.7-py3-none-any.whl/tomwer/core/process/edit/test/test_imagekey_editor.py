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

import pytest
from nxtomo.nxobject.nxdetector import ImageKey

from tomwer.core.process.edit.imagekeyeditor import (
    ImageKeyEditorTask,
    ImageKeyUpgraderTask,
)
from tomwer.core.scan.nxtomoscan import NXtomoScan
from tomwer.core.utils.scanutils import MockNXtomo


class TestImageKeyEditor(unittest.TestCase):
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
        process = ImageKeyEditorTask(
            inputs={
                "data": self.scan,
                "serialize_output_data": False,
                "configuration": {
                    "modifications": {
                        0: ImageKey.INVALID.value,
                        3: ImageKey.ALIGNMENT.value,
                    },
                },
            }
        )
        process.definition()
        process.program_version()
        process.program_name()
        process.run()


def test_ImageKeyUpgraderTask(tmp_path):
    """
    test ImageKeyUpgraderTask task
    """
    test_dir = tmp_path / "test_image_key_upgrader"
    os.makedirs(test_dir)
    scan = MockNXtomo(
        scan_path=test_dir,
        n_proj=20,
        n_ini_proj=20,
        create_ini_dark=False,
    ).scan

    operations = {
        ImageKey.PROJECTION: ImageKey.DARK_FIELD,
    }

    with pytest.raises(TypeError):
        ImageKeyUpgraderTask(
            inputs={
                "data": None,
                "operations": operations,
            },
        ).run()

    with pytest.raises(TypeError):
        ImageKeyUpgraderTask(
            inputs={
                "data": scan,
                "operations": None,
            },
        ).run()

    task = ImageKeyUpgraderTask(
        inputs={
            "data": scan,
            "operations": operations,
        },
    )
    task.run()

    scan = NXtomoScan(scan.master_file, scan.entry)
    assert len(scan.projections) == 0
    assert len(scan.darks) == 20
