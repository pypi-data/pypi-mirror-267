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
__date__ = "21/06/2021"


import gc
import os
import shutil
import tempfile

from orangecanvas.scheme.readwrite import literal_dumps
from silx.gui import qt
from silx.gui.utils.testutils import TestCaseQt

from orangecontrib.tomwer.widgets.visualization.DataViewerOW import DataViewerOW
from tomwer.core.utils.scanutils import MockNXtomo


class TestDataViewerOW(TestCaseQt):
    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp()
        self.scan = MockNXtomo(
            scan_path=os.path.join(self.tmp_dir, "myscan"),
            n_proj=20,
            n_ini_proj=20,
            dim=10,
        ).scan
        self.widget = DataViewerOW()

    def tearDown(self):
        self.widget.setAttribute(qt.Qt.WA_DeleteOnClose)
        self.widget.close()
        self.widget = None
        shutil.rmtree(self.tmp_dir)
        self.qapp.processEvents()
        gc.collect()

    def test(self):
        self.widget.addScan(self.scan)
        for mode in (
            "projections-radios",
            "slices",
            "raw darks",
            "raw flats",
            "reduced darks",
            "reduced flats",
        ):
            self.widget.viewer.setDisplayMode(mode)
            self.qapp.processEvents()

    def test_literal_dumps(self):
        """
        test settings are correcly dump to literals (and load)
        """
        self.widget._updateSettings()
        config = self.widget._viewer_config
        literal_dumps(config)
        self.widget._setSettings(config)
