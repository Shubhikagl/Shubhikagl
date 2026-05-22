# ============================================================
# CORRECT IMD MONTHLY RAINFALL (mm)
# INDIA SPATIAL AVERAGE
# ============================================================

import numpy as np
import pandas as pd
import glob
import os
import re

# ------------------------------------------------------------
# INPUT FOLDER
# ------------------------------------------------------------

input_folder = r"C:\Users\shubh\OneDrive\Desktop\IMD RF GRD"

# ------------------------------------------------------------
# OUTPUT FILE
# ------------------------------------------------------------

output_csv = os.path.join(
    input_folder,
    "India_Monthly_Rainfall.csv"
)

# ------------------------------------------------------------
# IMD 0.25° GRID SIZE
# ------------------------------------------------------------

nlat = 129
nlon = 135

# ------------------------------------------------------------
# FIND FILES
# ------------------------------------------------------------

grd_files = sorted(
    glob.glob(os.path.join(input_folder, "*.grd"))
)

# ------------------------------------------------------------
# EMPTY LIST
# ------------------------------------------------------------

all_data = []

# ------------------------------------------------------------
# PROCESS FILES
# ------------------------------------------------------------

for file in grd_files:

    filename = os.path.basename(file)

    print("Processing:", filename)

    # Extract year
    year_match = re.search(r"\d{4}", filename)

    if year_match:
        year = int(year_match.group())
    else:
        continue

    # --------------------------------------------------------
    # READ BINARY DATA
    # --------------------------------------------------------

    data = np.fromfile(
        file,
        dtype=np.float32
    )

    # Remove invalid values
    data[data < -100] = np.nan

    # --------------------------------------------------------
    # RESHAPE DATA
    # --------------------------------------------------------

    total_grids = nlat * nlon

    total_days = int(len(data) / total_grids)

    data = data.reshape(
        total_days,
        nlat,
        nlon
    )

    # --------------------------------------------------------
    # DAYS IN MONTH
    # --------------------------------------------------------

    if year % 4 == 0:
        days_in_month = [
            31,29,31,30,31,30,
            31,31,30,31,30,31
        ]
    else:
        days_in_month = [
            31,28,31,30,31,30,
            31,31,30,31,30,31
        ]

    start_day = 0

    # --------------------------------------------------------
    # MONTHLY RAINFALL
    # --------------------------------------------------------

    for month in range(1, 13):

        ndays = days_in_month[month - 1]

        end_day = start_day + ndays

        # Extract monthly data
        monthly_data = data[start_day:end_day, :, :]

        # STEP 1:
        # Daily India spatial mean rainfall
        daily_mean = np.nanmean(
            monthly_data,
            axis=(1,2)
        )

        # STEP 2:
        # Monthly accumulated rainfall
        monthly_rainfall = np.nansum(daily_mean)

        # Save
        all_data.append([
            year,
            month,
            round(monthly_rainfall, 2)
        ])

        start_day = end_day

# ------------------------------------------------------------
# CREATE DATAFRAME
# ------------------------------------------------------------

final_df = pd.DataFrame(
    all_data,
    columns=[
        "Year",
        "Month",
        "Rainfall_mm"
    ]
)

# ------------------------------------------------------------
# SAVE CSV
# ------------------------------------------------------------

final_df.to_csv(
    output_csv,
    index=False
)

print("\n================================")
print("MONTHLY RAINFALL CSV CREATED")
print("================================")

print(output_csv)