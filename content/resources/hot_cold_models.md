---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.14.5
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

+++ {"user_expressions": []}

(resource:hot_cold)=
# Worksheet: Comparing total cloud fraction in hot and cold models

This notebook is motivated by  [Zelinka et al., 2020](https://www.dropbox.com/s/2mbf87tdviosdki/Geophysical%20Research%20Letters%20-%202020%20-%20Zelinka%20-%20Causes%20of%20Higher%20Climate%20Sensitivity%20in%20CMIP6%20Models.pdf?dl=0) which includes
a  supplementary [table S1](https://www.dropbox.com/s/5l7kmf2rxhflgpc/zelinka_grl_supplement.pdf?dl=0) that
lists the equilibrium climate senitivity for 27 CMIP6 models.

They find that differences in southern ocean low cloud amount can explain much of the climate
sensitivity differences.  Below we ask you to compare southern ocean cloud fraction for 
a high and low climate sensitivity model run.

Below we compare the total cloud fraction [clt](https://cmip-publications.llnl.gov/view/CMIP6/?type=variable&option=clt%20-%20Total%20Cloud%20Cover%20Percentage)
for CESM2 (NCAR) and MIROC6 (Japan)



Things to note in this notebook

- {ref}`sec:lazy`
- {ref}`sec:isel`
- {ref}`sec:checkpoint`
- {ref}`sec:weighted`


Bottom line:  These two models have very different ideas about the cloud fraction over the Southern Ocean


```{code-cell} ipython3
import intake
import xarray
```

+++ {"user_expressions": []}

## Load the catalog

At import time, intake-esm plugin is available in intake’s registry as
`esm_datastore` and can be accessed with `intake.open_esm_datastore()` function.
Use the `intake_esm.tutorial.get_url()` method to access smaller subsetted catalogs for tutorial purposes.

```{code-cell} ipython3
import intake_esm
url ="https://raw.githubusercontent.com/NCAR/intake-esm-datastore/master/catalogs/pangeo-cmip6.json"
```

```{code-cell} ipython3
cat = intake.open_esm_datastore(url)
cat
```

+++ {"user_expressions": []}

The summary above tells us that this catalog contains 514818 data assets.
We can get more information on the individual data assets contained in the
catalog by looking at the underlying pandas dataframe created when we load the catalog:

```{code-cell} ipython3
cat.df
```

+++ {"user_expressions": []}

The first data asset listed in the catalog contains:

- the surace pressure (variable_id='ps'), as a function of latitude, longitude, time,

- the high resolution version of the CMCC climate model (source_id='CMCC-CM2-HR4'),

- the high resolution model intercomparison expermenet (experiment_id='HighResMIP'),

- developed by the Euro-Mediterranean Centre on Climate Change (instution_id='CMCC'),

- run as part of the Coupled Model Intercomparison Project (activity_id='CMIP')

And is located in Google Cloud Storage at 'gs://cmip6/CMIP6/HighResMIP/CMCC/CMCC-CM2-HR4/highresSST-present/r1i1p1f1/Amon/ps/gn/v20170706/"

## Finding unique entries

To get unique values for given columns in the catalog, intake-esm provides a
{py:meth}`~intake_esm.core.esm_datastore.unique` method:

Let's query the data catalog to see what models(`source_id`), experiments
(`experiment_id`) and temporal frequencies (`table_id`) are available.

```{code-cell} ipython3
unique = cat.unique()
unique
```

```{code-cell} ipython3
unique['source_id'].sort()
unique['source_id'][:10]
```

```{code-cell} ipython3
experiments = unique['experiment_id']
```

```{code-cell} ipython3
experiments.sort()
experiments[:10]
```

```{code-cell} ipython3
unique['table_id'][:10]
```

+++ {"user_expressions": []}

## Q1: find a low and a high climate sensitivity model


For the low sensitivity, I'll use MIROC6, ECS = 2.6 K/doubling, for the high sensitivity,  CESM2, ECS = 5.15 K/doubling

+++ {"user_expressions": []}

## Q2: cloud fraction

Check the variable list at [https://pcmdi.llnl.gov/mips/cmip3/variableList.html#overview](https://pcmdi.llnl.gov/mips/cmip3/variableList.html#overview)

What is the difference between **cl** and **clt**?  What table do they belong to?

These are both monthly averaged atmospheric variables in the table Amon -- clt is averaged over height and is 3 dimensional
(time, lon, lat) while cl is four dimensional (time, height, lon, lat)

+++ {"user_expressions": []}

## Q3 Grab one realization from each of your two models for two scenarios: historical and ssp585

First we need to find the available realizations.  To do this, get every realization by
leaving "member_id" unspecified. Note that there are 50 realization for the historical runs

```{code-cell} ipython3
cat_subset = cat.search(
    experiment_id=["historical","ssp585"],
    table_id=["Amon","fx"],
    source_id = ["CESM2","MIROC6"],
    variable_id=["clt","areacella"],
    grid_label="gn")
cat_subset.df.tail()
```

+++ {"user_expressions": []}

Now sort by member_id to get a common realization -- everyone has member_id = "r10i1p1f1"

```{code-cell} ipython3
cat_subset.search(experiment_id = ["historical","ssp585"],source_id=["CESM2","MIROC6"]).df.sort_values("member_id").head()
```

+++ {"user_expressions": []}

So grab these four realizations, plus the areacella weights for each of them.

```{code-cell} ipython3
single_realization = cat_subset.search(experiment_id = ["historical","ssp585"],source_id=["CESM2","MIROC6"],member_id = "r10i1p1f1")
```

```{code-cell} ipython3
:user_expressions: []

single_realization.df
```

+++ {"user_expressions": []}

(sec:lazy)=
## lazy-loading datasets by row

+++ {"user_expressions": []}

We can use [xarray.open_dataset](https://docs.xarray.dev/en/stable/generated/xarray.open_dataset.html) to read in the metadata from a google store zstore url.  This can take a few seconds, but it's "lazy" in the
sense that no data is read until some calculation (a plot, average, etc.) is conducted.  If you want to force a data read,
use [xarray.load_dataset](https://docs.xarray.dev/en/stable/generated/xarray.load_dataset.html)

```{code-cell} ipython3
# get aeracella for miroc6 historical r10i1p1f1
ds = xarray.open_zarr(single_realization.df.iloc[0]['zstore'])
ds
```

+++ {"user_expressions": []}

## Load datasets using `to_dataset_dict()`

Intake-esm implements convenience utilities for loading the query results into
higher level xarray datasets. The logic for merging/concatenating the query
results into higher level xarray datasets is provided in the input JSON file and
is available under `.aggregation_info` property of the catalog:

```{code-cell} ipython3
cat.esmcat.aggregation_control
```

+++ {"user_expressions": []}

The purpose of aggregation control is to combine variable datasets from the same table_id into a single dataset if possible.

+++ {"user_expressions": []}

### Get the 8 datasets (this is a lazy operation)

The following command reads in the consolidated metadata, but doesn't grab any actual data.
The data reads will occur later when  you make select operations.

The advantage of using `to_dataset_dict` over the raw `open_zarr` is that this this produces a dictionary with
keys that mark the institution, model, scenario, table an grid.

```{code-cell} ipython3
dset_dict = single_realization.to_dataset_dict(
        xarray_open_kwargs={"consolidated": True, "decode_times": True, "use_cftime": True}
    )
```

```{code-cell} ipython3
dset_dict.keys()
```

+++ {"user_expressions": []}

## Keep track of the `areacella` for each dataset

To keep track of the variables and weights, it helps to have the keys in two sorted lists

```{code-cell} ipython3
fx_keys = [key for key in dset_dict.keys() if key.find('fx') > -1]
cl_keys = [key for key in dset_dict.keys() if key.find('Amon') > -1]
fx_keys.sort()
cl_keys.sort()
fx_keys, cl_keys
```

+++ {"user_expressions": []}

(sec:isel)=
## limiting the dataset to the Sourthern Ocean without reading the data

To fetch the minimum amount of data, you can use [xarray.isel](https://docs.xarray.dev/en/stable/user-guide/indexing.html#vectorized-indexing) to
describe a slice that will be applied when a calculation is done.

```{code-cell} ipython3
def get_so(the_ds):
    """
    slice the dataset for latitudes south of -30 degrees
    """
    #
    # logical index of all latitudes south of -30
    #
    hit = the_ds.lat < -30
    so_slice = the_ds.isel(indexers = {'lat':hit})
    return so_slice
```

+++ {"user_expressions": []}

This reduces the latitude dimension size from 128 to 43, so your file size is 1/3 of the full dataset size

```{code-cell} ipython3
for key, ds in dset_dict.items():
    dset_dict[key]=get_so(ds)
```

+++ {"user_expressions": []}

(sec:checkpoint)=
## saving a checkpoint

You might want to load the dataset into memory (be careful) and save to disk for future acesss.  You
can preview how much space you'll need with [xarray.dataset.nbytes](https://docs.xarray.dev/en/stable/generated/xarray.Dataset.nbytes.html)

The cell below shows how to checkpoint the datasets to disk and restore from disk back to a dictionary

+++ {"user_expressions": []}

```python
readit = True
write_files = False
out_dir = home /"cmip6_files"
out_dir.mkdir(exist_ok=True,parents=True)
filenames=['cesm2_ssp585.nc','cesm2_historicial.nc','miroc6_ssp585.nc','miroc6_historical.nc']
dataset_names =['ScenarioMIP.NCAR.CESM2.ssp585.Amon.gn',
     'CMIP.NCAR.CESM2.historical.Amon.gn',
     'ScenarioMIP.MIROC.MIROC6.ssp585.Amon.gn',
     'CMIP.MIROC.MIROC6.historical.Amon.gn']
if readit:
    #
    # download over the internet
    #
    dset_dict = single_realization.to_dataset_dict(
        xarray_open_kwargs={"consolidated": True, "decode_times": True, "use_cftime": True}
    )
    if write_files:
        for ds, filename in zip(dset_dict.values(),filenames):
            out_file = out_dir / filename
            print(f"writing {out_file}")
            ds.to_netcdf(out_file)
else:
    #
    # read from a diskfile
    #
    dset_dict = dict()
    dset_dict[dataset_name]=xr.open_dataset(the_file)
```

+++ {"user_expressions": []}

(sec:weighted)=
## Find the area weighted cloud fraction for 1 dataset over the southern ocean

Note that I don't need a long variable name that includes all the metadata,
I can get that information at any point from the variable itself

```{code-cell} ipython3
ds = dset_dict['ScenarioMIP.NCAR.CESM2.ssp585.Amon.gn']
weights = dset_dict['ScenarioMIP.NCAR.CESM2.ssp585.fx.gn']['areacella']
print(f"{ds.experiment_id=}, {ds.member_id.data[0]=}, {ds.source_id=}")
ds
```

+++ {"user_expressions": []}

### The areacella weights

We're on a sphere, so every latitude band is going to have grid cells with different areas.  The grid size
will vary between models, so it's important to do weighted averages.

```{code-cell} ipython3
weights
```

+++ {"user_expressions": []}

### squeeze out the unit dimensions

Our variables come indexed over member id and starting year, but since we only have 1 member_id and 1 starting year, we
can squeeze those out

```{code-cell} ipython3
ds['clt'].shape
```

```{code-cell} ipython3
ds = ds.squeeze()
weights = weights.squeeze()
```

+++ {"user_expressions": []}

### use the weighted method to apply weights to the average

The [dataArray.weighted](https://docs.xarray.dev/en/stable/generated/xarray.DataArray.weighted.html) method makes a dataArray "weight aware".
You want to make sure you copy this weighted dataArray to a new variable, because it wipes out all of the dataArray metadata


+++ {"user_expressions": []}

### Add weights to the dataArray

```{code-cell} ipython3
clt_so  = ds['clt']
clt_so =  ds['clt'].weighted(weights)
clt_so
```

+++ {"user_expressions": []}

### Take the zonal mean

Note that this is the first statement that actually fetches variable values from google

```{code-cell} ipython3
:user_expressions: []

clt_so_zonal = clt_so.mean(dim=["lon","lat"])
clt_so_zonal
```

+++ {"user_expressions": []}

### Smooth the data with a rolling window

[https://docs.xarray.dev/en/stable/user-guide/computation.html#rolling-window-operations](https://docs.xarray.dev/en/stable/user-guide/computation.html#rolling-window-operations)

In the cell below I use a 5-year running mean to remove shorter-timescale flucuations. Note how
I include the metadata in the title for a legend entry.

```{code-cell} ipython3
:user_expressions: []

from matplotlib import pyplot as plt
rolling = clt_so_zonal.rolling(time=60)
clt_mean = rolling.mean()
fig, ax = plt.subplots(1,1,figsize=(8,8))
clt_mean.plot(ax=ax,label = f"{ds.experiment_id}, {ds.source_id}")
ax.grid(True)
ax.set(title="southern ocean cloud fraction",
    xlabel="time (years)", ylabel = "cloud fraction (percent)")
fig.legend();
```

+++ {"user_expressions": []}

## now add miroc6

Make a function so we don't need to copy/paste sells

```{code-cell} ipython3
def make_average(ds, weights):
    ds = ds.squeeze()
    weights = weights.squeeze()
    clt_so_weighted = ds['clt'].weighted(weights)
    clt_so_zonal = clt_so_weighted.mean(dim=["lon","lat"])
    rolling = clt_so_zonal.rolling(time=60)
    clt_mean = rolling.mean()
    return clt_mean
```

+++ {"user_expressions": []}

## add the miroc 5 year rolling mean to the plot

looks like, for these realizations, there's a pretty dramatic difference between the hot and cold models

```{code-cell} ipython3
ds_miroc =dset_dict['ScenarioMIP.MIROC.MIROC6.ssp585.Amon.gn']
weights_miroc = dset_dict['ScenarioMIP.MIROC.MIROC6.ssp585.fx.gn']['areacella']
miroc6_clt_mean = make_average(ds_miroc, weights_miroc)
miroc6_clt_mean.plot(ax=ax,label = f"{ds.source_id}, {ds.source_id}")
ax.set(title = (f"Southern ocean cloud fraction comparison: "
                f"{ds.source_id}:{ds.experiment_id} vs "
                f"{ds_miroc.source_id}:{ds_miroc.experiment_id}"),
       xlabel = "time (year)", ylabel = "cloud faction (percent)")
fig.legend()
display(fig)
```

+++ {"user_expressions": []}

## Historical runs

```{code-cell} ipython3
dset_dict.keys()
```

```{code-cell} ipython3
ds_miroc =dset_dict['CMIP.MIROC.MIROC6.historical.Amon.gn']
weights_miroc = dset_dict['CMIP.MIROC.MIROC6.historical.fx.gn']['areacella']
miroc6_clt_mean = make_average(ds_miroc, weights_miroc)
miroc6_clt_mean.plot(ax=ax,label = f"{ds.source_id}, {ds.source_id}")
ds_cesm =dset_dict['CMIP.NCAR.CESM2.historical.Amon.gn']
weights_cesm = dset_dict['CMIP.NCAR.CESM2.historical.fx.gn']['areacella']
cesm_clt_mean = make_average(ds_cesm, weights_cesm)
cesm_clt_mean.plot(ax=ax,label = f"{ds.source_id}, {ds.source_id}")
ax.set(title = (f"Southern ocean cloud fraction comparison: "
                f"{ds.source_id}:{ds.experiment_id} vs "
                f"{ds_miroc.source_id}:{ds_miroc.experiment_id}"),
       xlabel = "time (year)", ylabel = "cloud faction (percent)")
fig.legend()
display(fig)
```
