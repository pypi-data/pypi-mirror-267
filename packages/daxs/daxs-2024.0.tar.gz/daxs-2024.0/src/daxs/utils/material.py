"""Material class and related functions."""
from __future__ import annotations

from typing import Iterable

import numpy as np

try:
    from pymatgen.io.cif import CifParser

    HAS_PYMATGEN = True
except ImportError:
    HAS_PYMATGEN = False

MATERIALS = {
    "Si": [5.43071, 5.43071, 5.43071, 90.0, 90.0, 90.0],
    "Ge": [5.658, 5.658, 5.658, 90.0, 90.0, 90.0],
    "LiNbO3": [5.1501, 5.1501, 5.4952, 62.057, 62.057, 60.0],
    "a-quartz": [4.9133, 4.9133, 5.4053, 90.0, 90.0, 120.0],
    "diamond": [3.567, 3.567, 3.567, 90.0, 90.0, 90.0],
}


class Material:
    def __init__(  # noqa: PLR0913
        self,
        name: str,
        a: float,
        b: float,
        c: float,
        alpha: float,
        beta: float,
        gamma: float,
    ):
        """Initialize a material with its unit cell parameters."""
        self.name = name
        self.a = a
        self.b = b
        self.c = c
        self.alpha = np.radians(alpha)
        self.beta = np.radians(beta)
        self.gamma = np.radians(gamma)

    # fmt: off
    @property
    def volume(self):
        return (
            self.a * self.b * self.c * np.sqrt(
                1
                - np.cos(self.alpha) ** 2
                - np.cos(self.beta) ** 2
                - np.cos(self.gamma) ** 2
                + 2 * np.cos(self.alpha) * np.cos(self.beta) * np.cos(self.gamma)
            )
        )

    @property
    def s11(self):
        return self.b**2 * self.c**2 * np.sin(self.alpha) ** 2

    @property
    def s22(self):
        return self.a**2 * self.c**2 * np.sin(self.beta) ** 2

    @property
    def s33(self):
        return self.a**2 * self.b**2 * np.sin(self.gamma) ** 2

    @property
    def s12(self):
        return (
            self.a * self.b * self.c**2
            * (np.cos(self.alpha) * np.cos(self.beta) - np.cos(self.gamma))
        )

    @property
    def s23(self):
        return (
            self.a**2 * self.b * self.c
            * (np.cos(self.beta) * np.cos(self.gamma) - np.cos(self.alpha))
        )

    @property
    def s31(self):
        return (
            self.a * self.b**2 * self.c
            * (np.cos(self.gamma) * np.cos(self.alpha) - np.cos(self.beta))
        )
    # fmt: on

    def calculate_d_spacing(self, reflection: Iterable[int] = (1, 1, 1)):
        """Calculate the d spacing for a given reflection."""
        h, k, l = reflection  # noqa: E741

        return self.volume / np.sqrt(
            self.s11 * h**2
            + self.s22 * k**2
            + self.s33 * l**2
            + 2 * (self.s12 * h * k + self.s23 * k * l + self.s31 * l * h)
        )

    @classmethod
    def from_name(cls, name: str):
        """Initialize a material from its name."""
        if name in MATERIALS:
            return cls(name, *MATERIALS[name])
        raise ValueError(
            f"Unit cell parameters are not available for {name}. The available "
            f"materials are: {', '.join(MATERIALS.keys())}."
        )

    @classmethod
    def from_cif(cls, filename: str):
        """Initialize a material from a CIF file."""
        if not HAS_PYMATGEN:
            raise ImportError("pymatgen is required to read CIF files.")
        cif = CifParser(filename)
        structure = cif.get_structures()[0]
        return cls(filename, *structure.lattice.abc, *structure.lattice.angles)
