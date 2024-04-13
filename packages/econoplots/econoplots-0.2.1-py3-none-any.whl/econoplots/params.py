"""Set global parameters of matplotlib."""

# %% Imports
from __future__ import annotations

# Third Party Imports
import matplotlib as mpl
from cycler import cycler

# Econoplots Imports
from econoplots.utils import loadColorMap


# %% Set Params
def setRCParams():
    color_map = loadColorMap()

    mpl.rcParams["font.sans-serif"] = [
        # "CMU Sans Serif Demi Condensed",
        # "CMU Sans Serif",
        "CMU Serif",
        # "CMU Bright",
    ]
    # stix doesn't have the problem of unevenly-tall letters of CMU
    mpl.rcParams["mathtext.fontset"] = "stix"
    mpl.rcParams["font.family"] = "STIXGeneral"

    # mpl.rcParams["font.family"] = "sans-serif"
    mpl.rcParams.update(
        {
            # "font.size": 14,
            # "font.weight": "bold",
            # "font.weight": "600",
        }
    )
    mpl.rcParams["lines.linestyle"] = "-"
    mpl.rcParams["lines.linewidth"] = 3
    mpl.rcParams["axes.prop_cycle"] = cycler(color=color_map["line_chart"])
    mpl.rcParams["figure.facecolor"] = "w"
    mpl.rcParams["axes.facecolor"] = "w"
    mpl.rcParams["xtick.major.size"] = 6  # length of tick marks
    mpl.rcParams["xtick.minor.size"] = 3
    mpl.rcParams["ytick.major.size"] = 0
    mpl.rcParams["ytick.minor.size"] = 0
