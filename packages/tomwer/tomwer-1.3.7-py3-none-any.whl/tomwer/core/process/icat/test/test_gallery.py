import os

import h5py
import numpy
import pytest
from silx.io.url import DataUrl

from tomwer.core.process.icat.gallery import (
    SaveScreenshotsToGalleryTask,
    IcatScreenshots,
    deduce_dataset_gallery_location,
    deduce_proposal_GALLERY_location,
    select_screenshot_from_volume,
    PROPOSAL_GALLERY_DIR_NAME,
)
from tomwer.core.scan.edfscan import EDFTomoScan
from tomwer.core.scan.nxtomoscan import NXtomoScan
from tomwer.core.volume.edfvolume import EDFVolume
from tomwer.core.volume.hdf5volume import HDF5Volume


def test_deduce_dataset_gallery_dir():
    """test the deduce_gallery_dir function"""
    assert (
        deduce_dataset_gallery_location(
            NXtomoScan(scan="/path/to/PROCESSED_DATA/my_scan.nx", entry="entry")
        )
        == "/path/to/PROCESSED_DATA/gallery"
    )
    assert (
        deduce_dataset_gallery_location(
            NXtomoScan(scan="/path/to/RAW_DATA/collection/my_scan.nx", entry="entry")
        )
        == "/path/to/PROCESSED_DATA/collection/gallery"
    )
    assert (
        deduce_dataset_gallery_location(
            NXtomoScan(scan="/any/random/path/my_scan.nx", entry="entry")
        )
        == "/any/random/path/gallery"
    )
    assert (
        deduce_dataset_gallery_location(
            EDFTomoScan(scan="/path/to/PROCESSED_DATA/dataset/toto")
        )
        == "/path/to/PROCESSED_DATA/dataset/toto/gallery"
    )
    assert (
        deduce_dataset_gallery_location(EDFTomoScan(scan="/path/to/dataset/toto"))
        == "/path/to/dataset/toto/gallery"
    )


def test_deduce_proposal_gallery_dir():
    """test the deduce_gallery_dir function"""
    assert (
        deduce_proposal_GALLERY_location(
            NXtomoScan(scan="/path/to/PROCESSED_DATA/my_scan.nx", entry="entry")
        )
        == f"/path/to/{PROPOSAL_GALLERY_DIR_NAME}"
    )
    assert (
        deduce_proposal_GALLERY_location(
            NXtomoScan(scan="/path/to/PROCESSED_DATA/dataset/my_scan.nx", entry="entry")
        )
        == f"/path/to/{PROPOSAL_GALLERY_DIR_NAME}/dataset"
    )
    assert (
        deduce_proposal_GALLERY_location(
            NXtomoScan(scan="/any/random/path/my_scan.nx", entry="entry")
        )
        == f"/any/random/path/{PROPOSAL_GALLERY_DIR_NAME}"
    )
    assert (
        deduce_proposal_GALLERY_location(
            EDFTomoScan(scan="/path/to/PROCESSED_DATA/dataset/toto")
        )
        == "/path/to/GALLERY/dataset/toto"
    )
    assert (
        deduce_proposal_GALLERY_location(EDFTomoScan(scan="/path/to/dataset/toto"))
        == "/path/to/dataset/toto/GALLERY"
    )


@pytest.mark.parametrize("MetaVolumeClass", (HDF5Volume, EDFVolume))
def test_select_screenshot_from_volume(MetaVolumeClass, tmp_path):
    """test the 'select_screenshot_from_volume' function"""
    output_dir = tmp_path / "volumes"

    if MetaVolumeClass is HDF5Volume:
        volume = MetaVolumeClass(
            file_path=os.path.join(output_dir, "test.hdf5"),
            data_path="data",
        )
    elif MetaVolumeClass is EDFVolume:
        volume = MetaVolumeClass(folder=os.path.join(output_dir, "folder"))
    else:
        raise NotImplementedError

    # test with 'standard' volume
    ## setup the volume
    volume.data = numpy.arange(1000000).reshape(100, 100, 100)
    volume.save()  # needed because brosing urls check if url exists or not...
    ## make sure we get the expected number of screenshot
    screenshots_as_url = select_screenshot_from_volume(volume=volume)
    assert len(screenshots_as_url) == 3
    ## test slices
    for url in screenshots_as_url.values():
        if isinstance(volume, HDF5Volume):
            assert url.data_slice() in (33, 50, 66)
        elif isinstance(volume, EDFVolume):
            assert url.file_path().endswith(("33.edf", "50.edf", "66.edf"))
        else:
            raise NotImplementedError

    # test with a single frame volume
    volume.data = numpy.arange(100).reshape(1, 10, 10)
    volume.overwrite = True
    volume.save()
    screenshots_as_url = select_screenshot_from_volume(volume=volume)
    ## make sure we have a single screenshot in this case
    screenshot_url = tuple(screenshots_as_url.values())[0]
    if isinstance(volume, HDF5Volume):
        assert screenshot_url.data_slice() == 0
        assert len(screenshots_as_url) == 1
        # warning: for now this doesn't work for EDF because the volume class will not remove any existing slices...
        # which is a clear limitation. But not sure we should remove those either...
    elif isinstance(volume, EDFVolume):
        # warning: for now this doesn't work for EDF because the volume class will not remove any existing slices...
        # which is a clear limitation. But not sure we should remove those either...
        # so here we will still find 3 urls for the screenshot
        pass
    else:
        raise NotImplementedError


def test_MoveScreenshotsToGalleryTask(tmp_path):
    """test the 'MoveScreenshotsToGalleryTask' task"""
    raw_data_dir = tmp_path / "raw_data"
    raw_data_dir.mkdir()
    screenshot_output_data_dir = tmp_path / "screenshot"
    screenshot_output_data_dir.mkdir()

    raw_data_file = raw_data_dir / "data.hdf5"
    with h5py.File(raw_data_file, mode="w") as h5f:
        h5f["data"] = numpy.random.random(100).reshape(10, 10)

    screenshots = IcatScreenshots(
        data_dir=str(screenshot_output_data_dir),
        screenshots={
            "my_screenshot": DataUrl(
                file_path=raw_data_file,
                data_path="data",
                scheme="silx",
            )
        },
        scan=None,
    )

    task = SaveScreenshotsToGalleryTask(
        inputs={
            "screenshots": screenshots,
            "format": "png",
        }
    )
    task.run()

    expected_output_file = os.path.join(screenshot_output_data_dir, "my_screenshot.png")
    assert os.path.exists(expected_output_file)
