"""Full calibration for the FF Glass Beads project."""

import logging

from darsia.presets.workflows.rig import Rig
from darsia.presets.workflows.user_interface_calibration import preset_calibration

logging.basicConfig(level=logging.INFO)


if __name__ == "__main__":
    preset_calibration(Rig)
