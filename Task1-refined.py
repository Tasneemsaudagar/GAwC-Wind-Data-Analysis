#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import matplotlib.pyplot as plt
import itertools
import numpy as np
from windrose import WindroseAxes
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import scipy.stats as stats
import numpy as np

file_path = r"E:\tasneem\GAwC\M1 mast Data.txt"
data = pd.read_csv(
    file_path,
    sep="\t",
    engine="python",
    skiprows=23,   
    on_bad_lines="skip"
)

data.columns = [col.split("|")[0] for col in data.columns]
print(data.columns)

data["TimeStamp"] = pd.to_datetime(data["TimeStamp"])


for col in data.columns:
    if "MeanWindSpeed" in col or "Direction" in col or "TurbInt" in col:
        data[col] = pd.to_numeric(data[col], errors="coerce")


#Apply Wind Speed Filter (0–100 m/s)
for col in data.columns:
    if "MeanWindSpeed" in col:
        data = data[(data[col] >= 0) & (data[col] <= 100)]


#apply the directions(0-360)
for col in data.columns:
    if "Direction" in col:
        data = data[(data[col] >= 0) & (data[col] <= 360)]


wind_cols = [
"MeanWindSpeedUID_120.0m_1",
"MeanWindSpeedUID_100.0m_2",
"MeanWindSpeedUID_80.0m_3",
"MeanWindSpeedUID_60.0m_4",
"MeanWindSpeedUID_40.0m_6"
]

dir_cols = [
"DirectionUID_120.0m_1",
"DirectionUID_100.0m_2",
"DirectionUID_80.0m_3",
"DirectionUID_60.0m_4",
"DirectionUID_40.0m_6"
]

turb_cols = [
"TurbIntUID_120.0m_1",
"TurbIntUID_100.0m_2",
"TurbIntUID_80.0m_3",
"TurbIntUID_60.0m_4",
"TurbIntUID_40.0m_6"
]



plt.figure(figsize=(12,6))

for col in wind_cols:
    smooth = data[col].rolling(window=20).mean()
    plt.plot(smooth.head(500), label=col, linewidth=2)

plt.title("Smoothed Wind Speed Variation at Different Heights")
plt.xlabel("Samples")
plt.ylabel("Wind Speed (m/s)")

plt.legend()
plt.grid(True)

plt.show()

weekly_avg = data.resample("W", on="TimeStamp")[wind_cols].mean()

plt.figure(figsize=(12,6))

for col,height in zip(wind_cols,heights):
    plt.plot(weekly_avg.index, weekly_avg[col], marker="o", label=f"{height}m")

plt.xlabel("Date")
plt.ylabel("Wind Speed (m/s)")
plt.title("Weekly Average Wind Speed")

plt.legend()
plt.grid(True)

plt.show()

monthly_avg = data.resample("M", on="TimeStamp")[wind_cols].mean()

plt.figure(figsize=(10,6))

for col,height in zip(wind_cols,heights):
    plt.plot(monthly_avg.index, monthly_avg[col], marker="o", label=f"{height}m")

plt.xlabel("Time")
plt.ylabel("Average Wind Speed (m/s)")
plt.title("Monthly Wind Speed Variation")

plt.legend()
plt.grid(True)

plt.show()

data["Hour"] = data["TimeStamp"].dt.hour

hourly_avg = data.groupby("Hour")[wind_cols].mean()

heatmap_data = hourly_avg.T

plt.figure(figsize=(12,6))

sns.heatmap(
heatmap_data,
cmap="viridis",
cbar_kws={'label':'Wind Speed (m/s)'}
)

plt.xlabel("Hour of Day")
plt.ylabel("Height")
plt.title("24 Hour Wind Speed Heatmap")

plt.show()

for col,height in zip(wind_cols,heights):

    plt.figure(figsize=(6,4))

    plt.hist(data[col].dropna(), bins=30)

    plt.xlabel("Wind Speed (m/s)")
    plt.ylabel("Frequency")

    plt.title(f"Wind Speed Histogram ({height}m)")

    plt.grid(True)

    plt.show()

for col,height in zip(wind_cols,heights):

    speed = data[col].dropna()

    shape,loc,scale = stats.weibull_min.fit(speed, floc=0)

    x = np.linspace(0, speed.max(), 100)

    pdf = stats.weibull_min.pdf(x, shape, loc, scale)

    plt.figure(figsize=(8,5))

    plt.hist(speed, bins=30, density=True, alpha=0.6, label="Wind Speed Data")

    plt.plot(x, pdf, 'r-', label="Weibull Fit")

    plt.xlabel("Wind Speed (m/s)")
    plt.ylabel("Probability Density")

    plt.title(f"Weibull Distribution ({height}m)")

    plt.legend()
    plt.grid(True)

    plt.show()

corr = data[wind_cols].corr()

plt.figure(figsize=(8,6))

sns.heatmap(corr, annot=True, cmap="coolwarm")

plt.title("Wind Speed Correlation Between Heights")

plt.show()


data[wind_cols].describe()

avg_speed = [data[col].mean() for col in wind_cols]

plt.figure(figsize=(6,8))

plt.plot(avg_speed, heights, marker='o')

plt.xlabel("Average Wind Speed (m/s)")
plt.ylabel("Height (m)")
plt.title("Wind Shear Profile")

plt.grid(True)

plt.show()

for w,t,height in zip(wind_cols,turb_cols,heights):

    plt.figure(figsize=(6,4))

    plt.scatter(data[w], data[t], alpha=0.4)

    plt.xlabel("Wind Speed (m/s)")
    plt.ylabel("Turbulence Intensity")

    plt.title(f"TI vs Wind Speed ({height}m)")

    plt.grid(True)

    plt.show()

compass_ticks = [0, 45, 90, 135, 180, 225, 270, 315, 360]
compass_labels = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW', 'N']

for w, d, height in zip(wind_cols, dir_cols, heights):
    plt.figure(figsize=(6,4))
    
    plt.scatter(data[d], data[w], alpha=0.4)
    
    plt.xticks(compass_ticks, compass_labels)
    
    plt.xlabel("Wind Direction")
    plt.ylabel("Wind Speed (m/s)")
    plt.title(f"Wind Speed vs Direction ({height} m)")
    
    plt.grid(True)
    plt.show()

for w,d,height in zip(wind_cols,dir_cols,heights):

    speed = data[w].dropna()
    direction = data[d].dropna()

    fig = plt.figure(figsize=(7,7))

    ax = WindroseAxes.from_ax()

    ax.bar(direction, speed, normed=True, opening=0.8, edgecolor='white')

    ax.set_title(f"Wind Rose ({height}m)")

    plt.show()


speed_data = [data[col].dropna() for col in wind_cols]

plt.figure(figsize=(8,5))

plt.boxplot(speed_data, labels=["120m","100m","80m","60m","40m"])

plt.ylabel("Wind Speed (m/s)")
plt.title("Wind Speed Distribution by Height")

plt.show()

availability = data[wind_cols].notna().mean()*100

plt.figure(figsize=(8,5))

plt.bar(["120m","100m","80m","60m","40m"], availability)

plt.ylabel("Data Availability (%)")
plt.title("Wind Data Availability")

plt.show()

plt.figure(figsize=(8,5))

for col,height in zip(wind_cols,heights):

    sns.kdeplot(data[col].dropna(), label=f"{height}m")

plt.xlabel("Wind Speed (m/s)")
plt.ylabel("Density")

plt.title("Wind Speed Probability Density")

plt.legend()

plt.grid(True)

plt.show()

for col,height in zip(turb_cols,heights):

    plt.figure(figsize=(7,5))

    plt.hist(data[col].dropna(), bins=30)

    plt.xlabel("Turbulence Intensity")
    plt.ylabel("Frequency")

    plt.title(f"Turbulence Intensity Distribution ({height}m)")

    plt.grid(True)

    plt.show()

for col,height in zip(wind_cols,heights):

    wind_speed = data[col].dropna()

    x = np.sort(wind_speed)

    y = np.arange(1, len(x)+1) / len(x)

    plt.figure(figsize=(8,5))

    plt.plot(x, y, marker=".", linestyle="none")

    plt.xlabel("Wind Speed (m/s)")
    plt.ylabel("ECDF")

    plt.title(f"ECDF of Wind Speed ({height}m)")

    plt.grid(True)

    plt.show()

air_density = 1.225

for col,height in zip(wind_cols,heights):

    speed = data[col].dropna()

    power_density = 0.5 * air_density * (speed**3)

    plt.figure(figsize=(7,5))

    plt.scatter(speed, power_density, alpha=0.3)

    plt.xlabel("Wind Speed (m/s)")
    plt.ylabel("Power Density (W/m²)")

    plt.title(f"Wind Power Density vs Wind Speed ({height}m)")

    plt.grid(True)

    plt.show()