# pylint: disable=redefined-outer-name

import numpy as np
import pytest

from daxs.sources import Hdf5Source, Selection


@pytest.mark.parametrize(
    "selection, normalized_selection",
    (
        (None, []),
        (1, [1]),
        ("1", [1]),
        ("1-3", [1, 2, 3]),
        ("fscan", ["fscan"]),
        ([1, "fscan"], [1, "fscan"]),
    ),
)
def test_selection(selection, normalized_selection):
    selection = Selection(selection)
    assert list(selection) == normalized_selection


@pytest.mark.parametrize(
    "included_scans, excluded_scans, selected_scans",
    (
        ("1-4", None, [1, 2, 3, 4]),
        ([1, 2, 3, 4], "fscan", []),
        (np.array([1, 2, 3], dtype=np.int64), None, [1, 2, 3]),
        (".*", [1, 2, 3], [4, 5]),
    ),
)
def test_hdf5_source_selected_scans(
    hdf5_mock_path, included_scans, excluded_scans, selected_scans
):
    source = Hdf5Source(hdf5_mock_path, included_scans, excluded_scans)
    assert source.selected_scans == selected_scans
    # The second test is for the cached values.
    assert source.selected_scans == selected_scans


def test_hdf5_source_scans(hdf5_mock_path):
    data_mappings = {}
    source = Hdf5Source(hdf5_mock_path, 1, None, data_mappings)
    with pytest.raises(AssertionError):
        assert source.scans

    data_mappings["x"] = ".1/measurement/x"
    data_mappings["signal"] = ".1/measurement/signal"
    source = Hdf5Source(hdf5_mock_path, 1, None, data_mappings)
    with pytest.raises(KeyError):
        assert source.scans

    data_mappings["monitor"] = ".1/measurement/monitor"
    source = Hdf5Source(hdf5_mock_path, 3, None, data_mappings)
    assert source.scans

    data_mappings["name"] = ".1/instrument/name"
    source = Hdf5Source(hdf5_mock_path, 2, None, data_mappings)
    assert source.scans[0].data["name"] == b"detector"
    data_mappings.pop("name")

    data_mappings["detection_time"] = ".1/measurement/detection_time"
    source = Hdf5Source(hdf5_mock_path, 3, None, data_mappings)
    assert source.scans

    data_mappings["detection_time"] = ".1/measurement/sec"
    source = Hdf5Source(hdf5_mock_path, 3, None, data_mappings)
    assert source.scans

    data_mappings["not_set"] = [".1/measurement/counter1", ".1/measurement/counter2"]
    source = Hdf5Source(hdf5_mock_path, 5, None, data_mappings)
    assert source.scans
