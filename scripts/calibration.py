"""Full calibration for the FF Glass Beads project."""

import logging
import darsia
from darsia.presets.workflows.rig import Rig
from darsia.presets.workflows.user_interface_calibration import preset_calibration

logging.basicConfig(level=logging.INFO)


if __name__ == "__main__":
    rois = {
        "full": darsia.CoordinateArray([(0.0, 0.0), (2.745, 1.5)]),
    }
    preset_calibration(Rig, rois=rois)
