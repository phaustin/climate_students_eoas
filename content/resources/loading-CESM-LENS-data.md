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

+++ {"user_expressions": []}

(resource:intake_esm_LENS)=
# Accessing CESM LENS (and LENS2) data with intake-esm

Preliminary:  You'll need to install `intake-esm`, `xarray-datatree`, and `s3fs` into 

```
mamba install -c conda-forge intake-esm
mamba install -c conda-forge xarray-datatree
mamba install -c conda-forge s3fs
```

This notebook demonstrates how to access Google Cloud CMIP6 data using intake-esm.

Intake-esm is a data cataloging utility built on top of intake, pandas, and
xarray. Intake-esm aims to facilitate:

- the discovery of earth’s climate and weather datasets.
- the ingestion of these datasets into xarray dataset containers.

It's basic usage is shown below. To begin, let's import `intake`:

```{code-cell} ipython3
import intake
import xarray as xr
```

+++ {"user_expressions": []}

## Load the catalog - CESM LENS1

At import time, intake-esm plugin is available in intake’s registry as
`esm_datastore` and can be accessed with `intake.open_esm_datastore()` function.
Use the `intake_esm.tutorial.get_url()` method to access smaller subsetted catalogs for tutorial purposes.

```{code-cell} ipython3
import intake_esm
#url = intake_esm.tutorial.get_url('google_cmip6')
#print(url)
# If you want CESM LENS1:
url ="https://raw.githubusercontent.com/NCAR/cesm-lens-aws/main/intake-catalogs/aws-cesm1-le.json"

# If you want CESM LENS2:
#url = "https://raw.githubusercontent.com/NCAR/cesm2-le-aws/main/intake-catalogs/aws-cesm2-le.json"
```

```{code-cell} ipython3
cat = intake.open_esm_datastore(url)
cat
```

+++ {"user_expressions": []}

The summary above tells us that this catalog contains 442 data assets (for CESM LENS1).
We can get more information on the individual data assets contained in the
catalog by looking at the underlying dataframe created when we load the catalog:

```{code-cell} ipython3
cat.df
```

+++ {"user_expressions": []}

The first data asset listed in the catalog contains:

- the net longwave flux at the surface (variable_id='FLNS'), on daily timescales, from 1920-01-01 to 2005-12-31. 


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
# Let's look at the different variables that are available:
unique['variable']
```

```{code-cell} ipython3
# If you don't know the shorthand for the variable you're interested in, we can look 
# at the "long_name" instead, which is a more descriptive version of the variable name:
unique['long_name']
```

```{code-cell} ipython3
# Let's look at the different experiments that are available:
unique['experiment']
```

+++ {"user_expressions": []}

## Search for specific datasets

The {py:meth}`~intake_esm.core.esm_datastore.search` method allows the user to
perform a query on a catalog using keyword arguments. The keyword argument names
must match column names in the catalog. The search method returns a
subset of the catalog with all the entries that match the provided query.

In the example below, we are are going to search for the following:

- long_name: `sea level pressure` which stands for
- experiments: ['CTRL','20C', 'HIST','RCP85']:
  - 20C: all forcing of the recent past (20th century).
  - RCP85: emission-driven RCP8.5.

```{code-cell} ipython3
cat_subset = cat.search(
    experiment=["CTRL","20C","HIST", "RCP85"],
    long_name="sea level pressure",
)

cat_subset
```

```{code-cell} ipython3
cat_subset.df
```

We can see that sea level pressure uses the variable name 'PSL' ('pressure sea level'). We can also see that this variable is available on 3 different time frequencies: daily, 6-hourly (hourly6) and monthly averages

+++

## Explore the catalog - CESM LENS2

```{code-cell} ipython3
url2 = "https://raw.githubusercontent.com/NCAR/cesm2-le-aws/main/intake-catalogs/aws-cesm2-le.json"
cat2 = intake.open_esm_datastore(url2)
cat2
```

```{code-cell} ipython3
cat2.df
```

```{code-cell} ipython3
unique2 = cat2.unique()
unique2
```

```{code-cell} ipython3
# If you don't know the shorthand for the variable you're interested in, we can look 
# at the "long_name" instead, which is a more descriptive version of the variable name:
unique2['long_name']
```

```{code-cell} ipython3
cat_subset2 = cat2.search(
    experiment=["historical","ssp370"],
    long_name="sea level pressure",
)

cat_subset2
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

To load data assets into xarray datasets, we need to use the
{py:meth}`~intake_esm.core.esm_datastore.to_dataset_dict` method. This method
returns a dictionary of aggregate xarray datasets as the name hints.

```{code-cell} ipython3
# For loading CESM LENS1:
dset_dict = cat_subset.to_dataset_dict(zarr_kwargs={"consolidated": True}, storage_options={"anon": True})
```

```{code-cell} ipython3
[key for key in dset_dict.keys()][:10]
```

+++ {"user_expressions": []}

We can access a particular dataset as follows:

```{code-cell} ipython3
ds = dset_dict["atm.20C.monthly"]
ds
```

We can see that there are 40 different ensemble members (as we expect for CESM LENS1)

+++ {"user_expressions": []}

Let’s create a quick plot for a slice of the data for a subset of the ensemble members

```{code-cell} ipython3
ds.PSL.isel(time=0, member_id=range(1, 40, 4)).plot(col="member_id", col_wrap=3, robust=True)
```

```{code-cell} ipython3
# Let's look at how sea level pressure has changed over time in different ensemble member, 
# for a grid box close to Vancouer 
for iens in range(1,40,4): # only selecting every 4th ensemble member so the plot isn't too messy. 
    ds.PSL.sel(lat = 50, lon=237, method = 'nearest').isel(member_id=iens).plot()
    
# Plot the ensemble mean on top
ds.PSL.sel(lat = 50, lon=237, method = 'nearest').mean(dim='member_id').plot(color='k')
```

```{code-cell} ipython3
# What if we look at the CTRL simulation instead?
ds_ctrl = dset_dict["atm.CTRL.monthly"]
ds_ctrl
```

There are now no separate ensemble members: this is just one long control simulation of 21612/12 = 1801 years! In this case, the forcing (approximating pre-industrial forcing) is constant over time, unlike in the 20th century simulations, where the forcing changes with time. Think about why this means that it's reasonable to run a single 1801-year simulation for the control simulation, but necessary to have multiple ensemble members for the 20th century simulations.

+++

### For CESM LENS2

```{code-cell} ipython3
cat2.esmcat.aggregation_control
```

```{code-cell} ipython3
## For CESM LENS2:
dset_dict2 = cat_subset2.to_dataset_dict(
    xarray_open_kwargs={"consolidated": True, "decode_times": True}, storage_options={"anon": True}
)
```

```{code-cell} ipython3
[key for key in dset_dict2.keys()][:10]
```

```{code-cell} ipython3
ds_cmip6 = dset_dict2["atm.ssp370.monthly.cmip6"]
ds_cmip6
```

```{code-cell} ipython3
# Here we have 50 members. There are 50 other members under the 'smbb' 
# (see https://www.cesm.ucar.edu/community-projects/lens2 ) for more details on these differences, related
# to biomass burning emissions
ds_smbb = dset_dict2["atm.ssp370.monthly.smbb"]
ds_smbb
```

```{code-cell} ipython3
# Unless you think your results will be critically sensitive to the exact biomass burning specification, 
# you can combine these two sets of 50 members to create one 100 member ensemble.
merge_ds= xr.concat([ds_cmip6, ds_smbb], dim='member_id')
merge_ds
```

```{code-cell} ipython3
# information about the start year can be found in the member_id:
# e.g. r10i1181p1f1 is initialized on year 1181
# In the print-out below, you can see that some initialization dates have just one member, e.g. 1181: r10i1181p1f1, 
# whilst others have mutliple members, with micro-perturbations to the initial conditions, e.g. 1281: r1i1281p1f1,
# r2i1281p1f1, r3i1281p1f1 etc...
merge_ds.member_id
```

```{code-cell} ipython3

```
