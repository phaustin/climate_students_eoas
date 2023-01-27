---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.14.4
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

+++ {"tags": []}

# Calculating ENSO with Xarray


+++

---

+++

## Overview

In this notebook, we will:

1. Load SST data from the CESM2 model
2. Mask data using `.where()`
3. Compute climatologies and anomalies using `.groupby()`
4. Use `.rolling()` to compute moving average
5. Compute, normalize, and plot the Niño 3.4 Index

+++

## Prerequisites


| Concepts | Importance | Notes |
| --- | --- | --- |
| [Introduction to Xarray](xarray-intro) | Necessary | |
| [Computation and Masking](computation-masking) | Necessary | |



- **Time to learn**: 20 minutes

+++

---

+++ {"tags": []}

## Imports 

```{code-cell} ipython3
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import xarray as xr
from pythia_datasets import DATASETS
```

+++ {"tags": []}

## The Niño 3.4 Index

+++


In this notebook, we are going to combine several topics we've covered so far to compute the [Niño 3.4 Index](https://climatedataguide.ucar.edu/climate-data/nino-sst-indices-nino-12-3-34-4-oni-and-tni) for the CESM2 submission for the [CMIP6 project](https://esgf-node.llnl.gov/projects/cmip6/). 

> Niño 3.4 (5N-5S, 170W-120W): The Niño 3.4 anomalies may be thought of as representing the average equatorial SSTs across the Pacific from about the dateline to the South American coast. The Niño 3.4 index typically uses a 5-month running mean, and El Niño or La Niña events are defined when the Niño 3.4 SSTs exceed +/- 0.4C for a period of six months or more.

> Nino X Index computation: (a) Compute area averaged total SST from Niño X region; (b) Compute monthly climatology (e.g., 1950-1979) for area averaged total SST from Niño X region, and subtract climatology from area averaged total SST time series to obtain anomalies; (c) Smooth the anomalies with a 5-month running mean; (d) Normalize the smoothed values by its standard deviation over the climatological period.

![](https://www.ncdc.noaa.gov/monitoring-content/teleconnections/nino-regions.gif)

At the end of this notebook, you should be able to produce a plot that looks similar to this [Oceanic Niño Index plot](https://climatedataguide.ucar.edu/sites/default/files/styles/extra_large/public/2022-03/indices_oni_2_2_lg.png):

![ONI index plot from NCAR Climate Data Guide](https://climatedataguide.ucar.edu/sites/default/files/styles/extra_large/public/2022-03/indices_oni_2_2_lg.png)

+++ {"tags": []}

Open the SST and areacello datasets, and use Xarray's `merge` method to combine them into a single dataset:

```{code-cell} ipython3
filepath = DATASETS.fetch('CESM2_sst_data.nc')
data = xr.open_dataset(filepath)
filepath2 = DATASETS.fetch('CESM2_grid_variables.nc')
areacello = xr.open_dataset(filepath2).areacello

ds = xr.merge([data, areacello])
ds
```

Visualize the first time slice to make sure the data looks as expected:

```{code-cell} ipython3
fig = plt.figure(figsize=(12, 6))
ax = plt.axes(projection=ccrs.Robinson(central_longitude=180))
ax.coastlines()
ax.gridlines()
ds.tos.isel(time=0).plot(
    ax=ax, transform=ccrs.PlateCarree(), vmin=-2, vmax=30, cmap='coolwarm'
);
```

## Select the Niño 3.4 region 

There are a couple ways to select the Niño 3.4 region:

1. Use `sel()` or `isel()`
2. Use `where()` and select all values within the bounds of interest

```{code-cell} ipython3
tos_nino34 = ds.sel(lat=slice(-5, 5), lon=slice(190, 240))
tos_nino34
```

The other option for selecting our region of interest is to use 

```{code-cell} ipython3
tos_nino34 = ds.where(
    (ds.lat < 5) & (ds.lat > -5) & (ds.lon > 190) & (ds.lon < 240), drop=True
)
tos_nino34
```

Let's plot the selected region to make sure we are doing the right thing.

```{code-cell} ipython3
fig = plt.figure(figsize=(12, 6))
ax = plt.axes(projection=ccrs.Robinson(central_longitude=180))
ax.coastlines()
ax.gridlines()
tos_nino34.tos.isel(time=0).plot(
    ax=ax, transform=ccrs.PlateCarree(), vmin=-2, vmax=30, cmap='coolwarm'
)
ax.set_extent((120, 300, 10, -10))
```

## Compute the anomalies

We first group by month and subtract the mean SST at each point in the Niño 3.4 region. We then compute the weighted average over the region to obtain the anomalies:

```{code-cell} ipython3
gb = tos_nino34.tos.groupby('time.month')
tos_nino34_anom = gb - gb.mean(dim='time')
index_nino34 = tos_nino34_anom.weighted(tos_nino34.areacello).mean(dim=['lat', 'lon'])
```

Now, smooth the anomalies with a 5-month running mean:

```{code-cell} ipython3
index_nino34_rolling_mean = index_nino34.rolling(time=5, center=True).mean()
```

```{code-cell} ipython3
index_nino34.plot(size=8)
index_nino34_rolling_mean.plot()
plt.legend(['anomaly', '5-month running mean anomaly'])
plt.title('SST anomaly over the Niño 3.4 region');
```

Compute the standard deviation of the SST in the Nino 3.4 region, over the entire time period of the data array:

```{code-cell} ipython3
std_dev = tos_nino34.tos.std()
std_dev
```

Then we'll normalize the values by dividing the rolling mean by the standard deviation of the SST in the Niño 3.4 region:

```{code-cell} ipython3
normalized_index_nino34_rolling_mean = index_nino34_rolling_mean / std_dev
```

## Visualize the computed Niño 3.4 index

+++

We will highlight values in excess of $\pm$0.5, roughly corresponding to El Niño (warm) and La Niña (cold) events.

```{code-cell} ipython3
fig = plt.figure(figsize=(12, 6))

plt.fill_between(
    normalized_index_nino34_rolling_mean.time.data,
    normalized_index_nino34_rolling_mean.where(
        normalized_index_nino34_rolling_mean >= 0.4
    ).data,
    0.4,
    color='red',
    alpha=0.9,
)
plt.fill_between(
    normalized_index_nino34_rolling_mean.time.data,
    normalized_index_nino34_rolling_mean.where(
        normalized_index_nino34_rolling_mean <= -0.4
    ).data,
    -0.4,
    color='blue',
    alpha=0.9,
)

normalized_index_nino34_rolling_mean.plot(color='black')
plt.axhline(0, color='black', lw=0.5)
plt.axhline(0.4, color='black', linewidth=0.5, linestyle='dotted')
plt.axhline(-0.4, color='black', linewidth=0.5, linestyle='dotted')
plt.title('Niño 3.4 Index');
```

---

+++

## Summary

We have applied a variety of Xarray's selection, grouping, and statistical functions to compute and visualize an important climate index. 

+++

## Resources and References

- [Niño 3.4 index](https://climatedataguide.ucar.edu/climate-data/nino-sst-indices-nino-12-3-34-4-oni-and-tni)
- [Matplotlib's `fill_between` method](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.fill_between.html)
- [Matplotlib's `axhline` method](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.axhline.html) (see also its analogous `axvline` method)

```{code-cell} ipython3

```
