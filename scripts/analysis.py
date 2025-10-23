"""Main analysis for FF Glass Beads project."""

import logging

from darsia.presets.workflows.user_interface_analysis import preset_analysis
from darsia.presets.workflows.rig import Rig

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    preset_analysis(Rig)
