import pytest

from tomwer.core.process.reconstruction.nabu.utils import (
    get_recons_volume_identifier,
    get_multi_cor_recons_volume_identifiers,
    nabu_std_err_has_error,
)
from tomwer.core.scan.edfscan import EDFTomoScan
from tomwer.core.scan.nxtomoscan import NXtomoScan

_scans = (
    NXtomoScan(
        scan="/my_scan_file.nx",
        entry="entry_test",
    ),
    EDFTomoScan("/my_scan_folder"),
)


@pytest.mark.parametrize("scan", _scans)
@pytest.mark.parametrize("axis", ("YZ", "XZ", "XY"))
def test_get_recons_volume_identifier(scan, axis):
    """
    test get_recons_volume_identifier behavior
    """

    entry = scan.entry if isinstance(scan, NXtomoScan) else "entry"
    # check some exceptions
    with pytest.raises(ValueError):
        get_recons_volume_identifier(
            file_prefix="volume_rec",
            location="/this/is/a/test",
            file_format="toto",
            slice_index=1080,
            scan=scan,
            axis=axis,
        )

    # check hdf5 reconstructions
    id_rec_vols = get_recons_volume_identifier(
        file_prefix="volume_rec",
        location="/this/is/a/test",
        file_format="hdf5",
        slice_index="1080",
        scan=scan,
        axis=axis,
    )
    assert len(id_rec_vols) == 1
    assert (
        id_rec_vols[0].to_str()
        == f"hdf5:volume:/this/is/a/test/volume_rec_plane_{axis}_001080.hdf5?path={entry}/reconstruction"
    )

    # check edf and jp2k slice reconstructions (are expected to have the same behavior)
    id_rec_vols = get_recons_volume_identifier(
        file_prefix="volume_rec",
        location="/this/is/a/test",
        file_format="edf",
        slice_index="1080",
        scan=scan,
        axis=axis,
    )
    assert len(id_rec_vols) == 1
    assert (
        id_rec_vols[0].to_str() == "edf:volume:/this/is/a/test?file_prefix=volume_rec"
    )

    id_rec_vols = get_recons_volume_identifier(
        file_prefix="volume_recslice",
        location="/this/is/a/test",
        file_format="jp2k",
        slice_index="1080",
        scan=scan,
        axis=axis,
    )
    assert len(id_rec_vols) == 1
    assert (
        id_rec_vols[0].to_str()
        == "jp2k:volume:/this/is/a/test?file_prefix=volume_recslice"
    )

    # check tiff slice reconstructions
    id_rec_vols = get_recons_volume_identifier(
        file_prefix="volume_rec",
        location="/this/is/a/test",
        file_format="tiff",
        slice_index="1080",
        scan=scan,
        axis=axis,
    )
    assert len(id_rec_vols) == 1
    assert (
        id_rec_vols[0].to_str() == "tiff:volume:/this/is/a/test?file_prefix=volume_rec"
    )


@pytest.mark.parametrize("scan", _scans)
def test_get_multi_cor_recons_volume_identifier(scan):
    """
    test the get_multi_cor_recons_volume_identifier function
    """
    entry = scan.entry if isinstance(scan, NXtomoScan) else "entry"

    # dummy test with hdf5
    id_rec_vols = get_multi_cor_recons_volume_identifiers(
        scan=scan,
        slice_index="middle",
        location="/this/is/a/test",
        file_prefix="rec",
        cors=(10, 12),
        file_format="hdf5",
    )
    assert isinstance(id_rec_vols, dict)
    assert len(id_rec_vols) == 2
    assert 10 in id_rec_vols.keys()
    assert 12 in id_rec_vols.keys()
    assert (
        id_rec_vols[10].to_str()
        == f"hdf5:volume:/this/is/a/test/rec_10.000_01024.hdf5?path={entry}/reconstruction"
    )

    # dummy test with tiff
    id_rec_vols = get_multi_cor_recons_volume_identifiers(
        scan=scan,
        slice_index="middle",
        location="/this/is/a/test",
        file_prefix="rec",
        cors=(10, 12),
        file_format="tiff",
    )
    assert isinstance(id_rec_vols, dict)
    assert len(id_rec_vols) == 2
    assert 10 in id_rec_vols.keys()
    assert 12 in id_rec_vols.keys()
    assert id_rec_vols[10].to_str() == "tiff:volume:/this/is/a?file_prefix=test"


def test_nabu_std_err_has_error():
    assert nabu_std_err_has_error(None) is False
    assert nabu_std_err_has_error(b"") is False
    assert nabu_std_err_has_error(b"this is an error") is True
    assert (
        nabu_std_err_has_error(
            b"warnings.warn('creating CUBLAS context to get version num"
        )
        is False
    )
    assert (
        nabu_std_err_has_error(
            b"warnings.warn('creating CUBLAS context to get version num\n this is an error"
        )
        is True
    )

    assert (
        nabu_std_err_has_error(
            b"""/nobackup/lbs0511/tomotools/venvs/2023_10_04/lib/python3.8/site-packages/skcuda/cublas.py:284: UserWarning: creating CUBLAS context to get version number
            warnings.warn('creating CUBLAS context to get version number')
            /nobackup/lbs0511/tomotools/venvs/2023_10_04/lib/python3.8/site-packages/nabu/cuda/kernel.py:49: UserWarning: The CUDA compiler succeeded, but said the following:
            nvcc warning : The 'compute_35', 'compute_37', 'sm_35', and 'sm_37' architectures are deprecated, and may be removed in a future release (Use -Wno-deprecated-gpu-targets to suppress warning).
            self.module = SourceModule(self.src, **self.sourcemodule_kwargs)
            /nobackup/lbs0511/tomotools/venvs/2023_10_04/lib/python3.8/site-packages/pycuda/elementwise.py:47: UserWarning: The CUDA compiler succeeded, but said the following:
            nvcc warning : The 'compute_35', 'compute_37', 'sm_35', and 'sm_37' architectures are deprecated, and may be removed in a future release (Use -Wno-deprecated-gpu-targets to suppress warning).
            return SourceModule(
            /nobackup/lbs0511/tomotools/venvs/2023_10_04/lib/python3.8/site-packages/nabu/cuda/kernel.py:49: UserWarning: The CUDA compiler succeeded, but said the following:
            nvcc warning : The 'compute_35', 'compute_37', 'sm_35', and 'sm_37' architectures are deprecated, and may be removed in a future release (Use -Wno-deprecated-gpu-targets to suppress warning).
            self.module = SourceModule(self.src, **self.sourcemodule_kwargs)
            /nobackup/lbs0511/tomotools/venvs/2023_10_04/lib/python3.8/site-packages/pycuda/elementwise.py:47: UserWarning: The CUDA compiler succeeded, but said the following:
            nvcc warning : The 'compute_35', 'compute_37', 'sm_35', and 'sm_37' architectures are deprecated, and may be removed in a future release (Use -Wno-deprecated-gpu-targets to suppress warning).
            return SourceModule(
            /nobackup/lbs0511/tomotools/venvs/2023_10_04/lib/python3.8/site-packages/nabu/cuda/kernel.py:49: UserWarning: The CUDA compiler succeeded, but said the following:
            nvcc warning : The 'compute_35', 'compute_37', 'sm_35', and 'sm_37' architectures are deprecated, and may be removed in a future release (Use -Wno-deprecated-gpu-targets to suppress warning).
            self.module = SourceModule(self.src, **self.sourcemodule_kwargs)
            /nobackup/lbs0511/tomotools/venvs/2023_10_04/lib/python3.8/site-packages/nabu/cuda/kernel.py:49: UserWarning: The CUDA compiler succeeded, but said the following:
            nvcc warning : The 'compute_35', 'compute_37', 'sm_35', and 'sm_37' architectures are deprecated, and may be removed in a future release (Use -Wno-deprecated-gpu-targets to suppress warning).
            self.module = SourceModule(self.src, **self.sourcemodule_kwargs)
            /nobackup/lbs0511/tomotools/venvs/2023_10_04/lib/python3.8/site-packages/nabu/cuda/kernel.py:49: UserWarning: The CUDA compiler succeeded, but said the following:
            nvcc warning : The 'compute_35', 'compute_37', 'sm_35', and 'sm_37' architectures are deprecated, and may be removed in a future release (Use -Wno-deprecated-gpu-targets to suppress warning).
            kernel.cu(111): warning #1215-D: function "tex2D(texture<T, 2, cudaReadModeElementType>, float, float) [with T=float]"
            /cvmfs/hpc.esrf.fr/software/packages/ubuntu20.04/x86_64/cuda/11.8.0//bin/../targets/x86_64-linux/include/texture_fetch_functions.h(198): here was declared deprecated
            kernel.cu(112): warning #1215-D: function "tex2D(texture<T, 2, cudaReadModeElementType>, float, float) [with T=float]"
            /cvmfs/hpc.esrf.fr/software/packages/ubuntu20.04/x86_64/cuda/11.8.0//bin/../targets/x86_64-linux/include/texture_fetch_functions.h(198): here was declared deprecated
            kernel.cu(113): warning #1215-D: function "tex2D(texture<T, 2, cudaReadModeElementType>, float, float) [with T=float]"
            /cvmfs/hpc.esrf.fr/software/packages/ubuntu20.04/x86_64/cuda/11.8.0//bin/../targets/x86_64-linux/include/texture_fetch_functions.h(198): here was declared deprecated
            kernel.cu(114): warning #1215-D: function "tex2D(texture<T, 2, cudaReadModeElementType>, float, float) [with T=float]"
            /cvmfs/hpc.esrf.fr/software/packages/ubuntu20.04/x86_64/cuda/11.8.0//bin/../targets/x86_64-linux/include/texture_fetch_functions.h(198): here was declared deprecated
            self.module = SourceModule(self.src, **self.sourcemodule_kwargs)
            /nobackup/lbs0511/tomotools/venvs/2023_10_04/lib/python3.8/site-packages/pycuda/elementwise.py:47: UserWarning: The CUDA compiler succeeded, but said the following:
            nvcc warning : The 'compute_35', 'compute_37', 'sm_35', and 'sm_37' architectures are deprecated, and may be removed in a future release (Use -Wno-deprecated-gpu-targets to suppress warning).
            return SourceModule("""
        )
        is False
    )

    assert (
        nabu_std_err_has_error(
            b"""/cvmfs/tomo.esrf.fr/software/packages/linux/x86_64/tomotools/2024_02_26/lib/python3.11/site-packages/cupyx/jit/_interface.py:173: FutureWarning: cupyx.jit.rawkernel is experimental. The interface can change in the future.
        cupy._util.experimental('cupyx.jit.rawkernel')
        /cvmfs/tomo.esrf.fr/software/packages/linux/x86_64/tomotools/2024_02_26/lib/python3.11/site-packages/skcuda/cublas.py:284: UserWarning: creating CUBLAS context to get version number
        warnings.warn('creating CUBLAS context to get version number')"""
        )
        is False
    )
