# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2016 European Synchrotron Radiation Facility
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

__authors__ = ["C.Nemoz", "H.Payno"]
__license__ = "MIT"
__date__ = "18/08/2021"


import os
import tempfile
from glob import glob

from ewoks import execute_graph
from ewokscore.graph import analysis, load_graph
from ewokscore.graph.validate import validate_graph

from tomwer.core.utils.scanutils import HDF5MockContext
from tomwer.core.process.reconstruction.output import PROCESS_FOLDER_NAME

try:
    from nabu.pipeline.fullfield.reconstruction import (  # noqa F401
        FullFieldReconstructor,
    )
except ImportError:
    try:
        from nabu.pipeline.fullfield.local_reconstruction import (  # noqa F401
            ChunkedReconstructor,
        )
    except ImportError:
        has_nabu = False
    else:
        has_nabu = True
else:
    has_nabu = True


def test_simple_workflow_nabu():
    """Test the workflow: darkref -> axis -> nabu slices -> nabu volume"""

    with HDF5MockContext(
        scan_path=os.path.join(tempfile.mkdtemp(), "scan_test"), n_proj=100
    ) as scan:
        # insure no cfg yet
        assert len(glob(os.path.join(scan.path, "*.cfg"))) == 0
        assert not os.path.exists(
            scan.process_file
        ), "check tomwer should not have been processed yet"

        graph = load_graph(
            source={
                "nodes": [
                    {
                        "id": "darkref",
                        "task_type": "class",
                        "task_identifier": "tomwer.core.process.reconstruction.darkref.darkrefs.DarkRefs",
                    },
                    {
                        "id": "axis",
                        "task_type": "class",
                        "task_identifier": "tomwer.core.process.reconstruction.axis.axis.AxisProcess",
                        "default_inputs": [
                            {
                                "name": "axis_params",
                                "value": {
                                    "MODE": "manual",
                                    "POSITION_VALUE": 0.2,
                                },
                            },
                        ],
                    },
                    {
                        "id": "nabu slices",
                        "task_type": "class",
                        "task_identifier": "tomwer.core.process.reconstruction.nabu.nabuslices.NabuSlices",
                        "dry_run": True,  # as this is a mock dataset avoid to reconstruct it and only check for the .cfg file created
                        "default_inputs": [
                            {
                                "name": "nabu_params",
                                "value": {"tomwer_slices": 2},
                            }
                        ],
                    },
                    {
                        "id": "nabu volume",
                        "task_type": "class",
                        "task_identifier": "tomwer.core.process.reconstruction.nabu.nabuvolume.NabuVolume",
                        "dry_run": True,
                        "default_inputs": [
                            {
                                "name": "dry_run",
                                "value": True,
                            }
                        ],
                    },
                ],
                "links": [
                    {
                        "source": "darkref",
                        "target": "axis",
                        "map_all_data": True,
                    },
                    {
                        "source": "axis",
                        "target": "nabu slices",
                        "data_mapping": [  # same as all arguments but just here to test both
                            {
                                "source_output": "data",
                                "target_input": "data",
                            },
                        ],
                    },
                    {
                        "source": "nabu slices",
                        "target": "nabu volume",
                        "map_all_data": True,
                    },
                ],
            }
        )
        assert graph.is_cyclic is False, "graph is expected to be acyclic"
        assert analysis.start_nodes(graph=graph.graph) == {
            "darkref"
        }, "start node should be a single task `darkref`"
        validate_graph(graph.graph)
        result = execute_graph(
            graph,
            inputs=[
                {"id": "darkref", "name": "data", "value": scan},
            ],
        )
        assert analysis.end_nodes(graph=graph.graph) == {
            "nabu volume"
        }, "should only have one result nodes"
        assert "data" in result, f"cannot find `nabu volume` in {result}"
        assert os.path.exists(scan.process_file), "check tomwer has been processed"
        assert os.path.exists(
            os.path.join(scan.path, PROCESS_FOLDER_NAME, "nabu_cfg_files")
        ), "nabu has not been executed (even in dry mode)"
