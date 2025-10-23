"""Full setup for the FF Glass Beads project."""

import logging

from darsia.presets.workflows.rig import Rig
from darsia.presets.workflows.user_interface_setup import preset_setup

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    preset_setup(Rig)
