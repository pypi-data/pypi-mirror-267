import numpy
from tomwer.tests.conftest import nxtomo_scan_180  # noqa F811
from tomwer.core.process.icat.createscreenshots import (
    CreateRawDataScreenshotsTask,
    select_angles,
)


def test_CreateRawDataScreenshotsTask(nxtomo_scan_180):  # noqa F811
    """
    test CreateRawDataScreenshotsTask task
    """
    # test nothing requested
    task = CreateRawDataScreenshotsTask(
        inputs={
            "data": nxtomo_scan_180,
            "raw_projections_required": False,
            "raw_darks_required": False,
            "raw_flats_required": False,
        }
    )
    task.run()
    assert len(task.outputs.screenshots.screenshots) == 0

    # test only dark requested
    task = CreateRawDataScreenshotsTask(
        inputs={
            "data": nxtomo_scan_180,
            "raw_projections_required": False,
            "raw_darks_required": False,
            "raw_flats_required": True,
        }
    )
    task.run()
    assert len(task.outputs.screenshots.screenshots) == 1

    # test only flat requested
    task = CreateRawDataScreenshotsTask(
        inputs={
            "data": nxtomo_scan_180,
            "raw_projections_required": False,
            "raw_darks_required": True,
            "raw_flats_required": False,
        }
    )
    task.run()
    assert len(task.outputs.screenshots.screenshots) == 1

    # test only projection requested
    task = CreateRawDataScreenshotsTask(
        inputs={
            "data": nxtomo_scan_180,
            "raw_projections_required": True,
            "raw_darks_required": False,
            "raw_flats_required": False,
        }
    )
    task.run()
    assert len(task.outputs.screenshots.screenshots) == 2

    # test all requested
    task = CreateRawDataScreenshotsTask(
        inputs={
            "data": nxtomo_scan_180,
            "raw_projections_required": True,
            "raw_darks_required": True,
            "raw_flats_required": True,
            "raw_projections_each": 10,
        }
    )
    task.run()
    assert len(task.outputs.screenshots.screenshots) == 12


def test_select_angles():
    """test the select_angles function"""
    numpy.testing.assert_allclose(
        select_angles(
            numpy.linspace(start=-20, stop=40, num=201, endpoint=True), each_angle=20
        ),
        numpy.array([-20, 0.1, 19.9, 40]),
    )

    assert select_angles((), each_angle=20) == ()
    assert select_angles((10,), each_angle=10) == (10,)
    angles = select_angles(
        numpy.linspace(start=0, stop=10, num=400, endpoint=False), each_angle=1
    )
    assert len(angles) == 11
    assert numpy.isclose(angles[0], 0, atol=0.1)
    assert numpy.isclose(angles[-1], 10, atol=0.1)


# def test_CreateRawDataScreenshotsWidgetWorkflow():
#     """
#     test CreateRawDataScreenshotsTask with a MoveScreenshotsToGalleryTask task to make sure the two work well together
#     """
#     raise NotImplementedError
