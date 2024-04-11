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
__date__ = "17/06/2021"


import gc
import os
import pickle
import shutil
import tempfile

from orangecanvas.scheme.readwrite import literal_dumps
from silx.gui import qt
from silx.gui.utils.testutils import TestCaseQt

from orangecontrib.tomwer.widgets.control.DataSelectorOW import DataSelectorOW
from tomwer.core.utils.scanutils import MockNXtomo
from tomwer.synctools.axis import QAxisRP


class TestDataSelectorOw(TestCaseQt):
    def setUp(self):
        super().setUp()
        self.tempdir = tempfile.mkdtemp()
        dim = 10
        mock = MockNXtomo(
            scan_path=os.path.join(self.tempdir, "scan1"),
            n_proj=10,
            n_ini_proj=10,
            scan_range=180,
            dim=dim,
        )
        self.scan1 = mock.scan
        mock = MockNXtomo(
            scan_path=os.path.join(self.tempdir, "scan2"),
            n_proj=10,
            n_ini_proj=10,
            scan_range=180,
            dim=dim,
        )
        self.scan2 = mock.scan
        self.widget = DataSelectorOW()

    def tearDown(self):
        self.widget.setAttribute(qt.Qt.WA_DeleteOnClose)
        self.widget.close()
        self.widget = None
        shutil.rmtree(self.tempdir)
        gc.collect()

    def test(self):
        for scan in (self.scan1, self.scan2):
            assert scan.axis_params is None
            scan.axis_params = QAxisRP()
            self.widget.add(scan)
            self.qapp.processEvents()
            scan_1_identifier = scan.get_identifier()
            assert scan_1_identifier.to_str() in self.widget.widget.dataList._myitems
            item = self.widget.widget.dataList._myitems[scan_1_identifier.to_str()]
            data_obj = item.data(qt.Qt.UserRole)
            assert id(scan) == id(data_obj)
            assert scan.axis_params is not None
        self.widget.selectAll()
        self.widget.send()
        self.qapp.processEvents()

        # test serialization
        assert len(self.widget._scanIDs) == 2
        pickle.dumps(self.widget._scanIDs)
        literal_dumps(self.widget._scanIDs)
