__version__ = '0.23'
""" cmrseq - A package for defining and modifying Magnetic Resonance Sequences """
__all__ = ["bausteine", "Sequence", "SystemSpec", "seqdefs", "plotting", "utils", "io", "contrib"]

from cmrseq.core import bausteine
from cmrseq.core._sequence import Sequence
from cmrseq.core._system import SystemSpec
import cmrseq.parametric_definitions as seqdefs

import cmrseq.plotting
import cmrseq.utils
import cmrseq.io
import cmrseq.contrib

# Set default warning signature
import warnings

def warning_on_one_line(message, category, filename, lineno, file=None, line=None):
    if category.__name__=="UserWarning":
        return f"CMRSeq Warning : {message}\n"
    else: # Use different signature for all other warnings, such as DeprecationWarning
        return f"CMRSeq {category.__name__}: {filename}:{lineno} : {message}\n"

warnings.formatwarning = warning_on_one_line
