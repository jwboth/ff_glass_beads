"""Analyze the thickness of a gas cap over time."""

from __future__ import annotations

import argparse
import logging

import darsia
import matplotlib.pyplot as plt
import pandas as pd
from darsia.presets.workflows.analysis.analysis_context import prepare_analysis_context
from darsia.presets.workflows.rig import Rig

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def _specific_analysis(
    img,
    saturation_g,
    concentration_aq,  # Not used in this analysis.
    mass,  # Not used in this analysis.
    show=False,  # Whether to show images during analysis (for debugging).
) -> float:
    """Compute the gas cap thickness based on the saturation_g."""

    # HARDCODED parameter! Threshold for considering gas phase.
    threshold = 1e-2  # This threshold may need tuning based on the specific data and requirements.

    # Boolean mask of the saturation
    mask = saturation_g > threshold

    # Identify the coordinates of the True voxels in the mask
    points = mask.img.nonzero()

    # Compute the min and max row indices of the gas cap. Note that in image coordinates,
    # the row index corresponds to the vertical position. Also row (ascending) -> y (descending).
    # Thus, flip min->max.
    min_row = points[0].max()
    max_row = points[0].min()

    # Setup proxy voxels
    max_voxel = darsia.Voxel([max_row, 0])  # Max row index, arbitrary column index
    min_voxel = darsia.Voxel([min_row, 0])  # Min row index, arbitrary column index

    # Convert to coordinates.
    min_coordinate = mask.coordinatesystem.coordinate(min_voxel)
    max_coordinate = mask.coordinatesystem.coordinate(max_voxel)

    logger.info(f"Max coordinate of gas cap: {max_coordinate}")
    logger.info(f"Min coordinate of gas cap: {min_coordinate}")

    # Compute thickness as the difference in the vertical coordinate (assuming vertical is the second dimension)
    thickness = max_coordinate[1] - min_coordinate[1]

    # Plot the box corresponding to the gas cap for visualization (optional)
    if show:
        plt.figure()
        plt.imshow(img.img)
        plt.plot([0, saturation_g.img.shape[1]], [max_row, max_row], "r--", label="Max")
        plt.plot([0, saturation_g.img.shape[1]], [min_row, min_row], "b--", label="Min")
        plt.legend()
        plt.show()

    return thickness


def build_parser_for_analysis():
    """Build and return argument parser for the analysis."""
    parser = argparse.ArgumentParser(description="Setup run.")
    parser.add_argument(
        "--config",
        type=str,
        nargs="+",
        required=True,
        help="Path(s) to config file(s). Multiple files can be specified.",
    )
    parser.add_argument(
        "--show",
        action="store_true",
        help="Whether to show images during analysis (for debugging).",
    )

    return parser


if __name__ == "__main__":
    # Prepare shared context once for all analyses
    parser = build_parser_for_analysis()
    args = parser.parse_args()
    ctx = prepare_analysis_context(
        cls=Rig, path=args.config, require_color_to_mass=True
    )

    # Unpack context for easier access
    config = ctx.config
    fluidflower = ctx.fluidflower
    image_paths = ctx.image_paths
    color_to_mass_analysis = ctx.color_to_mass_analysis

    # Initialize DataFrame and CSV path for storing results
    columns = ["time", "datetime", "stem", "thickness"]
    df = pd.DataFrame(columns=columns)
    csv_path = config.data.results / "sparse_data" / "gas_cap_thickness.csv"
    csv_path.parent.mkdir(parents=True, exist_ok=True)

    # Loop over images and analyze
    for path in image_paths:
        # Extract color signal and assign mass
        img = fluidflower.read_image(path)
        mass_analysis_result = color_to_mass_analysis(img)

        # Run specific analysis
        thickness = _specific_analysis(
            img=img,
            saturation_g=mass_analysis_result.saturation_g,
            concentration_aq=mass_analysis_result.concentration_aq,
            mass=mass_analysis_result.mass,
            show=args.show,
        )

        # Prepare row data for DataFrame
        row_data = {
            "time": mass_analysis_result.time,
            "datetime": img.date,
            "stem": path.stem,
            "thickness": thickness,
        }

        # Add row to DataFrame using pd.concat for better performance
        new_row = pd.DataFrame([row_data])
        df = pd.concat([df, new_row], ignore_index=True)

        # Save DataFrame to CSV after each image analysis
        df.to_csv(csv_path, index=False)
        logger.info(
            f"Processed {path.stem} at time {mass_analysis_result.time} seconds: Thickness = {thickness} meters. Results saved to {csv_path}."
        )
