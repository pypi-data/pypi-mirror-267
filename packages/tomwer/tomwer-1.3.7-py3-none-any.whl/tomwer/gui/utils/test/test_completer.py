# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2016-2017 European Synchrotron Radiation Facility
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

"""module defining dedicated completer"""


__authors__ = ["H. Payno"]
__license__ = "MIT"
__date__ = "23/03/2022"


import pytest
from silx.gui import qt
from silx.gui.utils.testutils import TestCaseQt

from tomwer.gui.utils.completer import UrlCompleterDialog
from tomwer.tests.utils import skip_gui_test


@pytest.mark.skipif(skip_gui_test(), reason="skip gui test")
class TestUrlCompleterDialog(TestCaseQt):
    def setUp(self):
        super().setUp()
        self._urls = (
            "test",
            "test1",
            "test2",
        )
        self._dialog = UrlCompleterDialog(
            urls=self._urls,
            current_url="test",
        )

    def tearDown(self):
        self._dialog.setAttribute(qt.Qt.WA_DeleteOnClose)
        self._dialog.close()
        self._dialog = None
        super().tearDown()

    def test(self):
        """simple test on the dialog behavior"""
        assert self._dialog._buttons.button(qt.QDialogButtonBox.Ok).isEnabled()
        self._dialog._completerWidget.setText("toto")
        self.qapp.processEvents()
        assert not self._dialog._buttons.button(qt.QDialogButtonBox.Ok).isEnabled()
