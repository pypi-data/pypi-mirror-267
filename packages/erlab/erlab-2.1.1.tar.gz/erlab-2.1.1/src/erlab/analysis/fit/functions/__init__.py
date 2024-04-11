"""Various functions used in fitting.

.. currentmodule:: erlab.analysis.fit.functions

Modules
=======

.. autosummary::
   :toctree:

   dynamic
   general

"""

__all__ = [
    "TINY",
    "FermiEdge2dFunction",
    "MultiPeakFunction",
    "PolynomialFunction",
    "do_convolve",
    "do_convolve_y",
    "fermi_dirac",
    "fermi_dirac_linbkg",
    "fermi_dirac_linbkg_broad",
    "gaussian_wh",
    "lorentzian_wh",
    "step_broad",
    "step_linbkg_broad",
]

from erlab.analysis.fit.functions.dynamic import (
    FermiEdge2dFunction,
    MultiPeakFunction,
    PolynomialFunction,
)
from erlab.analysis.fit.functions.general import (
    TINY,
    do_convolve,
    do_convolve_y,
    fermi_dirac,
    fermi_dirac_linbkg,
    fermi_dirac_linbkg_broad,
    gaussian_wh,
    lorentzian_wh,
    step_broad,
    step_linbkg_broad,
)
