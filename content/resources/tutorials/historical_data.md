---
jupytext:
  formats: ipynb,md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.16.6
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

# Tutorial: Loading CMIP historical data 

Author: Ben Farris

In this notebook, we focus on loading in the data from the CMIP6 site for British Columbia and
saving it to netcdf. We can then work on histogramming the data in order to understand the variability within the models.  The models are the Canadian CanESM, the British Hadley model and the US GISS model

Based on [project pythia](https://projectpythia.org/cmip6-cookbook/notebooks/foundations/intake-esm.html)

This notebook and the netcdf files are in the [tutorials](https://drive.google.com/drive/folders/1ktPMS5IaZYox06MYTd9CP5pKle7Coocs) folder on our google drive.

## Installation

To generate the Taylor diagram in the last cell you'll need to do install the skillmetrics module into the e440 environment:

```
pip install skillmetrics
```

### Data download

In order to avoid repeatedly downloading the data, each model download is wrapped in an if statement, so that if
`writefile` is set to True, the download will be written to a folder called

```
~/repos/e440/tutorials/tutorial_data
```

These same files are in the `tutorials/tutorial_data` folder on our google drive if you want to skip all downloads and just
copy them into the tutorial_data folder

```{code-cell} ipython3
# Import statements
import xarray as xr
xr.set_options(display_style='html')
import intake
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import cartopy.crs as ccrs
import cartopy
```

Pull the data from the site itself and put into pandas df in order to be able to visualize it. Following similar steps to project pythia

```{code-cell} ipython3
cat_url = "https://storage.googleapis.com/cmip6/pangeo-cmip6.json"
col = intake.open_esm_datastore(cat_url)
col.df
```

Look at the unique keys for all the entries in order to find the models we want

```{code-cell} ipython3
cmipdf = col.df
cmipdf['source_id'].unique()
```

## Model downloads

+++

From above, we know that we need 3 specific models/source_ids: CanESM5, HadGEM3-GC31-MM, GISS-E2-1-H. In addition to this, we know that we want monthly precipitation data, so we need variable_id = "pr" and table_id = "Amon". Lastly, we'll also need the historical data at this point.

### CanESM5

+++

We want an approximate box of 115 to 135 lon and 49 to 60 lat, and we want a slice from 1960 to 2010. So, get closest lon lat slice and get the correct time from the site. Then write to file as a netcdf.  If
write = True this cell can take several minutes.

```{code-cell} ipython3
home_dir = Path.home()
out_folder = home_dir / "repos/e440/tutorials/tutorial_data"
def do_write(dataset,filename,out_folder):
    """
    write a cmip6 data set to the folder ~/repos/e440/tutorials/tutorial_data
    creating the folder if it doesn't already exist.  If the file exits,
    delete it before writing.
    """
    full_path = out_folder / filename
    if full_path.exists():
        full_path.unlink()
    out_folder.mkdir(parents=True,exist_ok=True)
    dataset.load().to_netcdf(full_path,'w')
    return full_path
   
```

```{code-cell} ipython3
filename = "can_bc_dset.nc"
full_path = out_folder / filename
var_key = "CMIP.CCCma.CanESM5.historical.Amon.gn"
#
# if wrie_file is true this will download and write the file to tutorial_data
#
write_file = False
if write_file:
    can_subset = col.search(table_id="Amon", variable_id = "pr", source_id = "CanESM5", experiment_id = 'historical')
    dset_dict = can_subset.to_dataset_dict(zarr_kwargs={'consolidated':True})
    can_dset = dset_dict[var_key]
    can_bc_dset = can_dset.sel(lon = slice(225.,239.0625), lat = slice(48.835241, 59.99702), time = slice('1960', '2010'))
    full_path = do_write(can_bc_dset,filename,out_folder)
    print(f"got here, writing {full_path=}")
#
# read the netcdffile
#
can_bc_dset = xr.open_dataset(full_path)
```

```{code-cell} ipython3

```

Read in the data from the netcdf file and begin plotting the data

```{code-cell} ipython3
mean_precip = can_bc_dset.groupby('time.year').mean('time').mean(['lon', 'lat'])*86400*365
plt.figure()
mean_precip.mean('member_id').pr.plot()
plt.title("Averaged Yearly precipitation for the CanESM5 GCM")
plt.xlabel('Year')
plt.ylabel('Precipitation total (mm)')
```

Looking at what the monthly precipitation pattern looks like for 1960-2010

```{code-cell} ipython3
mean_precip_monthly = can_bc_dset.groupby('time.month').mean('time').mean(['lon', 'lat'])*86400*30.4
plt.figure()
mean_precip_monthly.mean('member_id').pr.plot()
plt.title("Averaged Monthly precipitation for the CanESM5 GCM")
plt.xlabel('Month')
plt.ylabel('Precipitation total (mm)')
```

Plotting standard deviation as a timeseries

```{code-cell} ipython3
var_precip = can_bc_dset.groupby('time.year').mean('time').mean(['lon', 'lat'])*86400*365
var_precip.std('member_id').pr.plot()
plt.title("Standard deviation of precipitation for the CanESM5 members")
plt.xlabel('Year')
plt.ylabel('Precipitation total (mm)')
```

Getting an idea of the model member distribution via a histogram

```{code-cell} ipython3
hist_data = can_bc_dset.groupby('time.year').mean('time').mean(['lon', 'lat'])*86400*365
hist_data = hist_data.sel(year=2010)
hist_data.pr.plot.hist()
plt.title("2010 Precipitation Average distribution across the CanESM5 members")
plt.xlabel('Precipitation total (mm)')
plt.ylabel('Number')
```

Try plotting on a map to see what data looks like

```{code-cell} ipython3
## Try plotting on a map for 2010

data2010 = can_bc_dset.sel(time='2010')
precip_data2010 = data2010.groupby('time.year').mean('time')*86400*365
precip_data2010 = precip_data2010.mean('member_id')

fig = plt.figure(1, figsize=[30,13])

ax = plt.subplot(1, 1, 1, projection=ccrs.PlateCarree())
ax.coastlines()
ax.add_feature(cartopy.feature.BORDERS, linestyle='-', alpha=1)
ax.set_extent([-140, -110, 44, 60])

resol = '50m'

provinc_bodr = cartopy.feature.NaturalEarthFeature(category='cultural', 
    name='admin_1_states_provinces_lines', scale=resol, facecolor='none', edgecolor='k')
ax.add_feature(provinc_bodr, linestyle='--', linewidth=0.6, edgecolor="k", zorder=10)



precip_data2010.pr.plot(ax=ax,cmap='coolwarm')
ax.title.set_text("Precipitation total for 2010")
```

### HadGEM3

Repeat the same steps as for the CanESM

```{code-cell} ipython3
var_key = 'CMIP.MOHC.HadGEM3-GC31-MM.historical.Amon.gn'
filename = "had_bc_dset.nc"
full_path = out_folder / filename
write_file = False
if write_file:
    had_subset = col.search(table_id="Amon", variable_id = "pr", source_id = "HadGEM3-GC31-MM", experiment_id = 'historical')
    dset_dict = had_subset.to_dataset_dict(zarr_kwargs={'consolidated':True})
    had_dset = dset_dict[var_key]
    had_bc_dset = had_dset.sel(lon = slice(225.4, 239.6), lat = slice(48.835241, 59.99702), time = slice('1960', '2010'))
    had_bc_dset.load().to_netcdf('had_bc_dset.nc')
    full_path = do_write(had_bc_dset,filename,out_folder)
    print(f"got here for hadley, writing {full_path=}")
#
# read the netcdffile
#
had_bc_dset = xr.open_dataset(full_path)
```

```{code-cell} ipython3
mean_precip_had = had_bc_dset.groupby('time.year').mean('time').mean(['lon', 'lat'])*86400*365
plt.figure()
mean_precip_had.mean('member_id').pr.plot()
plt.title("Averaged Yearly precipitation for the HadGEM3 GCM")
plt.xlabel('Year')
plt.ylabel('Precipitation total (mm)')
```

```{code-cell} ipython3
had_std_precip = had_bc_dset.groupby('time.year').mean('time').mean(['lon', 'lat'])*86400*365
had_std_precip.std('member_id').pr.plot()
plt.title("Standard deviation of precipitation for the HadGEM members")
plt.xlabel('Year')
plt.ylabel('Precipitation total (mm)')
```

```{code-cell} ipython3
had_hist_data = had_bc_dset.groupby('time.year').mean('time').mean(['lon', 'lat'])*86400*365
had_hist_data = had_hist_data.sel(year=2010)
had_hist_data.pr.plot.hist()
plt.title("2010 Precipitation Average distribution across the HadGEM members")
plt.xlabel('Precipitation total (mm)')
plt.ylabel('Number')
```

```{code-cell} ipython3
had_data2010 = had_bc_dset.sel(time='2005')
had_precip_data2010 = had_data2010.groupby('time.year').mean('time')*86400*365
had_precip_data2010 = had_precip_data2010.mean('member_id')

fig = plt.figure(1, figsize=[30,13])

ax2 = plt.subplot(1, 1, 1, projection=ccrs.PlateCarree())
ax2.coastlines()
ax2.add_feature(cartopy.feature.BORDERS, linestyle='-', alpha=1)
ax2.set_extent([-140, -110, 40, 60])

resol = '50m'

provinc_bodr = cartopy.feature.NaturalEarthFeature(category='cultural', 
    name='admin_1_states_provinces_lines', scale=resol, facecolor='none', edgecolor='k')
ax2.add_feature(provinc_bodr, linestyle='--', linewidth=0.6, edgecolor="k", zorder=10)



had_precip_data2010.pr.plot(ax=ax2,cmap='coolwarm')
ax.title.set_text("Precipitation total for 2010")
```

### GISS

Repeat the same steps as for CanESM and HadGEM

```{code-cell} ipython3
var_key = 'CMIP.NASA-GISS.GISS-E2-1-H.historical.Amon.gn'
filename = 'gis_bc_dset.nc'
full_path = out_folder / filename

write_file = False
if write_file:
    gis_subset = col.search(table_id="Amon", variable_id = "pr", source_id = "GISS-E2-1-H", experiment_id = 'historical')
    dset_dict = gis_subset.to_dataset_dict(zarr_kwargs={'consolidated':True})
    gis_dset = dset_dict[var_key]
    gis_bc_dset = gis_dset.sel(lon = slice(226.25, 238.75), lat = slice(48.835241, 59.99702), time = slice('1960', '2010'))
    full_path = do_write(gis_bc_dset,filename,out_folder)
    print(f"got here: giss, writing {full_path=}")
#
# read the netcdffile
#
gis_bc_dset = xr.open_dataset(full_path)
```

```{code-cell} ipython3
mean_precip_gis = gis_bc_dset.groupby('time.year').mean('time').mean(['lon', 'lat'])*86400*365
plt.figure()
mean_precip_gis.mean('member_id').pr.plot()
plt.title("Averaged Yearly precipitation for the GISS GCM")
plt.xlabel('Year')
plt.ylabel('Precipitation total (mm)')
```

```{code-cell} ipython3
gis_std_precip = gis_bc_dset.groupby('time.year').mean('time').mean(['lon', 'lat'])*86400*365
gis_std_precip.std('member_id').pr.plot()
plt.title("Standard deviation of precipitation for the HadGEM members")
plt.xlabel('Year')
plt.ylabel('Precipitation total (mm)')
```

```{code-cell} ipython3
gis_hist_data = gis_bc_dset.groupby('time.year').mean('time').mean(['lon', 'lat'])*86400*365
gis_hist_data = gis_hist_data.sel(year=2010)
gis_hist_data.pr.plot.hist()
plt.title("2010 Precipitation Average distribution across the GISS members")
plt.xlabel('Precipitation total (mm)')
plt.ylabel('Number')
```

```{code-cell} ipython3
gis_data1990 = gis_bc_dset.sel(time='2010')
gis_precip_data1990 = gis_data1990.groupby('time.year').mean('time')*86400*365
gis_precip_data1990 = gis_precip_data1990.mean('member_id')

fig = plt.figure(1, figsize=[30,13])

ax = plt.subplot(1, 1, 1, projection=ccrs.PlateCarree())
ax.coastlines()
ax.add_feature(cartopy.feature.BORDERS, linestyle='-', alpha=1)
ax.set_extent([-140, -110, 40, 60])

resol = '50m'

provinc_bodr = cartopy.feature.NaturalEarthFeature(category='cultural', 
    name='admin_1_states_provinces_lines', scale=resol, facecolor='none', edgecolor='k')
ax.add_feature(provinc_bodr, linestyle='--', linewidth=0.6, edgecolor="k", zorder=10)



gis_precip_data1990.pr.plot(ax=ax,cmap='coolwarm')
```

### Creating plots with all 3 models

```{code-cell} ipython3
time = mean_precip_gis.year
fig, axs = plt.subplots(1, 1, figsize=(30, 13))
axs.plot(time,mean_precip_gis.mean('member_id').pr)
axs.plot(time, mean_precip_had.mean('member_id').pr)
axs.plot(time, mean_precip.mean('member_id').pr)
```

```{code-cell} ipython3
import skill_metrics as sm
import numpy as np

ref = mean_precip.mean('member_id').pr.to_numpy().flatten()
can = ref
had = mean_precip_had.mean('member_id').pr.to_numpy().flatten()
gis = mean_precip_gis.mean('member_id').pr.to_numpy().flatten()

data = {'ref': ref, 'can': can, 'had': had, 'gis':gis}

taylor_stats1 = sm.taylor_statistics(data['can'], data['ref'], 'data')
taylor_stats2 = sm.taylor_statistics(data['had'], data['ref'], 'data')
taylor_stats3 = sm.taylor_statistics(data['gis'], data['ref'], 'data')

sdev = np.array([taylor_stats1['sdev'][0], taylor_stats1['sdev'][1], 
                 taylor_stats2['sdev'][1], taylor_stats3['sdev'][1]])
crmsd = np.array([taylor_stats1['crmsd'][0], taylor_stats1['crmsd'][1], 
                  taylor_stats2['crmsd'][1], taylor_stats3['crmsd'][1]])
ccoef = np.array([taylor_stats1['ccoef'][0], taylor_stats1['ccoef'][1], 
                  taylor_stats2['ccoef'][1], taylor_stats3['ccoef'][1]])

# Specify labels for points in a cell array (M1 for model prediction 1,
# etc.). Note that a label needs to be specified for the reference even
# though it is not used.
label = ['Non-Dimensional Observation', 'M1', 'M2', 'M3']

'''
Produce the Taylor diagram

Display the data points for correlations that vary from -1 to 1 (2
panels). Label the points and change the axis options for SDEV, CRMSD,
and CCOEF. Increase the upper limit for the SDEV axis and rotate the
CRMSD contour labels (counter-clockwise from x-axis). Exchange color and
line style choices for SDEV, CRMSD, and CCOEFF variables to show effect.
Increase the line width of all lines.

For an exhaustive list of options to customize your diagram, 
please call the function at a Python command line:
>> taylor_diagram
'''
sm.taylor_diagram(sdev,crmsd,ccoef,
                  numberPanels = 2,
                  markerLabel = label, markerLabelColor = 'r',
                  tickRMS = range(0,90,10), tickRMSangle = 150.0,
                  colRMS = 'm', styleRMS = ':', widthRMS = 2.0, 
                  titleRMS = 'off',
                  tickSTD = range(0, 80, 20), axismax = 60.0,
                  colSTD = 'b', styleSTD = '-.', widthSTD = 1.0,
                  colCOR = 'k', styleCOR = '--', widthCOR = 1.0)
```

```{code-cell} ipython3

```
