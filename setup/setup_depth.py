"""Step 1 of workflow (continued).

Convert depth measurements from csv to a structured format for analysis,
and define a depth map for the Fluidflower rig through interpolation.

"""

import argparse
from pathlib import Path

from darsia.presets.workflows.setup.setup_depth import setup_depth_map

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process depth measurements.")
    parser.add_argument(
        "--config",
        type=str,
        default="config.toml",
        help="Path to config file.",
    )
    parser.add_argument(
        "--show",
        action="store_true",
        help="Show the resulting depth map.",
    )
    args = parser.parse_args()
    config = Path(args.config)

    # Call standard workflow for setting up a depth map
    setup_depth_map(config, key="mean", show=args.show)
