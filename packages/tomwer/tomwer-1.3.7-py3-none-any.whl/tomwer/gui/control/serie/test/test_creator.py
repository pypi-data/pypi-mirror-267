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
__date__ = "12/01/2022"


import os
import shutil
import tempfile

from silx.gui import qt
from silx.gui.utils.testutils import SignalListener, TestCaseQt
from tomoscan.serie import Serie

from tomwer.core.scan.nxtomoscan import NXtomoScan
from tomwer.core.utils.scanutils import MockEDF, MockNXtomo
from tomwer.core.volume.hdf5volume import HDF5Volume
from tomwer.gui.control.serie.seriecreator import (
    SerieDefinition,
    SerieHistoryDialog,
    SerieManualControlDialog,
    SerieManualFromTomoObj,
    SerieTree,
    SerieWidget,
)


class _MockScanBase:
    def init(self):
        n_hdf5_scan = 11
        self._scans = []
        self._root_dir = tempfile.mkdtemp()
        for i_scan in range(n_hdf5_scan):
            scan_path = os.path.join(self._root_dir, f"scan_{i_scan}")
            scan = MockNXtomo(scan_path=scan_path, n_proj=10, n_ini_proj=0).scan
            self._scans.append(scan)
        n_edf_scan = 4
        for i_scan in range(n_edf_scan):
            scan_path = os.path.join(self._root_dir, f"scan_{i_scan}")
            scan = MockEDF.mockScan(
                scanID=scan_path,
                nRadio=10,
                dim=10,
            )
            self._scans.append(scan)

    def close(self):
        shutil.rmtree(self._root_dir)


class _MockSerieBase(_MockScanBase):
    def init(self):
        super().init()
        self._series = [
            Serie("serie1", self._scans[0:1], use_identifiers=True),
            Serie("serie2", self._scans[1:5], use_identifiers=False),
            Serie("serie3", self._scans[5:11], use_identifiers=True),
            Serie("serie4", self._scans[8:11], use_identifiers=True),
            Serie("serie5", self._scans[-2:-1], use_identifiers=False),
            Serie("serie6", self._scans[-5:], use_identifiers=True),
        ]

    def close(self):
        self._series.clear()
        super().close()


class TestSerieTree(TestCaseQt, _MockSerieBase):
    """Test the SerieTree widget"""

    def setUp(self):
        super().setUp()
        super().init()
        self._widget = SerieTree()

    def tearDown(self):
        self._widget.setAttribute(qt.Qt.WA_DeleteOnClose)
        self._widget.close()
        self._widget = None
        super().close()
        super().tearDown()

    def test_add_remove(self):
        """Test adding and removing serie"""
        self._widget.show()
        self.qWaitForWindowExposed(self._widget)
        for serie in self._series:
            self._widget.addSerie(serie)
        assert self._widget.n_series == 6
        self._widget.removeSerie(self._series[3])
        assert self._widget.n_series == 5
        self._widget.removeSerie(self._series[2])
        self._widget.removeSerie(self._series[1])
        self._widget.removeSerie(self._series[0])
        # make sure no error is raised if we try to remove twine the same serie
        self._widget.removeSerie(self._series[0])
        assert self._widget.n_series == 2
        self._widget.addSerie(self._series[1])
        self._widget.addSerie(self._series[2])
        assert self._widget.n_series == 4

    def test_selection(self):
        """Test selection of the SerieTree"""
        self._widget.show()
        self.qWaitForWindowExposed(self._widget)
        for serie in self._series:
            self._widget.addSerie(serie)

        selection = (self._series[2], self._series[3])
        self._widget.setSelectedSeries(selection)
        assert self._widget.getSelectedSeries() == selection
        self._widget.clearSelection()
        assert self._widget.getSelectedSeries() == ()


class TestSerieHistoryDialog(TestCaseQt, _MockSerieBase):
    """Test the SerieHistoryDialog"""

    def setUp(self):
        super().setUp()
        super().init()
        self._widget = SerieHistoryDialog()

        # create listener for the nabu widget
        self.signal_listener = SignalListener()

        # connect signal / slot
        self._widget.sigSerieSend.connect(self.signal_listener)

    def tearDown(self):
        self._widget.setAttribute(qt.Qt.WA_DeleteOnClose)
        self._widget.close()
        self._widget = None
        super().close()
        super().tearDown()

    def test(self):
        self._widget.show()
        self.qWaitForWindowExposed(self._widget)
        for serie in self._series:
            self._widget.addSerie(serie)

        selection = (self._series[0], self._series[4])
        self._widget.setSelectedSeries(selection)
        assert self._widget.getSelectedSeries() == selection
        assert self.signal_listener.callCount() == 0
        self._widget._sendButton.clicked.emit()
        self.qapp.processEvents()
        assert self.signal_listener.callCount() == 2
        assert self._widget.getSelectedSeries() == selection
        self.signal_listener.clear()
        self._widget._clearButton.clicked.emit()
        assert self._widget.getSelectedSeries() == ()
        assert self.signal_listener.callCount() == 0
        self._widget._sendButton.clicked.emit()
        assert self.signal_listener.callCount() == 0


class TestSerieDefinition(TestCaseQt):
    def setUp(self):
        super().setUp()
        self._widget = SerieDefinition()

    def tearDown(self):
        self._widget.setAttribute(qt.Qt.WA_DeleteOnClose)
        self._widget.close()
        self._widget = None
        super().tearDown()

    def test_manual_selection(self):
        self._widget.setMode("manual")
        self._widget.show()
        self.qWaitForWindowExposed(self._widget)
        assert not self._widget._automaticDefWidget.isVisible()
        assert self._widget._manualDefWidget.isVisible()

    def test_automatic_selection(self):
        self._widget.setMode("auto")
        self._widget.show()
        self.qWaitForWindowExposed(self._widget)
        assert self._widget._automaticDefWidget.isVisible()
        assert not self._widget._manualDefWidget.isVisible()


class TestSerieManualDefinitionDialog(TestCaseQt, _MockScanBase):
    """Test interaction with the serie manual definition"""

    def setUp(self):
        self._widget = SerieManualControlDialog()
        super().setUp()
        super().init()

    def tearDown(self):
        self._widget.setAttribute(qt.Qt.WA_DeleteOnClose)
        self._widget.close()
        self._widget = None
        super().close()
        super().tearDown()

    def test(self):
        self._widget.show()
        self.qWaitForWindowExposed(self._widget)

        self._widget.setSerieName("serie test")
        self.qapp.processEvents()
        assert self._widget.getSerieName() == "serie test"

        self._widget._mainWidget._newSerieWidget._serieTree.rootItem.setText(
            0, "new serie"
        )
        self.qapp.processEvents()
        assert self._widget.getSerieName() == "new serie"

        for scan in self._scans[:5]:
            self._widget.addScan(scan)

        self.assertEqual(self._widget.n_tomo_objs, len(self._scans[:5]))
        self._widget.removeScan(self._scans[0])
        self.assertEqual(self._widget.n_tomo_objs, len(self._scans[:5]) - 1)

        series_scan = tuple(self._scans[1:5])
        assert isinstance(series_scan, tuple)

        current_serie = self._widget.getSerie(use_identifiers=True)
        assert isinstance(current_serie, Serie)
        serie_test_1 = Serie(
            name="new serie", iterable=series_scan, use_identifiers=True
        )

        self.assertEqual(serie_test_1, current_serie)
        serie_test_2 = Serie(name="test", iterable=series_scan, use_identifiers=True)
        assert serie_test_2.name == "test"
        assert current_serie.name == "new serie"
        self.assertNotEqual(serie_test_2, current_serie)

        self._widget.setSelectedScans([self._scans[2]])
        self._widget.getSelectedScans() == (self._scans[2],)
        self._widget.removeSelectedScans()
        self.assertEqual(self._widget.n_tomo_objs, len(self._scans[:5]) - 2)
        self._widget.getSelectedScans() == tuple()

        self._widget.clearSerie()
        self.assertEqual(self._widget.n_tomo_objs, 0)
        self.assertEqual(Serie(name="new serie"), self._widget.getSerie())

        # test adding an nx file
        hdf5_scan = self._scans[0]
        assert isinstance(hdf5_scan, NXtomoScan)
        self._widget.addScanFromNxFile(hdf5_scan.master_file)
        self.assertEqual(self._widget.n_tomo_objs, 1)


class TestSerieWidget(TestCaseQt, _MockSerieBase):
    """
    Test the SerieWidget
    """

    def setUp(self):
        super().setUp()
        super().init()
        self._widget = SerieWidget()
        # create listeners
        self.signal_send_serie_listener = SignalListener()
        self.signal_serie_changed_listener = SignalListener()
        self.signal_history_changed_listener = SignalListener()

        # connect signal / slot
        self._widget.sigSerieSend.connect(self.signal_send_serie_listener)
        self._widget.sigCurrentSerieChanged.connect(self.signal_serie_changed_listener)
        self._widget.sigHistoryChanged.connect(self.signal_history_changed_listener)

    def tearDown(self):
        self._widget.sigSerieSend.disconnect(self.signal_send_serie_listener)
        self._widget.sigCurrentSerieChanged.disconnect(
            self.signal_serie_changed_listener
        )
        self._widget.sigHistoryChanged.disconnect(self.signal_history_changed_listener)

        self.signal_send_serie_listener = None
        self.signal_serie_changed_listener = None
        self.signal_history_changed_listener = None

        self._widget.setAttribute(qt.Qt.WA_DeleteOnClose)
        self._widget.close()
        self._widget = None
        super().close()
        super().tearDown()

    def test(self):
        self._widget.show()
        self.qWaitForWindowExposed(self._widget)
        self._series[3].name = "toto serie"
        for serie in self._series[2:5]:
            self._widget.getHistoryWidget().addSerie(serie)
        self._widget.setMode("history")
        self._widget.setMode("serie definition", "manual")
        self._widget.getDefinitionWidget().getManualDefinitionWidget().setSerieName(
            "new serie"
        )

        self.assertEqual(
            len(
                self._widget.getDefinitionWidget()
                .getManualDefinitionWidget()
                .getSerie()
            ),
            0,
        )

        self._widget.getHistoryWidget().setSelectedSeries(
            [
                self._series[3],
            ]
        )
        assert len(self._widget.getHistoryWidget().getSelectedSeries()) == 1

        self.signal_serie_changed_listener.clear()
        self._widget.getHistoryWidget().editSelected()
        self.qapp.processEvents()
        assert self.signal_serie_changed_listener.callCount() == 1

        self.assertEqual(
            self._widget.getDefinitionWidget()
            .getManualDefinitionWidget()
            .getSerie()
            .name,
            "toto serie",
        )

        self.assertEqual(
            self._widget.getDefinitionWidget()
            .getManualDefinitionWidget()
            .getSerie(use_identifiers=True),
            self._series[3],
        )

        self.signal_serie_changed_listener.clear()
        self._widget.getDefinitionWidget().getManualDefinitionWidget().addToCurrentSerie(
            self._scans[0]
        )
        self.qapp.processEvents()
        assert self.signal_serie_changed_listener.callCount() == 1

        expected_scans = self._scans[8:11]
        expected_scans.append(self._scans[0])
        expected_serie = Serie("toto serie", expected_scans, use_identifiers=True)

        self.assertEqual(
            self._widget.getDefinitionWidget()
            .getManualDefinitionWidget()
            .getSerie(use_identifiers=True),
            expected_serie,
        )

        # check send edited serie
        self.signal_history_changed_listener.clear()
        self.signal_send_serie_listener.clear()
        self.qapp.processEvents()

        # check send selected from the history
        self.signal_send_serie_listener.clear()
        self._widget.getHistoryWidget().setSelectedSeries(
            [
                self._series[4],
            ]
        )
        assert len(self._widget.getHistoryWidget().getSelectedSeries()) == 1
        self._widget.getHistoryWidget().sendSelected()
        assert self.signal_send_serie_listener.callCount() == 1


class TestSerieManualFromTomoObj(TestCaseQt):
    """
    test the SerieManualFromTomoObj widget
    """

    def setUp(self):
        super().setUp()
        self._tmp_dir = tempfile.mkdtemp()
        self._widget = SerieManualFromTomoObj()
        self._volume_1 = HDF5Volume(
            file_path=os.path.join(self._tmp_dir, "vol1.hdf5"),
            data_path="data",
        )
        self._volume_2 = HDF5Volume(
            file_path=os.path.join(self._tmp_dir, "vol2.hdf"),
            data_path="data",
        )
        self._volume_3 = HDF5Volume(
            file_path=os.path.join(self._tmp_dir, "vol3.nx"),
            data_path="data",
        )
        self._scan_1 = MockNXtomo(
            scan_path=os.path.join(self._tmp_dir, "scan_1"), n_proj=10, n_ini_proj=10
        ).scan
        self._scan_2 = MockNXtomo(
            scan_path=os.path.join(self._tmp_dir, "scan_2"), n_proj=10, n_ini_proj=10
        ).scan

    def tearDown(self):
        shutil.rmtree(self._tmp_dir)
        self._widget.setAttribute(qt.Qt.WA_DeleteOnClose)
        self._widget.close()
        self._widget = None
        return super().tearDown()

    def test(self):
        self._widget.show()
        for tomo_obj in (
            self._volume_1,
            self._volume_2,
            self._volume_3,
            self._scan_1,
            self._scan_2,
        ):
            self._widget.addTomoObj(tomo_obj)

        current_serie = self._widget.getSerie()
        assert isinstance(current_serie, Serie)
        assert len(current_serie) == 0

        for tomo_obj in (self._volume_1, self._volume_2):
            self._widget.addToCurrentSerie(tomo_obj)

        current_serie = self._widget.getSerie()
        assert isinstance(current_serie, Serie)
        assert len(current_serie) == 2
