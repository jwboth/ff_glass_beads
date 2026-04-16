# Example script for plotting results from the finger analysis.
# Fetch here, the velocities over time.

# Usage:
# python analysis/finger_velocities.py --config config_example/single/common.toml config_example/run/run.toml config_example/single/analysis.toml config_example/single/data.toml

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import argparse
import logging
from darsia.presets.workflows.analysis.analysis_context import prepare_analysis_context
from darsia.presets.workflows.rig import Rig
import pandas as pd
import json

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


# User input:
roi = "storage"
key = "horizontal_distances"


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

    # Results path
    results_path = config.data.results / "fingers" / "statistics.json"

    # Load results
    with open(results_path, "r") as f:
        results = json.load(f)

    # Extract times.
    times = results["times"]

    # Extract statistics.
    statistics = results["paths"][roi]["statistics"]

    print(statistics.keys())

    # Collect distributions.
    distributions = []
    for time in times:
        distributions.append(statistics[str(time)][key])

    # Plot time agains the distribution using a boxplot.
    plt.figure(figsize=(10, 6))
    plt.boxplot(distributions, positions=times, widths=0.5)
    plt.xlabel("Time")
    plt.ylabel(f"{key} distribution")
    plt.show()
