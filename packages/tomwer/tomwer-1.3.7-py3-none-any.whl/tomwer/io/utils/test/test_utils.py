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
"""
contains utils for inputs and outputs
"""

__authors__ = ["H. Payno"]
__license__ = "MIT"
__date__ = "15/12/2021"

import os

import h5py
import numpy
from silx.io.url import DataUrl
from tomoscan.io import HDF5File

from tomwer.core.utils import scanutils
from tomwer.io.utils import (
    get_default_directory,
    get_linked_files_with_entry,
    get_slice_data,
)


def test_get_linked_files_with_entry(tmp_path):
    """test get_linked_files_with_entry function"""
    dir_test = tmp_path / "sub"
    dir_test.mkdir()

    layout = h5py.VirtualLayout(shape=(4, 10, 10), dtype="i4")
    for i_file in range(4):
        file_name = os.path.join(dir_test, f"file_{i_file}.hdf5")
        with HDF5File(file_name, "w") as h5s:
            h5s.create_dataset("data", (10, 10), "i4", numpy.ones((10, 10)))
            vsource = h5py.VirtualSource(file_name, "data", shape=(10, 10))
            layout[i_file] = vsource

    test_with_vds = os.path.join(dir_test, "file_with_vds")
    with HDF5File(test_with_vds, "w") as h5s:
        h5s.create_virtual_dataset("vdata", layout, fillvalue=-1)

    assert len(get_linked_files_with_entry(test_with_vds, "vdata")) == 4


def test_get_default_directory():
    get_default_directory()


def test_get_slice_data_vol(tmp_path):
    """test load of a .vol file"""
    dir_test = tmp_path / "test_vol"
    dir_test.mkdir()
    vol_file_path = os.path.join(dir_test, "volume.vol")
    vol_info_file_path = os.path.join(dir_test, "volume.vol.info")

    shape = (4, 50, 20)
    data = numpy.ones(shape)
    data.astype(numpy.float32).tofile(vol_file_path)
    scanutils.MockEDF._createVolInfoFile(
        filePath=vol_info_file_path,
        shape=shape,
    )

    vol = get_slice_data(DataUrl(file_path=vol_file_path))
    assert vol is not None
    assert vol.shape == shape
    vol = get_slice_data(DataUrl(file_path=vol_info_file_path))
    assert vol is not None
    assert vol.shape == shape
