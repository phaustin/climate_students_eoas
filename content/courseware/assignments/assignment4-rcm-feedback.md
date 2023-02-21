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

(nb:rcm-feedback)=
# Assignment: Feedbacks in the Radiative-Convective Model

This notebook is part of [The Climate Laboratory](https://brian-rose.github.io/ClimateLaboratoryBook) by [Brian E. J. Rose](http://www.atmos.albany.edu/facstaff/brose/index.html), University at Albany.

+++

## Learning goals

Students completing this assignment will gain the following skills and concepts:

- Familiarity with setting up and running a single-column Radiative-Convective Model using climlab
- Familiarity with plotting and interpreting vertical air temperature data on meteorological Skew-T charts
- Use of climlab to perform controlled parameter-sensitivity experiments
- Understanding of the lapse rate feedback concept
- Calculation of radiative forcing and climate feedback parameters

+++

## Question 1

Here you look at the effects of doubling CO$_2$ in the single-column Radiative-Convective model. 

*This exercise just repeats what we did in the lecture notes. You want to ensure that you can reproduce the same results before starting the next question, because you will need these results below.*

Following the lecture notes on climate sensitivity, do the following:

- set up a single-column radiative-convective model with specific humidity taken from the CESM control simulation 
    - done
- Run this control model out to equilibrium 
    - done
- Using a clone of the control model, calculate the stratosphere-adjusted radiative forcing $\Delta R$. 
    - done
- Using another model clone, timestep the model out to equilibrium **with fixed specific humidity**
    - done
- Calculate the no-feedback Equilibrium Climate Sensitivity (ECS)
    - done
- Also calculate the no-feedback climate response parameter $\lambda_0$
    - done

Verify and show that you get the same results as we did in the lecture notes.

```{code-cell} ipython3
import climlab
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
from metpy.plots import SkewT
```

### plotting functions

```{code-cell} ipython3
#  Resuable function to plot the temperature data on a Skew-T chart
def make_skewT():
    fig = plt.figure(figsize=(9, 9))
    skew = SkewT(fig, rotation=30)
    skew.plot(Tglobal.level, Tglobal, color='black', linestyle='-', linewidth=2, label='Observations')
    skew.ax.set_ylim(1050, 10)
    skew.ax.set_xlim(-90, 45)
    # Add the relevant special lines
    skew.plot_dry_adiabats(linewidth=0.5)
    skew.plot_moist_adiabats(linewidth=0.5)
    # skew.plot_mixing_lines()
    skew.ax.legend()
    skew.ax.set_xlabel('Temperature (degC)', fontsize=14)
    skew.ax.set_ylabel('Pressure (hPa)', fontsize=14)
    return skew


#  and a function to add extra profiles to this chart
def add_profile(skew, model, linestyle='-', color=None):
    line = skew.plot(model.lev, model.Tatm - climlab.constants.tempCtoK,
             label=model.name, linewidth=2)[0]
    skew.plot(1000, model.Ts - climlab.constants.tempCtoK, 'o', 
              markersize=8, color=line.get_color())
    skew.ax.legend()
    
```

### global averages of temperature and specific humidity

```{code-cell} ipython3
# air temperature
ncep_url = "http://www.esrl.noaa.gov/psd/thredds/dodsC/Datasets/ncep.reanalysis.derived/"
ncep_air = xr.open_dataset( ncep_url + "pressure/air.mon.1981-2010.ltm.nc", use_cftime=True)
#  Take global, annual average 
coslat = np.cos(np.deg2rad(ncep_air.lat))
weight = coslat / coslat.mean(dim='lat')
Tglobal = (ncep_air.air * weight).mean(dim=('lat','lon','time'))

# Get the water vapor data from CESM output
cesm_data_path = "http://thredds.atmos.albany.edu:8080/thredds/dodsC/CESMA/"
atm_control = xr.open_dataset(
    cesm_data_path + "cpl_1850_f19/concatenated/cpl_1850_f19.cam.h0.nc"
)
# Take global, annual average of the specific humidity
weight_factor = atm_control.gw / atm_control.gw.mean(dim='lat')
Qglobal = (atm_control.Q * weight_factor).mean(dim=('lat','lon','time'))
```

### initial conditions, based on water vapor levels

```{code-cell} ipython3
# model domain
mystate = climlab.column_state(lev=Qglobal.lev, water_depth=2.5)
```

```{code-cell} ipython3
# #  Fixed relative humidity
# h2o = climlab.radiation.ManabeWaterVapor(name='WaterVapor', state=mystate)
```

```{code-cell} ipython3
# create the model: we want to combine radiative and convective
albedo = 0.25
rad = climlab.radiation.RRTMG(name='Radiation',
                              state=mystate, 
                              specific_humidity=Qglobal.values,
                              timestep = climlab.constants.seconds_per_day,
                              albedo = albedo,  # surface albedo, tuned to give reasonable ASR for reference cloud-free model
                             )
#  Now create the convection model
conv = climlab.convection.ConvectiveAdjustment(name='Convection',
                                               state=mystate,
                                               adj_lapse_rate=6.5, # this is the key parameter! We'll discuss below
                                               timestep=rad.timestep,  # same timestep!
                                              )
#  Here is where we build the model by coupling together the two components
rcm = climlab.couple([rad, conv], name='Radiative-Convective Model')
print(rcm)
```

### run radiative-convective control model to equilibrium

```{code-cell} ipython3
# # rcm.integrate_years(0.11)

for n in range(100):
    rcm.step_forward()
while (np.abs(rcm.ASR-rcm.OLR) > 0.01):
    rcm.step_forward()
    
rcm.ASR - rcm.OLR
```

```{code-cell} ipython3
# rcm.subprocess['Radiation (net)'].absorber_vmr['CO2']
```

```{code-cell} ipython3
# Make an exact clone with same temperatures
rcm_2xCO2 = climlab.process_like(rcm)
rcm_2xCO2.name = 'Radiative-Convective Model (2xCO2 initial)'
```

```{code-cell} ipython3
#  Now double it!
rcm_2xCO2.subprocess['Radiation'].absorber_vmr['CO2'] *= 2
rcm_2xCO2.subprocess['Radiation'].absorber_vmr['CO2']
```

```{code-cell} ipython3
# compare with control rcm
rcm_2xCO2.compute_diagnostics()
DeltaR_2xCO2 = (rcm_2xCO2.ASR - rcm_2xCO2.OLR) - (rcm.ASR - rcm.OLR)
DeltaR_2xCO2  # this is the radiative forcing
```

```{code-cell} ipython3
# stratospheric-adjustment model
rcm_2xCO2_strat = climlab.process_like(rcm_2xCO2)
rcm_2xCO2_strat.name = 'Radiative-Convective Model (2xCO2 stratosphere-adjusted)'
# compute the adjustment
for n in range(1000):
    rcm_2xCO2_strat.step_forward()
    # hold tropospheric and surface temperatures fixed
    rcm_2xCO2_strat.Tatm[13:] = rcm.Tatm[13:]
    rcm_2xCO2_strat.Ts[:] = rcm.Ts[:]
rcm_2xCO2_strat.compute_diagnostics()
DeltaR_strat = (rcm_2xCO2_strat.ASR - rcm_2xCO2_strat.OLR) - (rcm.ASR - rcm.OLR)
DeltaR_strat  # this is the radiative forcing
```

```{code-cell} ipython3
DeltaR_strat
```

```{code-cell} ipython3
# strat run to equilibrium
rcm_2xCO2_eq = climlab.process_like(rcm_2xCO2_strat)
rcm_2xCO2_eq.name = 'Radiative-Convective Model (2xCO2 equilibrium)'
rcm_2xCO2_eq.integrate_years(5)
# are we close to equilibrium?
rcm_2xCO2_eq.ASR - rcm_2xCO2_eq.OLR
```

```{code-cell} ipython3
#  actual specific humidity
q = rcm.subprocess['Radiation'].specific_humidity
#  saturation specific humidity (a function of temperature and pressure)
qsat = climlab.utils.thermo.qsat(rcm.Tatm, rcm.lev)
#  Relative humidity
rh = q/qsat
```

```{code-cell} ipython3
rcm_2xCO2_h2o = climlab.process_like(rcm_2xCO2)
rcm_2xCO2_h2o.name = 'Radiative-Convective Model (2xCO2 equilibrium with H2O feedback)'
rcm_2xCO2_h2o.compute_diagnostics()
rcm_2xCO2_h2o.step_forward()
```

```{code-cell} ipython3
# compare with control rcm
DeltaR_wv = (rcm_2xCO2_h2o.ASR - rcm_2xCO2_h2o.OLR) - (rcm.ASR - rcm.OLR)
DeltaR_wv  # this is the radiative forcing
```

```{code-cell} ipython3
for n in range(2000):
    # At every timestep
    # we calculate the new saturation specific humidity for the new temperature
    #  and change the water vapor in the radiation model
    #  so that relative humidity is always the same
    qsat = climlab.utils.thermo.qsat(rcm_2xCO2_h2o.Tatm, rcm_2xCO2_h2o.lev)
    rcm_2xCO2_h2o.subprocess['Radiation'].specific_humidity[:] = rh * qsat
    rcm_2xCO2_h2o.step_forward()
```

```{code-cell} ipython3
# Check for energy balance
rcm_2xCO2_h2o.ASR - rcm_2xCO2_h2o.OLR
```

```{code-cell} ipython3
# Plot all the results
skew = make_skewT()
# for model in rad_models:
add_profile(skew, rcm)
add_profile(skew, rcm_2xCO2)
add_profile(skew, rcm_2xCO2_strat)
add_profile(skew, rcm_2xCO2_eq)
add_profile(skew, rcm_2xCO2_h2o)
skew.ax.set_title('radiative-convective equilibrium', fontsize=18);
```

```{code-cell} ipython3
ECS_no_feedback = rcm_2xCO2_eq.Ts - rcm.Ts
ECS_no_feedback
```

```{code-cell} ipython3
ECS_wv = rcm_2xCO2_h2o.Ts - rcm.Ts
ECS_wv  # include water vapor feedback
```

```{code-cell} ipython3
lambda0 = DeltaR_strat / ECS_no_feedback
lambda0
```

```{code-cell} ipython3

```

## Question 2: combined lapse rate and water vapor feedback in the RCM

### Instructions

A typical, expected feature of global warming is that the **upper troposphere warms more than the surface**. (Later we will see that this does occur in the CESM simulations).

This feature is **not represented in our radiative-convective model**, which is forced to a single prescribed lapse rate due to our convective adjustment.

Here you will suppose that other physical processes modify this lapse rate as the climate warms. 

**Repeat the RCM global warming calculation, but implement two different feedbacks:**

- a water vapor feedback using **fixed relative humidity**
    - done
- a **lapse rate feedback** using this formula:

$$ \Gamma = \Gamma_{ref} - (0.3 \text{ km}) \Delta T_s $$

where $\Gamma_{ref}$ is the critical lapse rate you used in your control model, probably 6.5 K / km, and $\Delta T_s$ is the **current value of the surface warming relative to the control** in units of K. 

So, for example if the model has warmed by 1 K at the surface, then our parameterization says that the critical lapse rate should be 6.5 - 0.3 = 6.2 K / km.

Follow the example in the lecture notes where we implemented the fixed relative humidity. In addition to adjusting the `specific_humidity` at each timestep, you should also change the attribute

```
adj_lapse_rate
```
of the convection process at each timestep.

For example, if you have a model called `mymodel` that contains a `ConvectiveAdjustment` process called `Convection`:
```
mymodel.subprocess['Convection'].adj_lapse_rate = newvalue
```
where `newvalue` is a number in K / km.

### Specific questions:

1. Make a nice skew-T plot that shows three temperature profiles:
    - RCM control
    - RCM, equilibrium after doubling CO$_2$ without feedback
    - RCM, equilibrium after doubling CO$_2$ with combined water vapor and lapse rate feedback
        - done
2. Based on your plot, where in the column do you find the greatest warming?
    - We find the greatest warming in the troposphere up to the tropopause
3. Calculate the ECS of the new version of the model with combined water vapor and lapse rate feedback
    - done
4. Is this sensitivity larger or smaller than the "no feedback" ECS? Is it larger or smaller than the ECS with water vapor feedback alone (which we calculated in the lecture notes)?
    - this ECS sits between the ECS_no_feedback and ECS_wv
5. Calculate the combined feedback parameter for (water vapor plus lapse rate).
    - done
6. Compare this result to the IPCC figure with feedback results from comprehensive models in our lecture notes (labeled "WV+LR"). Do you find a similar number?
    - fairly similar -- both close to positive and close to 1
7. Would you describe the **lapse rate feedback** as positive or negative?
    - I would describe the lapse rate feedback as negative. In this averaged model, we are warming higher in the troposphere, which will result in a larger release of energy to space. The ECS was smaller with both feedbacks, indicating that the lapse rate feedback is working against the (positive) water vapor feedback.

```{code-cell} ipython3
gamma_ref = 6.5  # K / km
slope = 0.3  # 1/km
```

```{code-cell} ipython3
#  actual specific humidity
q = rcm.subprocess['Radiation'].specific_humidity
#  saturation specific humidity (a function of temperature and pressure)
qsat = climlab.utils.thermo.qsat(rcm.Tatm, rcm.lev)
#  Relative humidity
rh = q/qsat
```

```{code-cell} ipython3
rcm_2xCO2_lr_h2o = climlab.process_like(rcm_2xCO2)
rcm_2xCO2_lr_h2o.name = 'Radiative-Convective Model (2xCO2 equilibrium\nwith H2O and lapse rate feedback)'
```

```{code-cell} ipython3
rcm_2xCO2_lr_h2o.compute_diagnostics()
DeltaR_lr_wv = (rcm_2xCO2_lr_h2o.ASR - rcm_2xCO2_lr_h2o.OLR) - (rcm.ASR - rcm.OLR)
DeltaR_lr_wv  # this is the radiative forcing (compute before running to equilibrium!)
```

```{code-cell} ipython3
for n in range(2000):
    # At every timestep
    # we calculate the new saturation specific humidity for the new temperature
    #  and change the water vapor in the radiation model
    #  so that relative humidity is always the same
    qsat = climlab.utils.thermo.qsat(rcm_2xCO2_lr_h2o.Tatm, rcm_2xCO2_h2o.lev)
    # water vapor feedback (fixed relative humidity)
    rcm_2xCO2_lr_h2o.subprocess['Radiation'].specific_humidity[:] = rh * qsat
    # lapse rate feedback
    rcm_2xCO2_lr_h2o.subprocess['Convection'].adj_lapse_rate = gamma_ref - slope * (rcm_2xCO2_lr_h2o.Ts - rcm.Ts)
    rcm_2xCO2_lr_h2o.step_forward()
```

```{code-cell} ipython3
# Plot all the results
skew = make_skewT()
# for model in rad_models:
add_profile(skew, rcm)
add_profile(skew, rcm_2xCO2_eq)
add_profile(skew, rcm_2xCO2_lr_h2o)

skew.ax.set_title('radiative-convective equilibria', fontsize=18);
```

```{code-cell} ipython3
ECS_lr_wv = rcm_2xCO2_lr_h2o.Ts - rcm.Ts
ECS_lr_wv  # include lapse rate and water vapor feedbacks
```

```{code-cell} ipython3
lambda_lr_wv = DeltaR_lr_wv / ECS_lr_wv
lambda_lr_wv
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
