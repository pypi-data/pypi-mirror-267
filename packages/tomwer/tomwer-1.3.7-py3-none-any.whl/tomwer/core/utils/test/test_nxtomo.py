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


import pytest
from nxtomo.nxobject.nxdetector import ImageKey

from tomwer.core.utils.nxtomoutils import get_n_series


def test_get_n_series():
    """test tomwer.core.utils.nxtomoutils.get_n_series function"""
    array_1 = (
        [ImageKey.DARK_FIELD] * 2
        + [ImageKey.FLAT_FIELD]
        + [ImageKey.PROJECTION] * 4
        + [ImageKey.FLAT_FIELD]
    )

    with pytest.raises(ValueError):
        get_n_series(array_1, ImageKey.INVALID)
    with pytest.raises(ValueError):
        get_n_series(array_1, 3)

    assert len(array_1) == 8
    assert get_n_series(array_1, ImageKey.DARK_FIELD) == 1
    assert get_n_series(array_1, ImageKey.FLAT_FIELD) == 2
    assert get_n_series(array_1, ImageKey.PROJECTION) == 1
    assert get_n_series(array_1, 0) == 1

    array_2 = (
        [ImageKey.FLAT_FIELD.value]
        + [ImageKey.PROJECTION.value] * 4
        + [ImageKey.INVALID.value] * 2
        + [ImageKey.PROJECTION.value] * 3
        + [ImageKey.FLAT_FIELD.value]
    )
    assert get_n_series(array_2, ImageKey.DARK_FIELD) == 0
    assert get_n_series(array_2, ImageKey.PROJECTION) == 1
    assert get_n_series(array_2, ImageKey.FLAT_FIELD) == 2
