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

# Feedback notation for worksheet 4

+++

## Rose lab 14

### Radiation balance at the top of the atmosphere

$\Delta R + f \lambda_0 \Delta T_0$

* where $\Delta R$ is the radiative forcing. units: $W\,m^{-2}$

* $\lambda_0$ is the Planck feedback. units: $W\,m^{-2}\,K^{-1}$

* $\Delta T_0$ is the initial response. units: $K$

  $\Delta R = \Delta T_0/\lambda_0$
  
* $f_i$ is the feedback factor for process $i$. units: unitless

  $f = \sum f_i$
  
* climate feedback parameter: $\lambda_i = \lambda_0 f_i$. units: $W\,m^{-2}\,K^{-1}$
  
### Equilibrium Climate Sensitivity

* $g = \frac{1}{1-f}$ = system gain. units: unitless

* $ECS = \Delta T$, units: K,  for the case where $\Delta R$ is given for doubled $CO_2$.  

  * i.e. $ECS = g \Delta R_{2 x CO2}$ units: degrees/doubling

  
  
## Hartmann Chapter 10

### Radiation balance at the top of the atmosphere

$\Delta Q + \Delta R_{TOA}$

* where $\Delta Q$. units:$W\,m^{-2}$  is the radiative forcing and $\Delta R_{TOA}$ is the climate response

* Planck feedback factor $\left(\lambda_{\mathrm{R}}\right)_{\mathrm{BB}}^{-1}=\left(\frac{\partial\left(\sigma T_{\mathrm{e}}^4\right)}{\partial T_{\mathrm{s}}}\right)$.  units: $W\,m^{-2}$

### Equilibrium Climate Sensitivity

* $\lambda_R = \Delta T_s / \Delta Q$  units: $K \, (W\,m^{-2})^{-1}$

## Roe, 2009

### Radiation balance at the top of the atmosphere

$\Delta R_f+\Delta R_\alpha$

* where $\Delta R_f$ is the radiative forcing. units: $W\,m^{-2}$ 

* Planck feedback factor: $c_{pl}$= 1/$\lambda_0=\left ( \frac{\Delta T}{\Delta R_f} \right )^{-1} = -\frac{d F}{d T}= - 4 \sigma T^3$  units: $W\,m^{-2}\,K^{-1}$

* Gain -- $G=\frac{\Delta T}{\Delta T_0}=\frac{1}{1-f}=\frac{\Delta T}{\Delta T_0}$

* feedback factors:  $f_1 =\lambda_0 c_1$, $f = \lambda_0 \sum_i c_i$

* feedback factors as Taylor series terms: $\left.f_i \approx \lambda_0\left\{\frac{\Delta R}{\Delta \alpha_i}\right)_{\alpha_{j, j \neq i}} \frac{\Delta \alpha_i}{\Delta T}\right\}$


### Equilibrium climate sensitivity

* equilibrium climate response:  $\Delta T=\frac{\lambda_0 \Delta R_f}{1-\lambda_0 \sum_i c_i}$


* equilibrium climate sensitivity: $ \frac{\lambda_0 }{1-\lambda_0 \sum_i c_i} $  units: $K \, (W\,m^{-2})^{-1}$

## Sherwood et al. 2020

### Radiation balance at the top of the atmosphere

$\Delta N=\Delta F+\Delta \mathrm{R}+V$

Where $\Delta F$ units: $W\,m^{-2}$ is the radiative forcing, $\Delta R$ is the response and 
$V$ is variability from unforced variations.

* Feedback factor:  $\lambda = \frac{\Delta R}{\Delta T}$ units: $W\,m^{-2}\,K^{-1}$

* Feedback factors as Taylor series terms:

* $ \lambda=\sum_i \lambda_i=\sum_i \frac{\partial N}{\partial x_i} \frac{d x_i}{\partial T}=\lambda_{\text {Planck }}+\lambda_{\text {water vapor }}+\lambda_{\text {lapse rate }}+\lambda_{\text {surface }}+\lambda_{\text {clouds }}+\lambda_{\text {other }}$


### Equilibrium climate sensitivity

* $\Delta \mathrm{T}=-\Delta \mathrm{F} / \lambda$

* $S=-\frac{\Delta F_{2 \times \mathrm{CO} 2}}{\lambda}$
