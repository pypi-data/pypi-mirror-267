import os
import shutil
import tempfile

import numpy
from nabu.stitching.config import PreProcessedZStitchingConfiguration
from nabu.stitching.z_stitching import PreProcessZStitcher
from silx.gui import qt
from silx.gui.utils.testutils import TestCaseQt
from silx.image.phantomgenerator import PhantomGenerator

from tomwer.gui.stitching.stitching_preview import PreviewStitchingPlot
from tomwer.gui.stitching.tests.utils import create_scans_z_serie


class TestPreview(TestCaseQt):
    def setUp(self):
        super().setUp()
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
        self._stitching_config = PreProcessedZStitchingConfiguration(
            output_file_path=self.output_file_path,
            output_data_path="entry_stitched",
            overwrite_results=True,
            slurm_config=None,
            axis_0_pos_mm=numpy.array(self.axis_0_positions) / 1000,
            axis_2_pos_mm=numpy.array(self.axis_2_positions) / 1000,
            axis_0_pos_px=None,
            axis_1_pos_px=None,
            axis_2_pos_px=None,
            input_scans=self._scans,
            pixel_size=pixel_size,
        )
        self.widget = PreviewStitchingPlot()

    def tearDown(self):
        self.widget.setAttribute(qt.Qt.WA_DeleteOnClose)
        self.widget.close()
        self.widget = None
        shutil.rmtree(self._tmp_path)

    def test(self):
        """
        test the PreviewStitchingPlot
        """
        self.widget.show()
        self.widget._backGroundAction.toggle()
        self.qapp.processEvents()

        stitcher = PreProcessZStitcher(configuration=self._stitching_config)
        stitched_id = stitcher.stitch(store_composition=True)
        assert stitched_id is not None
        composition = stitcher.frame_composition
        assert composition is not None

        self.widget.setStitchedTomoObj(
            tomo_obj_id=stitched_id.to_str(), composition=composition
        )
        self.qapp.processEvents()
        assert self.widget.stitched_image is not None
        assert self.widget.composition_background is not None

        numpy.testing.assert_almost_equal(
            self.widget.stitched_image,
            PhantomGenerator.get2DPhantomSheppLogan(n=280).astype(numpy.float32)
            * 256.0,
        )

        self.widget._backGroundAction.toggle()
        self.qapp.processEvents()
