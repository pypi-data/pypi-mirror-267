from tomwer.tests.conftest import qtapp  # noqa F401
from tomwer.gui.icat.gallery import GalleryWidget


def test_GalleryWidget(
    qtapp,  # noqa F811
):
    widget = GalleryWidget()
    assert widget.getConfiguration() == {
        "beamline": "bm05",
        "beamline_auto_update": True,
        "dataset": "",
        "dataset_auto_update": True,
        "proposal": "",
        "proposal_auto_update": True,
        "output_format": "png",
        "output_location_mode": "dataset gallery",
        "custom_output": "",
        "overwrite": True,
        "binning": "16x16",
    }

    new_config = {
        "beamline": "id19",
        "beamline_auto_update": False,
        "dataset": "my_dataset",
        "dataset_auto_update": False,
        "proposal": "inh99",
        "proposal_auto_update": False,
        "output_location_mode": "custom",
        "output_format": "jpg",
        "custom_output": "",
        "overwrite": False,
        "binning": "4x4",
    }
    widget.setConfiguration(new_config)
    assert widget.getConfiguration() == new_config
