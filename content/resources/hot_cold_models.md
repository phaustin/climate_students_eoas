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
unique['source_id']
```

```{code-cell} ipython3
experiments = unique['experiment_id']
```

```{code-cell} ipython3
experiments.sort()
experiments
```

```{code-cell} ipython3
unique['table_id'][:10]
```

+++ {"user_expressions": []}

## Q1: find a low and a high climate sensitivity model


I'll use a high sensitivity example, substitute your model choice here.

+++ {"user_expressions": []}

## Q2: cloud fraction

Check the variable list at [https://pcmdi.llnl.gov/mips/cmip3/variableList.html#overview](https://pcmdi.llnl.gov/mips/cmip3/variableList.html#overview)

What is the difference between **cl** and **clt**?  What table do they belong to?

+++ {"user_expressions": []}

## Q3 Grab one realization from each of your two models following the cells below

```{code-cell} ipython3
cat_subset = cat.search(
    experiment_id=["historical", "ssp585"],
    table_id="Amon",
    source_id = ["CESM2","MIROC6"],
    variable_id="clt",
    grid_label="gn",
)

cat_subset
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
readit = False
if readit:
    dset_dict = cat_subset.to_dataset_dict(
        xarray_open_kwargs={"consolidated": True, "decode_times": True, "use_cftime": True}
    )
else:
    dset_dict = dict()
```

```{code-cell} ipython3
[key for key in dset_dict.keys()]
```

```{code-cell} ipython3
:tags: []

from pathlib import Path
import xarray as xr
filenames=['cesm2_ssp585.nc','cesm2_historicial.nc','miroc6_ssp585.nc','miroc6_historical.nc']
dataset_names =['ScenarioMIP.NCAR.CESM2.ssp585.Amon.gn',
     'CMIP.NCAR.CESM2.historical.Amon.gn',
     'ScenarioMIP.MIROC.MIROC6.ssp585.Amon.gn',
     'CMIP.MIROC.MIROC6.historical.Amon.gn']
home = Path.home()
out_dir = home /"cmip6_files"
out_dir.mkdir(exist_ok=True,parents=True)
if readit:
    for ds, filename in zip(dset_dict.values(),filenames):
        out_file = out_dir / filename
        print(f"writing {out_file}")
        ds.to_netcdf(out_file)
else:
    for filename,dataset_name in zip(filenames,dataset_names):
        the_file = out_dir / filename
        dset_dict[dataset_name]=xr.open_dataset(the_file)
        
dset_dict
```

```{code-cell} ipython3
:tags: []

for the_ds in dset_dict.values():
    the_ds.close()
```

```{code-cell} ipython3
:tags: []

from pathlib import Path
home = Path.home()
out_dir = home /"cmip6_files"
ds.to_n
```

+++ {"user_expressions": []}

We can access a particular dataset as follows:

```{code-cell} ipython3
ds = dset_dict['ScenarioMIP.NCAR.CESM2.ssp585.Amon.gn']
filename = out_dir / cesm2_ssp585.nc
```

+++ {"user_expressions": []}

## Find the model realizations

```{code-cell} ipython3
ds.coords['member_id']
```

+++ {"user_expressions": []}

### Grab one realization

```{code-cell} ipython3
:user_expressions: []

run1 = ds.sel(member_id = 'r10i1p1f1')
```

+++ {"user_expressions": []}

## Q4: Calculate a zonal average time serie for the Southern ocean

Do this in two steps

### Step 1, zonal mean

See [https://earth-env-data-science.github.io/lectures/xarray/xarray-part2.html](https://earth-env-data-science.github.io/lectures/xarray/xarray-part2.html) for how to average over the **lon** dimension

### Step 2, average over the southern ocean

Use logical indexing to get that part of the zonal mean for the Southern Ocean, i.e.
seletct latitudes south of -30.  Find the average over latitude for that subsection, which should
give you a 1 dimensional time series

### Step 3, compare time series between the low and high sensitivity models
