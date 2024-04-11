import os
import tempfile

from silx.gui import qt
from silx.gui.utils.testutils import TestCaseQt
from tomoscan.serie import Serie

from tomwer.gui.stitching.stitching import ZStitchingWindow
from tomwer.gui.stitching.tests.utils import create_scans_z_serie


class TestAxis_N_Params(TestCaseQt):
    """
    Test definition of an axis shift research parameters
    """

    def setUp(self):
        super().setUp()
        self._window = ZStitchingWindow()

        self._tmp_path = tempfile.mkdtemp()
        self.axis_0_positions = (90, 0.0, -90.0)
        self.axis_2_positions = (0.0, 0.0, 0.0)
        pixel_size = 1.0

        self.output_file_path = os.path.join(self._tmp_path, "output", "stitched.nx")
        self._input_dir = os.path.join(self._tmp_path, "input")

        self._scans = create_scans_z_serie(
            output_dir=self._input_dir,
            z_positions_m=self.axis_0_positions,
            x_positions_m=self.axis_2_positions,
            shifts=((0.0, 0.0), (-90.0, 0.0), (-180.0, 0.0)),
            pixel_size=pixel_size,
            raw_frame_width=280,
            final_frame_width=100,
        )
        self._serie = Serie("z-serie", self._scans)

    def tearDown(self):
        self._window.setAttribute(qt.Qt.WA_DeleteOnClose)
        self._window.close()
        self._window = None
        while self.qapp.hasPendingEvents():
            self.qapp.processEvents()

    def test(self):
        self._window.show()
        for scan in self._scans:
            self._window.addTomoObj(scan)
        self._window.clean()
        self._window.setSerie(self._serie)

        # test dumping and loading configuration to a file
        with tempfile.TemporaryDirectory() as dump_dir:
            config_file = os.path.join(dump_dir, "configuration.cfg")
            self._window._saveSettings(file_path=config_file)
            assert os.path.exists(config_file)
            self._window._loadSettings(config_file)
            # remove configuration
            self._window.clean()
            assert len(self._window._widget._mainWidget.getTomoObjs()) == 0
            # reload it
            self._window._loadSettings(file_path=config_file)
            assert len(self._window._widget._mainWidget.getTomoObjs()) == len(
                self._serie
            )
