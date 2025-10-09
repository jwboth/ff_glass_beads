"""Batch analysis for cropping raw images."""

import argparse
from pathlib import Path

import darsia
import logging

from darsia.presets.workflows.fluidflower_config import FluidFlowerConfig
from darsia.presets.workflows.rig import Rig

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
import numpy as np

if __name__ == "__main__":
    # ! ---- PARSE DATA ----

    # Parse arguments
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
        help="Show the labels after each step.",
    )
    args = parser.parse_args()

    # Read data from meta
    config = FluidFlowerConfig(Path(args.config))

    # Plotting
    plot_folder = config.data.log / "plot"
    plot_folder.mkdir(parents=True, exist_ok=True)

    # ! ---- LOAD RIG AND RUN ----

    fluidflower = Rig()
    fluidflower.load(config.data.results / "fluidflower")

    # Load run
    experiment = darsia.ProtocolledExperiment(
        imaging_protocol=config.protocol.imaging,
        injection_protocol=config.protocol.injection,
        pressure_temperature_protocol=config.protocol.pressure_temperature,
        blacklist_protocol=config.protocol.blacklist,
        pad=config.data.pad,
    )
    fluidflower.load_experiment(experiment)

    for i, path in enumerate(config.data.data):
        # Update
        fluidflower.update(path)

        # Read image
        img = fluidflower.read_image(path)

        # Convert image to darsia.OpticalImage
        img = darsia.OpticalImage(img.img, **img.metadata())

        # Plot image
        img = img.img_as(np.uint8)
        img.original_dtype = np.uint8  # Hack to allow plotting
        img.write(plot_folder / f"{path.stem}.jpg", quality=40)

    print("Done. Analysis.")
