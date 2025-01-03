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

(nb:aclimchange)=
# Assignment: Climate change in the CESM simulations

This notebook is part of [The Climate Laboratory](https://brian-rose.github.io/ClimateLaboratoryBook) by [Brian E. J. Rose](http://www.atmos.albany.edu/facstaff/brose/index.html), University at Albany.

+++

## Part 1

Following the examples in the [lecture notes](https://brian-rose.github.io/ClimateLaboratoryBook/courseware/transient-cesm.html), open the four CESM simulations (fully coupled and slab ocean versions). 

Calculate timeseries of **global mean ASR and OLR** and store each of these as a new variable. *Recall that ASR is called `FSNT` in the CESM output, and OLR is called `FLNT`.*
- done-- stored in a dictionary for each flux and each simulation

Plot a timeseries of **(ASR - OLR), the net downward energy flux at the top of the model**, along with a **12 month rolling mean**, analogous to the plot of global mean surface air temperature in the lecture notes.
- done

*Note that the rolling mean is important here because, just like with surface air temperature, there is a large seasonal cycle which makes it harder to see evidence of the climate change signal we wish to focus on.*

```{code-cell} ipython3
%matplotlib inline
import numpy as np
import matplotlib.pyplot as plt
import xarray as xr

import warnings
warnings.filterwarnings("ignore")  # suppresses some runtime warnings
```

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
atm = {}
for name in casenames:
    path = casepaths[name] + casenames[name] + '.cam.h0.nc'
    print('Attempting to open the dataset ', path)
    atm[name] = xr.open_dataset(path, decode_times=False)
```

```{code-cell} ipython3
# note: times are days since beginning, stepped by month lengths
atm['cpl_control'].FSNT

# are weights the same for the different sims? yes
# todo: could use itertools.product for fun
for name in casenames:
    for compare_name in casenames:
#         print(atm[name].gw.all() == atm[compare_name].gw.all())
        pass
        
gw = atm['cpl_control'].gw
days_per_year = 365
# print(gw)
```

```{code-cell} ipython3
# define a function to compute the global mean using correctly spatial weights
def global_mean(field, weight=gw):
    return (field * weight).mean(dim=('lat', 'lon')) / weight.mean(dim='lat')
```

```{code-cell} ipython3
# global_mean(atm['cpl_control'].FSNT)
```

```{code-cell} ipython3
# global_mean(atm['cpl_control']['FLNT'])
```

```{code-cell} ipython3
# make time-series of global mean FSNT and FLNT
fluxes_global = {}
```

```{code-cell} ipython3
model_types = ['cpl', 'som']  # coupled or slab ocean models
radiative_fluxes = {'FSNT': 'ASR', 'FLNT': 'OLR'}

for flux in radiative_fluxes.keys():  # iterate over FSNT, FLNT
    print(radiative_fluxes[flux])
    fluxes_global[radiative_fluxes[flux]] = {}  # remap to ASR and OLR
    for name in casenames:
        # compute global mean for each case:
        fluxes_global[radiative_fluxes[flux]][name] = global_mean(atm[name][flux])
 
```

```{code-cell} ipython3
print(fluxes_global.keys())
print(fluxes_global['ASR'].keys())
print(f"ASR array:\n\t{fluxes_global['ASR']['cpl_control']}\n")  # show the nested structure
print(f"OLR array:\n\t{fluxes_global['OLR']['cpl_control']}\n")
```

```{code-cell} ipython3
fig, axes = plt.subplots(2,2,figsize=(10,8), dpi=150)
for ii, flux in enumerate(radiative_fluxes):
    for name in casenames:
#         print(f"currently iterating over {flux},\n\tcase {name}")
        if 'cpl' in name:
            ax = axes[0][ii]
            ax.set_title(f'Fully coupled ocean {radiative_fluxes[flux]}')
        else:
            ax = axes[1][ii]
            ax.set_title(f'Slab ocean {radiative_fluxes[flux]}')
        field = fluxes_global[radiative_fluxes[flux]][name]
        field_running = field.rolling(time=12, center=True).mean()
        line = ax.plot(field.time / days_per_year, 
                       field, 
                       label=name,
                       linewidth=0.75,
                       )
        ax.plot(field_running.time / days_per_year, 
                field_running, 
                color=line[0].get_color(),
                linewidth=2,
               )
        
    counter = 0
    for ax in axes:
        ax[ii].legend();
        if counter == 1:
            ax[ii].set_xlabel('Years')
        ax[ii].set_ylabel(f'{flux} (W/m2)')
        ax[ii].grid();
        ax[ii].set_xlim(0,100)
        ax[ii].set_ylim(224.0,242.0)  # make this a function of the range, make it smarter
        counter+=1
# plt.tight_layout()  # not working with suptitle
fig.suptitle('Global mean ASR and OLR in CESM simulations', fontsize=16);
```

```{code-cell} ipython3
fig, axes = plt.subplots(2,1,figsize=(10,8), dpi=150)
for name in casenames:
    if 'cpl' in name:
        ax = axes[0]
        ax.set_title('Fully coupled ocean')
    else:
        ax = axes[1]
        ax.set_title('Slab ocean')
    field = np.subtract(fluxes_global['ASR'][name], fluxes_global['OLR'][name])  # ASR - OLR
#     print(field)
    field_running = field.rolling(time=12, center=True).mean()
    line = ax.plot(field.time / days_per_year, 
                   field, 
                   label=name,
                   linewidth=0.75,
                   )
    ax.plot(field_running.time / days_per_year, 
            field_running, 
            color=line[0].get_color(),
            linewidth=2,
           )
counter = 0
for ax in axes:
    ax.legend();
    if counter == 1:
        ax.set_xlabel('Years')
    ax.set_ylabel('(ASR - OLR) (W/m2)')
    ax.grid();
    ax.set_xlim(0,100)
    counter+=1
# plt.tight_layout()  # not working with suptitle
fig.suptitle('Global mean net downward energy flux\nat the top of the model in CESM simulations', fontsize=16);
```

## Part 2

Calculate and show the **time-average ASR** and **time-average OLR** over the final 10 or 20 years of each simulation. Following the lecture notes, use the 20-year slice for the fully coupled simulations, and the 10-year slice for the slab ocean simulations.

```{code-cell} ipython3
# todo: time average, preserving lat-long
print("ASR time averages")
# extract the last 10 years from the slab ocean control simulation
# and the last 20 years from the coupled control
nyears_slab = 10
nyears_cpl = 20
clim_slice_slab = slice(-(nyears_slab*12),None)
clim_slice_cpl = slice(-(nyears_cpl*12),None)
# extract the last 10 years from the slab ocean control simulation
asr0_slab = fluxes_global['ASR']['som_control'].isel(time=clim_slice_slab).mean(dim='time')
print(f"slab model control: {asr0_slab}")
# extract the last 10 years from the slab 2xCO2 simulation
asr2x_slab = fluxes_global['ASR']['som_2xCO2'].isel(time=clim_slice_slab).mean(dim='time')
print(f"slab model doulbing: {asr2x_slab}")
# and the last 20 years from the coupled control
asr0_cpl = fluxes_global['ASR']['cpl_control'].isel(time=clim_slice_cpl).mean(dim='time')
print(f"coupled model control: {asr0_cpl}")
# extract the last 20 years from the coupled CO2 ramp simulation
asr2x_cpl = fluxes_global['ASR']['cpl_CO2ramp'].isel(time=clim_slice_cpl).mean(dim='time')
print(f"coupled model doubling: {asr2x_cpl}")
```

```{code-cell} ipython3
print("OLR time averages")
# extract the last 10 years from the slab ocean control simulation
olr0_slab = fluxes_global['OLR']['som_control'].isel(time=clim_slice_slab).mean(dim='time')
print(f"slab model control: {olr0_slab}")
# extract the last 10 years from the slab 2xCO2 simulation
olr2x_slab = fluxes_global['OLR']['som_2xCO2'].isel(time=clim_slice_slab).mean(dim='time')
print(f"slab model doulbing: {olr2x_slab}")
# and the last 20 years from the coupled control
olr0_cpl = fluxes_global['OLR']['cpl_control'].isel(time=clim_slice_cpl).mean(dim='time')
print(f"coupled model control: {olr0_cpl}")
# extract the last 20 years from the coupled CO2 ramp simulation
olr2x_cpl = fluxes_global['OLR']['cpl_CO2ramp'].isel(time=clim_slice_cpl).mean(dim='time')
print(f"coupled model doubling: {olr2x_cpl}")
```

```{code-cell} ipython3
(asr2x_slab - olr2x_slab) - (asr0_slab - olr0_slab)
```

```{code-cell} ipython3
(asr2x_cpl - olr2x_cpl) - (asr0_cpl - olr0_cpl)
```

## Part 3

Based on your plots and numerical results from Parts 1 and 2, answer these questions:

1. Are the two control simulations (fully coupled and slab ocean) near energy balance?
- The slab ocean is near energy balance, as the radiative balance of ASR to OLR is close to zero. However, the fully coupled model is near an average of 1.05 W/m2 of forcing over the last 20 years. This indicates that this model is not in energy balance.
2. In the fully coupled CO2 ramp simulation, does the energy imbalance (ASR-OLR) increase or decrease with time? What is the imbalance at the end of the 80 year simulation?
- Upon inspection, the energy imbalance is increasing with time. At the end of 80 years of simulation, the fully coupled CO2 ramp energy balance is diverting from equilibrium, with a magnitude around 1.33 W/m2.
3. Answer the same questions for the slab ocean abrupt 2xCO2 simulation.
- Again upon inspection of the curves, the energy imbalance for the slab ocean model decreases with time toward zero. The imbalance at the end of the simulation is -0.11 W/m2.
4. Explain in words why the timeseries of ASR-OLR look very different in the fully coupled simulation (1%/year CO2 ramp) versus the slab ocean simulation (abrupt 2xCO2). *Think about both the different radiative forcings and the different ocean heat capacities.*
- These time series look very different because a coupled atmosphere-ocean has less average energetic inertia compared to the slab ocean model, which assumes the ocean layer is well-mixed. The instantaneous mixing assumption of the slab model and the ocean's enormous heat capacity imply that extra energy in the earth fluid-envelope can be diffused into the ocean quickly, rather than left in the atmosphere to heat the earth's surface. This effect is punctuated by the abrupt doubling of CO2, as we see in the time series the decay toward radiative equilibrium within 30 years of the slab model simulation.

```{code-cell} ipython3
(fluxes_global['ASR']['som_2xCO2'] - fluxes_global['OLR']['som_2xCO2']).rolling(time=12, center=True).mean()[-6]
```

```{code-cell} ipython3
# compute the annual average imbalance at the end of the coupled simulation
(fluxes_global['ASR']['cpl_CO2ramp'] - fluxes_global['OLR']['cpl_CO2ramp']).rolling(time=12, center=True).mean()[-6]
```

## Part 4

Does the global average ASR **increase** or **decrease** because of CO2-driven warming in the CESM? 
- We can see from the plot in part one that the global average ASR is increasing with CO2-driven warming.

Would you describe this as a **positive** or **negative** feedback?
- I find this counterintuitive at first, as the CO2 forcing would be a reduction in OLR to produce energy accumulation. However, we see from these simulations that the OLR is relatively unaffected, and the ASR is instead the source of accumulation of energy, upon enhancement of ASR due to feedbacks. Since this feedback is resulting in an increasing ASR, the gain is greater than one and the feedback is positive.

+++

## Part 5

In the previous question you looked at the global average change in ASR. Now I want you to look at how different parts of the world contribute to this change.

**Make a map** of the **change in ASR** due to the CO2 forcing. Use the average over the last 20 years of the coupled CO2 ramp simulation, comparing against the average over the last 20 years of the control simulation.

```{code-cell} ipython3
# this averages over the last 20 years
global_asr_CO2ramp = atm['cpl_CO2ramp'].FSNT.isel(time=clim_slice_cpl).mean(dim='time')
global_asr_control = atm['cpl_control'].FSNT.isel(time=clim_slice_cpl).mean(dim='time')
delta_asr_cpl = global_asr_CO2ramp - global_asr_control
```

```{code-cell} ipython3
# The map projection capabilities come from the cartopy package. There are many possible projections
import cartopy.crs as ccrs
from cartopy.util import add_cyclic_point
```

```{code-cell} ipython3
def make_map(field, title=""):
    '''input field should be a 2D xarray.DataArray on a lat/lon grid.
        Make a filled contour plot of the field, and a line plot of the zonal mean
    '''
    fig = plt.figure(figsize=(14,6), dpi=150)
    nrows = 10; ncols = 3
    mapax = plt.subplot2grid((nrows,ncols), (0,0), colspan=ncols-1, rowspan=nrows-1, projection=ccrs.Robinson())
    barax = plt.subplot2grid((nrows,ncols), (nrows-1,0), colspan=ncols-1)
    plotax = plt.subplot2grid((nrows,ncols), (0,ncols-1), rowspan=nrows-1)
    # add cyclic point so cartopy doesn't show a white strip at zero longitude
    wrap_data, wrap_lon = add_cyclic_point(field.values, coord=field.lon, axis=field.dims.index('lon'))
    cx = mapax.contourf(wrap_lon, field.lat, wrap_data, transform=ccrs.PlateCarree())
    mapax.set_global(); mapax.coastlines();
    plt.colorbar(cx, cax=barax, orientation='horizontal')
    plotax.plot(field.mean(dim='lon'), field.lat)
    plotax.set_ylabel('Latitude')
    plotax.grid()
    fig.suptitle(title, fontsize=16)
    return fig, (mapax, plotax, barax), cx
```

```{code-cell} ipython3
fig, axes, cx = make_map(delta_asr_cpl,
                        title='Absorbed Shortwave Radiation Anomaly (coupled transient) (W/m2)')
```

## Part 6

Repeat part 5, but this time instead of the change in ASR, look at the just change in the **clear-sky** component of ASR. You can find this in the output field called `FSNTC`.

*The `FSNTC` field shows shortwave absorption in the absence of clouds, so the **change** in `FSNTC` shows how absorption and reflection of shortwave are affected by processes other than clouds.*

```{code-cell} ipython3
global_asr_clear_CO2ramp = atm['cpl_CO2ramp'].FSNTC.isel(time=clim_slice_cpl).mean(dim='time')
global_asr_clear_control = atm['cpl_control'].FSNTC.isel(time=clim_slice_cpl).mean(dim='time')
delta_asr_clear_cpl = global_asr_clear_CO2ramp - global_asr_clear_control
```

```{code-cell} ipython3
fig, axes, cx = make_map(delta_asr_clear_cpl,
                        title='Absorbed Shortwave Radiation Anomaly (coupled transient) (W/m2)')
```

## Part 7

Discussion:

- Do your two maps (change in ASR, change in clear-sky ASR) look the same? 
    - My maps have similarities and differences. The similarity at the poles, which is enhanced in the clear-sky simulation, suggests that reductions in surface albedo related to ice-albedo feedback have increased absorption with CO2 forcing. Both maps show negative anomalies in the oceans. The relatively high absorption at high latitudes in the clear-sky case points to how the angle of incidence controls absorption, with clouds contributing a dampening effect. The maps differ most between the mid-latitudes and the equator, where the clear-sky map shows small absorption anomalies due to the direct view of the ocean across time. Some areas of negative anomalies at the margins of continents in the clear-sky case are switched to moderate absorption anomalies in the model with clouds.
- Offer some ideas about why the clear-sky map looks the way it does.
    - The clear-sky map has high ASR anomalies mostly over bodies of water near the poles, perhaps due to a reduction in sea ice (lower albedo) related to surface warming. The clear-sky anomaly is close to zero between the mid-latitudes because of the large water fraction throughout that band. 
- Comment on anything interesting, unusual or surprising you found in the maps.
    - I am intrigued by the negative anomaly at the south pole, as well as those near the equator in the eastern Pacific, central America, the western Sahara, and the Namibian desert. The negative anomaly is present in both maps for the eastern Pacific and some of central America, but what role have clouds played to reduce the absorption in the first pair of models?

+++

____________

## Credits

This notebook is part of [The Climate Laboratory](https://brian-rose.github.io/ClimateLaboratoryBook), an open-source textbook developed and maintained by [Brian E. J. Rose](http://www.atmos.albany.edu/facstaff/brose/index.html), University at Albany.

It is licensed for free and open consumption under the
[Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/) license.

Development of these notes and the [climlab software](https://github.com/brian-rose/climlab) is partially supported by the National Science Foundation under award AGS-1455071 to Brian Rose. Any opinions, findings, conclusions or recommendations expressed here are mine and do not necessarily reflect the views of the National Science Foundation.
____________

```{code-cell} ipython3

```
