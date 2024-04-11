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

__authors__ = ["H. Payno"]
__license__ = "MIT"
__date__ = "02/12/2021"


import os

import pytest
from nxtomo.nxobject.nxdetector import ImageKey

from tomwer.core.scan.edfscan import EDFTomoScan
from tomwer.core.utils.scanutils import MockEDF, MockNXtomo
from tomwer.gui.reconstruction.nabu import check


def test_check_dark_series(tmpdir):
    """test check.check_dark_series function"""
    full_edf_path = os.path.join(tmpdir, "my", "aquisition", "folder")
    MockEDF.fastMockAcquisition(full_edf_path)
    edf_scan = EDFTomoScan(full_edf_path)
    with pytest.raises(TypeError):
        assert check.check_dark_series(edf_scan)

    full_hdf5_scan = os.path.join(tmpdir, "hdf5_scan")
    scan = MockNXtomo(
        scan_path=full_hdf5_scan,
        n_proj=20,
        n_ini_proj=20,
        dim=10,
    ).scan
    scan._image_keys = (
        [ImageKey.DARK_FIELD] * 2
        + [ImageKey.PROJECTION] * 4
        + [ImageKey.DARK_FIELD] * 2
    )
    assert check.check_dark_series(scan, logger=None, user_input=False) is False
    scan._image_keys = [ImageKey.DARK_FIELD] * 2 + [ImageKey.PROJECTION] * 4
    assert check.check_dark_series(scan, logger=None, user_input=False) is True
    scan._image_keys = [ImageKey.PROJECTION] * 4
    assert check.check_dark_series(scan, logger=None, user_input=False) is False


def test_check_flat_series(tmpdir):
    """test check.check_flat_series function"""
    full_edf_path = os.path.join(tmpdir, "my", "aquisition", "folder")
    MockEDF.fastMockAcquisition(full_edf_path)
    edf_scan = EDFTomoScan(full_edf_path)
    with pytest.raises(TypeError):
        assert check.check_flat_series(edf_scan)

    full_hdf5_scan = os.path.join(tmpdir, "hdf5_scan")
    scan = MockNXtomo(
        scan_path=full_hdf5_scan,
        n_proj=20,
        n_ini_proj=20,
        dim=10,
    ).scan
    scan._image_keys = (
        [ImageKey.FLAT_FIELD] * 2
        + [ImageKey.PROJECTION] * 4
        + [ImageKey.FLAT_FIELD] * 2
    )
    assert check.check_flat_series(scan, logger=None, user_input=False) is True
    scan._image_keys = [ImageKey.FLAT_FIELD] * 2 + [ImageKey.PROJECTION] * 4
    assert check.check_flat_series(scan, logger=None, user_input=False) is True
    scan._image_keys = [ImageKey.PROJECTION] * 4
    assert check.check_flat_series(scan, logger=None, user_input=False) is False
