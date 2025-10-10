"""Step 3 of setup. Setup of Rig object."""

import argparse
import logging
from pathlib import Path

from darsia.presets.workflows.setup.setup_rig import setup_rig
from darsia.presets.workflows.rig import Rig

# Set logging level
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
        "--show",
        action="store_true",
        help="Show intermediate results.",
    )
    args = parser.parse_args()

    setup_rig(Rig, Path(args.config), args.show)
