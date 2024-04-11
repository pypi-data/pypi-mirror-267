"""Module containing array utilities."""
import numpy as np


def intersect(a, b):
    """
    Check if the arrays a and b intersect.

    Parameters
    ----------
    a, b : numpy.array
        The arrays to compare.

    Returns
    -------
    : bool
        True if the arrays intersect, False otherwise.

    """
    # Sort the input arrays.
    a, b = np.sort(a), np.sort(b)
    if (b[-1] < a[0]) or (a[-1] < b[0]):
        return False
    return True
