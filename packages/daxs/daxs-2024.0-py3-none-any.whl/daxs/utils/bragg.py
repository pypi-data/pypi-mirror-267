"""Bragg's law calculations."""
from __future__ import annotations

from typing import Iterable

import numpy as np
from scipy.constants import Planck, elementary_charge, speed_of_light


def calculate_wavelength(angle: float | Iterable[float], d_spacing: float):
    """
    Calculate the wavelength [Å] for the scattering angle [degrees] and d-spacing [Å].

    λ [Å] = 2 * d [Å] * sin(θ [rad])
    """
    if not isinstance(angle, np.ndarray):
        angle = np.asarray(angle)
    return 2 * d_spacing * np.sin(np.radians(angle))


def calculate_energy(angle: float | Iterable[float], d_spacing: float):
    """
    Calculate the energy [keV] for the scattering angle [degrees] and d-spacing [Å].

    E [keV] = h [J s] * c [m s^-1] / e [C] / λ [Å] =  [eV m / Å] = 1e7 [keV]
    """
    wavelength = calculate_wavelength(angle, d_spacing)
    return 1e7 * Planck * speed_of_light / elementary_charge / wavelength


def calculate_scattering_angle(energy: float | Iterable[float], d_spacing: float):
    """Calculate the angle [degrees] for a given energy [keV] and d-spacing [Å]."""
    if not isinstance(energy, np.ndarray):
        energy = np.asarray(energy)
    wavelength = 1e7 * Planck * speed_of_light / elementary_charge / energy
    return np.degrees(np.arcsin(wavelength / (2 * d_spacing)))
