# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2017-2019 European Synchrotron Radiation Facility
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
__date__ = "10/12/2021"


import asyncio
import os
import shutil
import tempfile

import pytest
from silx.gui import qt
from silx.gui.utils.testutils import TestCaseQt

from orangecontrib.tomwer.widgets.cluster.FutureSupervisorOW import FutureSupervisorOW
from tomwer.core.futureobject import FutureTomwerObject
from tomwer.core.utils.scanutils import MockNXtomo
from tomwer.tests.utils import skip_gui_test


@pytest.mark.skipif(skip_gui_test(), reason="skip gui test")
class TestFutureSupervisorOW(TestCaseQt):
    """Test that the axis widget work correctly"""

    def setUp(self):
        super().setUp()
        self._window = FutureSupervisorOW()
        self.tempdir = tempfile.mkdtemp()

        # set up scans
        self._scans = []
        self._future_tomo_objs = []
        for i in range(5):
            # create scan
            scan = MockNXtomo(
                scan_path=os.path.join(self.tempdir, f"scan_test{i}"),
                n_proj=10,
                n_ini_proj=10,
                create_ini_dark=False,
                create_ini_flat=False,
                dim=10,
            ).scan
            self._scans.append(scan)

            # create future
            future = asyncio.Future()
            if i == 1:
                future.set_result(None)
            self._future_tomo_objs.append(
                FutureTomwerObject(
                    tomo_obj=scan,
                    futures=(future,),
                )
            )

    def tearDown(self):
        self._window.setAttribute(qt.Qt.WA_DeleteOnClose)
        self._window.close()
        self._window = None
        shutil.rmtree(self.tempdir)
        self._scans.clear()
        self._future_tomo_objs.clear()
        super().tearDown()
