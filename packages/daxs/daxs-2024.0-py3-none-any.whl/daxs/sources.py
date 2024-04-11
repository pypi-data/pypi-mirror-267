"""The module provides classes to deal with different types of data sources."""

from __future__ import annotations

import contextlib
import copy
import logging
import re
from abc import ABC, abstractmethod

import numpy as np
import silx.io.h5py_utils

from daxs.scans import Scan

logger = logging.getLogger(__name__)


class Selection:
    def __init__(self, items):
        assert not isinstance(
            items, dict
        ), "The selection items cannot be a dictionary."

        self.items = items
        self.normalize()

    def normalize(self):
        """
        Convert the items to proper formatting.

        Examples
        --------
        Here are a few examples of how different selections are normalized:

        - 1 to [1,]
        - "1" to [1,]
        - [1, "fscan"] to [1, "fscan"]
        - ["1-3", "fscan"] to [1, 2, 3, "fscan"]

        """
        if self.items is None:
            self.items = []
        elif isinstance(self.items, (int, str)):
            self.items = [self.items]
        elif isinstance(self.items, np.ndarray):
            self.items = self.items.tolist()

        items = []
        for item in self.items:
            if isinstance(item, int):
                items.append(item)
            elif isinstance(item, str):
                if re.search(r"^\d+$", item):
                    items.append(int(item))
                elif re.search(r"^\d+\-\d+$", item):
                    start, stop = item.split("-")
                    for i in range(int(start), int(stop) + 1):
                        items.append(i)
                else:
                    items.append(item)
        self.items = items

    def __iter__(self):
        return iter(self.items)


class Source(ABC):
    """Base class for sources of scans."""

    @property
    @abstractmethod
    def filename(self) -> str | None:
        """The filename of the source."""

    @property
    @abstractmethod
    def scans(self) -> list[Scan]:
        """Return all source scans."""


class Hdf5Source(Source):
    def __init__(
        self,
        filename: str,
        included_scans=None,
        excluded_scans=None,
        data_mappings: dict | None = None,
    ):
        """
        Class for a HDF5 source of scans

        Parameters
        ----------
        filename :
            Name of the HDF5 file.
        included_scans :
            Selection of included scans.
        excluded_scans :
            Selection of excluded scans.
        data_mappings :
            Mappings between scan attributes (x, signal, monitor, etc.) and paths in
            the HDF5 file.

        """
        self._filename = filename
        self.included_scans = Selection(included_scans)
        self.excluded_scans = Selection(excluded_scans)
        self.data_mappings = data_mappings

        self._scans: list[Scan] | None = None
        self._selected_scans: list[int] | None = None

    @property
    def filename(self) -> str | None:
        return self._filename

    @property
    def selected_scans(self) -> list[int]:
        """The selected scans considering the inclusions and exclusions selections."""
        if self._selected_scans is not None:
            return self._selected_scans

        included_scans, excluded_scans, selected_scans = [], [], []

        with silx.io.h5py_utils.File(self.filename) as fp:
            indices = []

            for group in fp.values():
                title = group["title"][()]

                with contextlib.suppress(AttributeError):
                    title = title.decode("utf-8")

                # The group.name is of the form /1.1, /1.2, /2.1, etc.
                # The title contains the command executed by the user, e.g.
                # fscan 3.16 3.22 60 0.0002.
                index = int(group.name[1:-2])
                if index in indices:
                    continue
                indices.append(index)

                for item in self.included_scans:
                    if item == index or (
                        isinstance(item, str) and re.search(item, title)
                    ):
                        included_scans.append(index)

                for item in self.excluded_scans:
                    if item == index or (
                        isinstance(item, str) and re.search(item, title)
                    ):
                        excluded_scans.append(index)

        for index in sorted(included_scans):
            if index not in excluded_scans:
                selected_scans.append(index)
            else:
                logger.info("Scan %s/%d was excluded.", self.filename, index)

        self._selected_scans = selected_scans
        logger.debug(
            "The scans %s have been selected from %s.", selected_scans, self.filename
        )
        return self._selected_scans

    @property
    def scans(self):
        """Return the scans."""
        if self._scans is None:
            self._scans = [self.read_scan(index) for index in self.selected_scans]
        return self._scans

    def read_data(self, index: int, data_paths: str | list[str]) -> np.ndarray:
        """Read the data given the scan index and data paths."""
        if isinstance(data_paths, str):
            data_paths = [data_paths]

        data: list = []
        with silx.io.h5py_utils.File(self.filename) as fp:
            for data_path in data_paths:
                full_data_path = f"{index}{data_path}"
                try:
                    data_at_path = fp[full_data_path][()]  # type: ignore
                except KeyError as e:
                    raise KeyError(f"Unable to access {full_data_path}.") from e
                except TypeError as e:
                    raise TypeError(
                        f"Unable to read data from {full_data_path}."
                    ) from e

                if isinstance(data_at_path, np.ndarray) and data_at_path.size == 0:
                    raise ValueError(f"Data from {full_data_path} is empty.")

                data.append(data_at_path)

        # Return the element of the array if it has only one element.
        if len(data) == 1:
            [data] = data

        return np.array(data)

    def read_scan(self, index: int) -> Scan:
        """Return a scan object at the index."""
        assert isinstance(index, int), "The index must be an integer."
        assert (
            self.data_mappings is not None
        ), "The data_mappings attribute must be set."
        assert (
            "x" in self.data_mappings
        ), "The data_mappings attribute must contain an entry for the X-axis values."
        assert (
            "signal" in self.data_mappings
        ), "The data_mappings attribute must contain an entry for the signal values."

        data = {}

        x = self.read_data(index, self.data_mappings["x"])
        signal = self.read_data(index, self.data_mappings["signal"])

        # Read additional data paths.
        for key, data_paths in self.data_mappings.items():
            if key in ("x", "signal"):
                continue
            # These are not critical, so we do not raise an error if they are
            # not found.
            try:
                values = self.read_data(index, data_paths)
            except (KeyError, TypeError):
                values = None
            data[key] = copy.deepcopy(values)

        # Finally, copy some metadata.
        data["filename"] = self.filename
        data["index"] = index

        return Scan(x, signal, data)
