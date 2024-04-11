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

import pytest
from ewokscore.graph import analysis, load_graph
from ewokscore.graph.validate import validate_graph

from tomwer.core.utils.scanutils import HDF5MockContext
from nabu.pipeline.config import get_default_nabu_config
from nabu.pipeline.fullfield.nabu_config import (
    nabu_config as nabu_fullfield_default_config,
)

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

pytest.mark.skipif(condition=not has_nabu, reason="nabu not installed")


classes_to_test = {
    "darkref": "tomwer.core.process.reconstruction.darkref.darkrefs.DarkRefs",
    "axis": "tomwer.core.process.reconstruction.axis.axis.AxisProcess",
    "nabu slices": "tomwer.core.process.reconstruction.nabu.nabuslices.NabuSlices",
}


@pytest.mark.parametrize("node_name, node_qual_name", classes_to_test.items())
def test_single_class_instanciation(node_name, node_qual_name):
    with HDF5MockContext(
        scan_path=os.path.join(tempfile.mkdtemp(), "scan_test"), n_proj=100
    ) as scan:
        # insure no cfg yet
        assert len(glob(os.path.join(scan.path, "*.cfg"))) == 0

        graph = load_graph(
            {
                "nodes": [
                    {
                        "id": node_name,
                        "task_type": "class",
                        "task_identifier": node_qual_name,
                        "default_inputs": [
                            {
                                "name": "data",
                                "value": scan,
                            },
                            {
                                "name": "nabu_params",
                                "value": get_default_nabu_config(
                                    nabu_fullfield_default_config
                                ),
                            },
                        ],
                    },
                ]
            }
        )

        assert graph.is_cyclic is False, "graph is expected to be acyclic"
        assert analysis.start_nodes(graph.graph) == {
            node_name
        }, "graph is expected to have only on start nodes"
        validate_graph(graph.graph)
        result = graph.execute(varinfo=None)

        assert analysis.end_nodes(graph.graph) == {
            node_name
        }, "graph is expected to have only one end node"
        assert "data" in result, "data is expected to be part of the output_values"
