---
jupytext:
  formats: md:myst,ipynb
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

# Assignment: Climate change in the CESM simulations

This notebook is part of [The Climate Laboratory](https://brian-rose.github.io/ClimateLaboratoryBook) by [Brian E. J. Rose](http://www.atmos.albany.edu/facstaff/brose/index.html), University at Albany.

+++

Download assignment5-cesm-climate-change.md from the [google drive](https://drive.google.com/drive/folders/1ktPMS5IaZYox06MYTd9CP5pKle7Coocs?usp=sharing)

```{code-cell} ipython3
import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
from pathlib import Path

import warnings
warnings.filterwarnings("ignore")  # suppresses some runtime warnings
```

## Part 1

Following the examples in the [lecture notes](https://brian-rose.github.io/ClimateLaboratoryBook/courseware/transient-cesm.html), open the four CESM simulations (fully coupled and slab ocean versions). 

Calculate timeseries of **global mean ASR and OLR** and store each of these as a new variable. *Recall that ASR is called `FSNT` in the CESM output, and OLR is called `FLNT`.*

Plot a timeseries of **(ASR - OLR), the net downward energy flux at the top of the model**, along with a **12 month rolling mean**, analogous to the plot of global mean surface air temperature in the lecture notes.  

*Note that the rolling mean is important here because, just like with surface air temperature, there is a large seasonal cycle which makes it harder to see evidence of the climate change signal we wish to focus on.*

```{code-cell} ipython3
casenames = {'cpl_control': 'cpl_1850_f19',
             'cpl_CO2ramp': 'cpl_CO2ramp_f19',
             'som_control': 'som_1850_f19',
             'som_2xCO2':   'som_1850_2xCO2',
            }
# The path to the THREDDS server, should work from anywhere
basepath = 'http://thredds.atmos.albany.edu:8080/thredds/dodsC/CESMA/'
# For better performance if you can access the roselab_rit filesystem (e.g. from JupyterHub)
# basepath = '/roselab_rit/cesm_archive/'
casepaths = {}
for name in casenames:
    casepaths[name] = basepath + casenames[name] + '/concatenated/'
```

```{code-cell} ipython3
# make a dictionary of all the CAM atmosphere output
local_folder = Path.home() / "repos/e440/assign5"
local_folder.mkdir(parents=True, exist_ok = True)
atm = {}
for name in casenames:
    filename = casenames[name] + '.cam.h0.nc'
    path = casepaths[name] + filename
    print('Attempting to open the dataset ', path)
    atm[name] = xr.open_dataset(path, decode_times=False)
```

## Part 2

Calculate and show the **time-average ASR** and **time-average OLR** over the final 10 or 20 years of each simulation. Following the lecture notes, use the 20-year slice for the fully coupled simulations, and the 10-year slice for the slab ocean simulations.

```{code-cell} ipython3

```

## Part 3

Based on your plots and numerical results from Parts 1 and 2, answer these questions:

1. Are the two control simulations (fully coupled and slab ocean) near energy balance?
2. In the fully coupled CO2 ramp simulation, does the energy imbalance (ASR-OLR) increase or decrease with time? What is the imbalance at the end of the 80 year simulation?
3. Answer the same questions for the slab ocean abrupt 2xCO2 simulation.
4. Explain in words why the timeseries of ASR-OLR look very different in the fully coupled simulation (1%/year CO2 ramp) versus the slab ocean simulation (abrupt 2xCO2). *Think about both the different radiative forcings and the different ocean heat capacities.*

```{code-cell} ipython3

```

## Part 4

Does the global average ASR **increase** or **decrease** because of CO2-driven warming in the CESM? 

Would you describe this as a **positive** or **negative** feedback?

```{code-cell} ipython3

```

## Part 5

In the previous question you looked at the global average change in ASR. Now I want you to look at how different parts of the world contribute to this change.

**Make a map** of the **change in ASR** due to the CO2 forcing. Use the average over the last 20 years of the coupled CO2 ramp simulation, comparing against the average over the last 20 years of the control simulation.

```{code-cell} ipython3

```

## Part 6

Repeat part 5, but this time instead of the change in ASR, look at the just change in the **clear-sky** component of ASR. You can find this in the output field called `FSNTC`.

*The `FSNTC` field shows shortwave absorption in the absence of clouds, so the **change** in `FSNTC` shows how absorption and reflection of shortwave are affected by processes other than clouds.*

```{code-cell} ipython3

```

## Part 7

Discussion:

- Do your two maps (change in ASR, change in clear-sky ASR) look the same? 
- Offer some ideas about why the clear-sky map looks the way it does.
- Comment on anything interesting, unusual or surprising you found in the maps.

```{code-cell} ipython3

```

____________

## Credits

This notebook is part of [The Climate Laboratory](https://brian-rose.github.io/ClimateLaboratoryBook), an open-source textbook developed and maintained by [Brian E. J. Rose](http://www.atmos.albany.edu/facstaff/brose/index.html), University at Albany.

It is licensed for free and open consumption under the
[Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/) license.

Development of these notes and the [climlab software](https://github.com/brian-rose/climlab) is partially supported by the National Science Foundation under award AGS-1455071 to Brian Rose. Any opinions, findings, conclusions or recommendations expressed here are mine and do not necessarily reflect the views of the National Science Foundation.
____________

```{code-cell} ipython3

```
