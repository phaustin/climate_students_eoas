# Courseware vs. ClimateLaboratoryBook upstream: comparison report

*Session date: 2026-11-23*

## Request

> content/courseware holds an older version of the course files in
> `~/repos/ClimateLaboratoryBook/courseware`. For each markdown file in this
> project, find its newer version in `~/repos/ClimateLaboratoryBook/courseware`
> and report on changes, if any.

## Method

- Local files were mapped to upstream names by stripping the `labN_` / `labN_M_` prefix and turning `assignmentN-` into `assignment-` (for example `week3/lab7_elementary-greenhouse.md` → `elementary-greenhouse.md`). Checkpoint and editor lock files were skipped.
- Local files are a mix of jupytext `markdown` and `myst` formats, while all upstream files are `myst`. Raw `diff` output was therefore mostly format noise. Both sides were read with jupytext (1.19.6, from the upstream pixi env) and compared cell by cell, ignoring blank lines and trailing whitespace.
- These changes appear everywhere and were ignored: the jupytext version, Brian Rose's homepage URL, the climlab GitHub URL (`brian-rose/climlab` → `climlab/climlab`), absolute book URLs → short links between pages, `____` rule lines and `(nb:…)=` labels.
- The comparison script and per-file diffs are in `courseware_upstream_comparison/` (`cmp.py`, `diffs/`). To regenerate them, run:
  `~/repos/ClimateLaboratoryBook/.pixi/envs/default/bin/python -I courseware_upstream_comparison/cmp.py courseware_upstream_comparison/diffs`

### Size of each normalized diff (lines added/removed in upstream)

| Local file | Upstream file | Diff |
|---|---|---|
| assignments/assignment-rcm-feedback.md | assignment-rcm-feedback.md | +25 −13 |
| assignments/assignment1-zero-dim-ebm.md | assignment-zero-dim-ebm.md | +45 −28 |
| assignments/assignment2-cesm-control-hints.md | assignment-cesm-control-hints.md | +3 −1 |
| assignments/assignment2-cesm-control.md | assignment-cesm-control.md | +4 −5 |
| assignments/assignment3-simple-clouds.md | assignment-simple-clouds.md | +5 −4 |
| assignments/assignment4-rcm-feedback.md | assignment-rcm-feedback.md | +24 −13 |
| assignments/assignment5-cesm-climate-change.md | assignment-cesm-climate-change.md | +0 −226 |
| assignments/assignment6-insolation-orbit.md | assignment-insolation-orbit.md | +1 −1 |
| courseware.md | courseware.md | identical |
| week1/lab1_models-budgets-fun.md | models-budgets-fun.md | +42 −36 |
| week2/lab2_1_analytical-efolding.md | analytical-efolding.md | +12 −3 |
| week2/lab2_zero-dim-ebm.md | zero-dim-ebm.md | +64 −27 |
| week2/lab3_climate-system-models.md | climate-system-models.md | +49 −48 |
| week3/lab4_introducing-cesm.md | introducing-cesm.md | +24 −19 |
| week3/lab5_climlab-intro.md | climlab-intro.md | +33 −15 |
| week3/lab6_radiation.md | radiation.md | +12 −15 |
| week3/lab7_elementary-greenhouse.md | elementary-greenhouse.md | +91 −64 |
| week3/lab8_sympy-greenhouse.md | sympy-greenhouse.md | +3 −2 |
| week4/lab9_grey-radiation-climlab.md | grey-radiation-climlab.md | +26 −20 |
| week4/lab10_radiative-transfer.md | radiative-transfer.md | +19 −5 |
| week4/lab11_spectral-bands.md | spectral-bands.md | +31 −32 |
| week5/lab12_radeq.md | radeq.md | +14 −10 |
| week5/lab13_rce.md | rce.md | +8 −7 |
| week5/lab14_sensitivity-feedback.md | sensitivity-feedback.md | +77 −48 |
| week5/lab14_2_advanced-sensitivity-feedback.md | advanced-sensitivity-feedback.md | +15 −24 |
| week5/lab15_transient-cesm.md | transient-cesm.md | +31 −24 |
| week5/lab16_transient-toy.md | transient-toy.md | +24 −20 |
| week6/lab17_clouds.md | clouds.md | +16 −23 |
| week6/lab18_insolation.md | insolation.md | +79 −16 |
| week6/lab19_orbital.md | orbital.md | +77 −86 |
| week6/lab20_heat-transport.md | heat-transport.md | +13 −11 |
| week6/lab20_2_advanced-heat-transport.md | advanced-heat-transport.md | +29 −26 |
| week7/lab21_one-dim-ebm.md | one-dim-ebm.md | +10 −11 |
| week7/lab22_seasonal-cycle.md | seasonal-cycle.md | +16 −10 |
| week7/lab24_numerical-diffusion.md | numerical-diffusion.md | +4 −2 |
| week8/lab25_albedo-snowball.md | albedo-snowball.md | +14 −21 |
| week8/lab25_2_advanced-albedo-feedback.md | advanced-albedo-feedback.md | +20 −13 |
| week8/lab25_3_advanced-snowball-earth.md | advanced-snowball-earth.md | +26 −21 |
| week9/lab27_surface-energy-balance.md | surface-energy-balance.md | +104 −59 |
| week9/lab28_land-ocean-contrast.md | land-ocean-contrast.md | +48 −26 |
| week9/lab29_water-water-everywhere.md | water-water-everywhere.md | +12 −14 |

## Changes made in nearly every file

- **Figures:** `{figure}` blocks and `<img>` tags became plain Markdown images pointing at `../images/`.
- **Citations:** written-out references became `{cite:p}` / `{cite:t}` keys (Hartmann, Pierrehumbert, AR5_Ch9, Byrne & O'Gorman, etc.).
- **Callouts:** "Python fact N" headings and `<div class="alert">` boxes became `:::{tip}`, `:::{note}`, `:::{warning}` and `:::{important}` boxes.
- **Equations:** bare `\begin{align}` blocks are now wrapped in `$$ … $$`.
- **Code:** `print(x)` became a bare `x` so the object displays as rich output. Most notebooks gained a commented-out `/roselab_rit/cesm_archive/` path for JupyterHub. CO2 is written CO$_2$ in text, and degree signs replace `$^\circ$`.
- **Library updates:**
  - `use_cftime=True` → `xr.coders.CFDatetimeCoder`
  - `cumtrapz` → `cumulative_trapezoid`
  - `np.math.pi` → `np.pi`
  - `insolation=sun.insolation` → `irradiance_factor=sun.irradiance_factor`
  - `.weighted()` for averaging
  - `[0]` or `.squeeze()` on climlab outputs
  - `newrad + conv` → `climlab.couple(...)`
  - `n is 0` → `n == 0`
- **Link targets:** links to sections now use lower-case anchors (`#the-observed-global-energy-budget`), and old links to `LectureNN -- ….ipynb` files are fixed.

## Content changes by file

### Assignments

- **assignment1-zero-dim-ebm:** split into Parts (a)/(b)/(c) with hints and "Your answer goes here" cells. Adds JupyterHub kernel instructions and a link to the timestepping section of the notes.
- **assignment2-cesm-control:** the two energy-balance questions are merged into one, and the NCEP file is opened with `decode_times=False`. In the hints file, a printed label is corrected from "Downwelling" to "Upwelling" longwave.
- **assignment3-simple-clouds:** adds a `:::{hint}` for Question 2. Upstream **removed Question 6**, which the local copy still has.
- **assignment-rcm-feedback and assignment4-rcm-feedback:** both match the same upstream file.
  - A new Question 2 has students reproduce the water vapour feedback, so the old Question 2 is now Question 3.
  - "Stratosphere-adjusted" forcing becomes "atmosphere-adjusted".
  - The lapse-rate formula has corrected units: Γ = 6.5 K km⁻¹ − (0.3 km⁻¹)ΔTs.
- **assignment5-cesm-climate-change:** ⚠️ the local copy contains a **completed student solution**, about 220 lines of code and written answers. Upstream is just the blank questions.
- **assignment6-insolation-orbit:** one link anchor fixed.

### Weeks 1–3

- **lab1 models-budgets-fun:** adds a glossary entry for OLR and puts the Python facts in tip boxes. Upstream removed the pre-written `OLR(T)` function cell, so students write it themselves.
- **lab2_1 analytical-efolding:** the code cells now define their own constants (τ, σ, C) instead of relying on earlier notebooks. A note on the sign of the Planck feedback (−λ₀) is added.
- **lab2 zero-dim-ebm:** adds glossary entries for Insolation and ASR. A new section shows working `ASR()` / `OLR()` functions for students who hit a `NameError`, followed by an "Automate the timestepping with a loop" heading.
- **lab3 climate-system-models:** the "spheres" definitions and model components become glossaries, with entries for EBM and GCM. IPCC image links are updated, and Primer figures are now local files.
- **lab4 introducing-cesm:** the cell that saved topo data with `to_netcdf` is removed. The global-mean plot is now built with matplotlib and has labelled axes.
- **lab5 climlab-intro:** adds a `delta_t` variable and an explicit `step_forward()` cell. A new `ebm4` loop stores temperatures in `Tarray` and plots them.
- **lab6 radiation:** raw strings in plot labels, and the units read "μm".
- **lab7 elementary-greenhouse:** ⭐ the biggest change in this group. The two-layer model now gives each layer its own emissivity (ε₀, ε₁) and derives a general OLR formula before simplifying to ε₀ = ε₁ = ε. It uses a new sketch image (`2layerAtm_sketch_general.png`) and adds a partial-code exercise cell for tuning ε.
- **lab8 sympy-greenhouse:** minor changes; the dead link to "Assignment 5" is removed.

### Weeks 4–5

- **lab9 grey-radiation-climlab:** the intro is replaced with the "About climlab / Installing climlab" text. Upstream does **not** have the local Jan 27 2025 `num_lev` bug fix; it hard-codes `num_lev=2`.
- **lab10 radiative-transfer:** the references section becomes a note box with a citation.
- **lab11 spectral-bands:** fixed link anchors. In the forcing and ECS printouts, values are indexed with `[0]`.
- **lab12 radeq / lab13 rce:** API updates only, including `climlab.couple`. rce drops the line "click to expand the code".
- **lab14 sensitivity-feedback:** ⭐ substantive changes.
  - Stratosphere-adjusted forcing (holding levels 13 and below fixed) is replaced by atmosphere-adjusted forcing, which holds only Ts fixed. The quoted results change from ΔR 4.3 → 4.2, λ₀ 3.3 → 3.2, and λ_h2o 1.86 → 1.8.
  - A new plot of the temperature difference profile is added.
  - The NCEP data now loads from the Hawaii APDRC server instead of NOAA.
  - **Upstream uses the AR5 Fig 9.43 feedback figure with a legend, while the local copy uses an AR6 figure.** The local copy is ahead here.
- **lab14_2 advanced-sensitivity-feedback:** λ₀ code updated, sign fixed to −λ₀, and the AR5 citation block replaced with a cite key.
- **lab15 transient-cesm:** `make_map` gains a cyclic point, `title` / `levels` arguments and axis labels. Adds the AR5 Fig 9.43 figure alongside the existing AR5 Table 9.5.
- **lab16 transient-toy:** `.squeeze()` fixes and formatted print statements.

### Weeks 6–7

- **lab17 clouds:** `[0]` indexing on outputs, plus figure and citation changes.
- **lab18 insolation:** ⭐
  - The Hartmann Fig 2.8 image is replaced by code that computes the insolation-weighted zenith angle, citing Cronin 2014.
  - New section "Using real calendar dates" with `np.datetime64`.
  - A finer day grid, which moves the solstice indices to 472/976.
- **lab19 orbital:** the ice-ages intro now comes before the imports. Adds a finer `days` grid, `days20`, gridlines, and named indices (`lat70index`). The plots no longer restrict the time axis to the last 400 kyr.
- **lab20 heat-transport / lab20_2 advanced:** API updates and axis labels. The column sketches are now PDF files under `../images/`.
- **lab21 one-dim-ebm:** `math` → `np`, raw strings, and link fixes.
- **lab22 seasonal-cycle:** NCEP URL changed to `psl.noaa.gov`. Old Lecture links fixed, though upstream still links to `./insolation.ipynb`.
- **lab24 numerical-diffusion:** link and citation fixes only.

### Weeks 8–9

- **lab25 albedo-snowball:** upstream does not have the local `skip_execution` raw cell. Citations and figures updated.
- **lab25_2 / lab25_3 advanced:** "-- test2" removed from the title, plus axis labels and citations. Adds the Hoffman 2017 figure.
- **lab27 surface-energy-balance:** ⭐ rewritten to use the **fully coupled CO2-ramp** runs (`cpl_control` / `cpl_CO2ramp`, last 20 years) instead of the slab-ocean 2xCO2 runs. Monthly climatologies now use `groupby`, the maps use a cartopy Robinson projection, and the interpretation text is updated to match.
- **lab28 land-ocean-contrast:** adds an embedded tweet from Gavin Schmidt. Figures move to `:::{figure}` blocks and maps gain cyclic points.
- **lab29 water-water-everywhere:** the half-evaporation run now loads **`QAqu_halfEvap_old/…cam2.h0.clim.nc`**, a different dataset path. Also `irradiance_factor` and citation changes.

## Local files with no upstream counterpart

`bayes_lecture`, `hydrostat`, `hydrostatic_balance`, `multi_layer_equilibrium`, `pandas_csv_intro`, `pandas-cheatsheet`, `solving-the-stock-and-flow-equation`, `week7/lab23_cesm-atmospheric-dynamics`, `week8/lab26_cesm-coupled-dynamics`, `xarray/*`.

Every upstream file has a local counterpart.

## Watch out before copying upstream over local

The local copy has three things upstream lacks:

1. the AR6 feedback figure in lab14
2. the `num_lev` bug fix in lab9
3. Question 6 in assignment3

Also, `assignment5-cesm-climate-change.md` locally contains student answers.
