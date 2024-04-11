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
__date__ = "16/12/2021"


import gc
import os
import pickle
import tempfile
import time

import numpy
from orangecanvas.scheme.readwrite import literal_dumps
from silx.gui import qt
from silx.gui.utils.testutils import TestCaseQt

from orangecontrib.tomwer.widgets.reconstruction.CastNabuVolumeOW import (
    CastNabuVolumeOW,
)
from tomwer.core.volume.rawvolume import RawVolume


class TestCastVolumeOW(TestCaseQt):
    def setUp(self):
        super().setUp()
        self._window = CastNabuVolumeOW()

    def tearDown(self):
        self._window.setAttribute(qt.Qt.WA_DeleteOnClose)
        self._window.close()
        self._window = None
        gc.collect()

    def test(self):
        self._window.show()
        self.qWaitForWindowExposed(self._window)

    def test_serializing(self):
        pickle.dumps(self._window.getConfiguration())

    def test_literal_dumps(self):
        literal_dumps(self._window.getConfiguration())

    def test_cast_volume(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            input_dir = os.path.join(tmp_dir, "input")
            os.makedirs(input_dir)

            volume = RawVolume(
                file_path=os.path.join(input_dir, "vol_file.vol"),
                data=numpy.linspace(0, 10, 100 * 100 * 3, dtype=numpy.float32).reshape(
                    3, 100, 100
                ),
            )
            volume.save()

            self._window.process_volume(volume)
            while self._window._processingStack.is_computing():
                time.sleep(0.1)
                self.qapp.processEvents()
