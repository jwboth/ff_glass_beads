"""Step 2 of workflow.

Define a geometric segmentation of the uncorrected baseline image.

This requires a suitably colored image as input for the automatic segmentation.

"""

import argparse
import logging
from darsia.presets.workflows.setup_labeling import segment_colored_image

logging.basicConfig(level=logging.INFO)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Geometry segmentation of FFUM geometry."
    )
    parser.add_argument(
        "--config",
        type=str,
        default="config.toml",
        help="Path to config file.",
    )
    parser.add_argument(
        "--show",
        action="store_true",
        help="Show the labels after each step.",
    )
    args = parser.parse_args()
    segment_colored_image(args.config, args.show)
