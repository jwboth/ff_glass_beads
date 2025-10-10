"""Step 4 setup routine. Setup of color paths."""

import argparse
from pathlib import Path
import logging

from darsia.presets.workflows.rig import Rig
from darsia.presets.workflows.setup.setup_color_paths import setup_color_paths

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Setup run.")
    parser.add_argument(
        "--config",
        type=str,
        default="config.toml",
        help="Path to config file.",
    )
    parser.add_argument(
        "--show", action="store_true", help="Show the labels after each step."
    )
    args = parser.parse_args()
    setup_color_paths(Rig, Path(args.config), args.show)
