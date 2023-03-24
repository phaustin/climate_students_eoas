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
# Worksheet: Comparing low cloud fraction in hot and cold models

This notebook is based on [Zelinka et al., 2020](https://www.dropbox.com/s/2mbf87tdviosdki/Geophysical%20Research%20Letters%20-%202020%20-%20Zelinka%20-%20Causes%20of%20Higher%20Climate%20Sensitivity%20in%20CMIP6%20Models.pdf?dl=0) which includes
a  supplementary [table S1](https://www.dropbox.com/s/5l7kmf2rxhflgpc/zelinka_grl_supplement.pdf?dl=0) that
lists the equilibrium climate senitivity for 27 CMIP6 models.

They find that differences in southern ocean low cloud amount can explain much of the climate
sensitivity differences.  Below we ask you to compare southern ocean cloud fraction for 
a high and low climate sensitivity model run

```{code-cell} ipython3
import intake
```

+++ {"user_expressions": []}

## Load the catalog

At import time, intake-esm plugin is available in intake’s registry as
`esm_datastore` and can be accessed with `intake.open_esm_datastore()` function.
Use the `intake_esm.tutorial.get_url()` method to access smaller subsetted catalogs for tutorial purposes.

```{code-cell} ipython3
import intake_esm
#url = intake_esm.tutorial.get_url('google_cmip6')
#print(url)
url ="https://raw.githubusercontent.com/NCAR/intake-esm-datastore/master/catalogs/pangeo-cmip6.json"
```

```{code-cell} ipython3
cat = intake.open_esm_datastore(url)
cat
```

+++ {"user_expressions": []}

The summary above tells us that this catalog contains 514818 data assets.
We can get more information on the individual data assets contained in the
catalog by looking at the underlying dataframe created when we load the catalog:

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

## Load datasets using `to_dataset_dict()`

Intake-esm implements convenience utilities for loading the query results into
higher level xarray datasets. The logic for merging/concatenating the query
results into higher level xarray datasets is provided in the input JSON file and
is available under `.aggregation_info` property of the catalog:

```{code-cell} ipython3
cat.esmcat.aggregation_control
```

+++ {"user_expressions": []}

### Get the 8 datasets (this is a lazy operation)

The following command reads in the consolidated metadata, but doesn't grab any actual data.
The data reads will occur later when  you make select operations

```{code-cell} ipython3
dset_dict = single_realization.to_dataset_dict(
        xarray_open_kwargs={"consolidated": True, "decode_times": True, "use_cftime": True}
    )
```

```{code-cell} ipython3
dset_dict.keys()
```

+++ {"user_expressions": []}

## Add the area weights to the cloud cover datsets

To keep track of the variables and weights, it helps to have the keys in two sorted lists

```{code-cell} ipython3
fx_keys = [key for key in dset_dict.keys() if key.find('fx') > -1]
cl_keys = [key for key in dset_dict.keys() if key.find('Amon') > -1]
fx_keys.sort()
cl_keys.sort()
fx_keys, cl_keys
```

+++ {"user_expressions": []}

## reading with checkpoint

+++ {"user_expressions": []}

The cell below shows how to save the datasets to disk, which means fetching all
the data and downloading.  You should have an good idea about how big your files
will be before you do this

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

We can access a particular dataset as follows.  We can choose a simple name like ds, confident
that we can reconstruct the scenario and model from the metadata

```{code-cell} ipython3
ds = dset_dict['ScenarioMIP.NCAR.CESM2.ssp585.Amon.gn']
weights = dset_dict['ScenarioMIP.NCAR.CESM2.ssp585.fx.gn']['areacella']
print(f"{ds.experiment_id=}, {ds.member_id.data[0]=}, {ds.source_id=}")
ds
```

```{code-cell} ipython3
weights
```

+++ {"user_expressions": []}

### squeeze out the unit dimensions

```{code-cell} ipython3
ds = ds.squeeze()
weights = weights.squeeze()
```

+++ {"user_expressions": []}

## Q4: Calculate a zonal average time serie for the Southern ocean

We want to take the zonal mean, weighted by the changing area with latitude, for latitudes
south of -30 degrees

See [https://earth-env-data-science.github.io/lectures/xarray/xarray-part2.html](https://earth-env-data-science.github.io/lectures/xarray/xarray-part2.html) for how to average over the **lon** dimension

+++ {"user_expressions": []}

### Find the weighte mean for the southern ocean

```{code-cell} ipython3
hit = ds.lat < -30
clt_so  = ds['clt'][:,hit,:]
clt_so_weighted = clt_so.weighted(weights)
clt_so_zonal = clt_so.mean(dim=["lon","lat"])
clt_so_zonal
```

+++ {"user_expressions": []}

### Step 3, compare time series between the low and high sensitivity models

https://docs.xarray.dev/en/stable/user-guide/computation.html#rolling-window-operations

```{code-cell} ipython3
:user_expressions: []

from matplotlib import pyplot as plt
rolling = clt_so_zonal.rolling(time=60)
clt_mean = rolling.mean()
fig, ax = plt.subplots(1,1,figsize=(8,8))
clt_mean.plot(ax=ax,label = f"{ds.experiment_id}, {ds.source_id}")
ax.grid(True)
ax.set(title="southern ocean cloud fraction",
    xlabel="time (years)", ylabel = "cloud fraction (percent)");
```

```{code-cell} ipython3
def make_average(ds, weights):
    ds = ds.squeeze()
    weights = weights.squeeze()
    hit = ds.lat < -30
    clt_so  = ds['clt'][:,hit,:]
    clt_so_weighted = clt_so.weighted(weights)
    clt_so_zonal = clt_so.mean(dim=["lon","lat"])
    rolling = clt_so_zonal.rolling(time=60)
    clt_mean = rolling.mean()
    return clt_mean
```

```{code-cell} ipython3
ds =dset_dict['ScenarioMIP.MIROC.MIROC6.ssp585.Amon.gn']
weights = dset_dict['ScenarioMIP.MIROC.MIROC6.ssp585.fx.gn']['areacella']
miroc6_clt_mean = make_average(ds, weights)
miroc6_clt_mean.plot(ax=ax,label = f"{ds.experiment_id}, {ds.source_id}")
fig.legend()
display(fig)
```
