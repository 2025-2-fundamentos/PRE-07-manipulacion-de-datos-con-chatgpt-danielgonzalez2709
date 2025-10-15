import os
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

__all__ = ["generate_outputs"]


def generate_outputs(input_dir: str = "files/input", output_dir: str = "files/output", plots_dir: str = "files/plots") -> None:
    """Generate required outputs for the exercise.

    - Reads drivers.csv and timesheet.csv from input_dir
    - Aggregates total hours and miles per driver
    - Writes a summary CSV to output_dir/summary.csv
    - Saves a bar chart with top 10 drivers by total miles to plots_dir/top10_drivers.png
    """
    # Ensure output directories exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    Path(plots_dir).mkdir(parents=True, exist_ok=True)

    drivers_path = os.path.join(input_dir, "drivers.csv")
    timesheet_path = os.path.join(input_dir, "timesheet.csv")

    # Load data
    drivers = pd.read_csv(drivers_path)
    timesheet = pd.read_csv(timesheet_path)

    # Aggregate totals by driver
    summary = (
        timesheet.groupby("driverId", as_index=False)
        .agg({"hours-logged": "sum", "miles-logged": "sum"})
        .rename(columns={"hours-logged": "total_hours", "miles-logged": "total_miles"})
    )

    # Join driver names
    summary = summary.merge(drivers[["driverId", "name"]], on="driverId", how="left")

    # Reorder columns for readability
    cols = ["driverId", "name", "total_hours", "total_miles"]
    summary = summary[cols]

    # Save summary CSV
    summary_csv_path = os.path.join(output_dir, "summary.csv")
    summary.to_csv(summary_csv_path, index=False)

    # Plot top 10 drivers by total miles
    top = summary.nlargest(10, "total_miles").copy()
    plt.figure(figsize=(10, 6))
    plt.barh(top["name"], top["total_miles"], color="#4C72B0")
    plt.gca().invert_yaxis()  # Highest at the top
    plt.xlabel("Total miles")
    plt.title("Top 10 drivers by total miles")
    plt.tight_layout()

    plot_path = os.path.join(plots_dir, "top10_drivers.png")
    plt.savefig(plot_path)
    plt.close()
