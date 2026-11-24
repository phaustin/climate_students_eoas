# Jupyter Book v1 → v2 migration notes

Session date: 2026-11-18

## Result

The Jupyter Book 2 (v2.1.7) version builds 69 pages with the same layout as the v1 site:

- the same 17 sidebar sections in the same order
- the same page titles
- the same two Google Drive links

Lab outputs are still missing (see "Still to do" below).

## The v1 reference site was overwritten, then restored

JB2 writes its HTML to `content/_build/html`, so the first v2 build replaced the v1 site there. That folder is gitignored, so git had no copy of it.

The v1 site was recovered from the `gh-pages` branch (last published 2025-03-10) into `content/_build_v1/html`, where future builds can't touch it. That path was added to `.gitignore`. Its sidebar is identical to the original's.

**Note:** if v1 was rebuilt locally after 2025-03-10, those newer changes are lost.

## What changed

### `content/myst.yml`

This file now holds the full configuration, converted from `_config.yml` and `_toc.yml`:

- title, author, GitHub repo
- files to exclude
- the table of contents (all parts and chapters, including nested sections and URL entries)
- `site.options.folders: true`, so page URLs keep the v1 folder structure, e.g. `courseware/week3/lab5-climlab-intro/`

One difference couldn't be avoided: JB2 turns underscores in page addresses into dashes, so `lab5_climlab-intro.html` becomes `lab5-climlab-intro/`.

### Syllabi

`ugradsyllabus.rst` and `gradsyllabus.rst` were converted to `.md` with pandoc, because JB2 can't read reStructuredText. The inline math was fixed by hand afterwards. The `.rst` originals are still in place.

### Fixes to source files

- Removed 739 empty `<a id='sectionN'></a>` anchors from 36 notebooks. Nothing linked to them, and JB2 reported each one as an error ("Link has no URL").
- Corrected two broken image paths, both now `../../images/...`:
  - `2layerAtm_sketch.png` in `courseware/week3/lab7_elementary-greenhouse.md`
  - `feedback_sketch.png` in `courseware/week5/lab14_2_advanced-sensitivity-feedback.md`
- Replaced the Sphinx-only `{py:meth}` links with plain code text such as `unique()`, which is how v1 displayed them. Files changed:
  - `resources/loading-cmip6-data.md`
  - `resources/loading-CESM-LENS-data.md`
  - `resources/hot_cold_models.md`
- Added `skip_execution: true` to `courseware/week8/lab25_albedo-snowball.md` and `courseware/week8/lab25_3_advanced-snowball-earth.md`. These are the two notebooks v1's `execute.exclude_patterns` skipped.

### Left out on purpose

- `project-resources.md` is listed in the old `_toc.yml`, but the file doesn't exist and it wasn't on the v1 site either.
- v1 numbered the labs in the sidebar ("1." to "26."). JB2 has no equivalent, so they appear unnumbered.

## Still to do: notebook outputs

v1 ran the notebooks during the build (using `.jupyter_cache`), so the labs showed their plots. JB2 builds without running them, so the lab pages currently show code with no output. Many of the paired `.ipynb` files have no saved outputs either.

To match v1, build from inside the course conda environment, which needs climlab and a working Python kernel:

```bash
cd content
pip install "jupyter-book>=2"        # or: conda install -c conda-forge jupyter-book
BASE_URL=/climate_students_eoas jupyter book build --html --execute
```

This wasn't run during the session because it needs that environment and downloads CMIP/CESM data.

To build without execution, using pixi (JB2 isn't installed globally on this machine; `pixi exec` doesn't change the setup):

```bash
cd content
BASE_URL=/climate_students_eoas pixi exec -s "jupyter-book>=2" -s imagemagick -s libwebp -s ghostscript \
    jupyter-book build --html
```

imagemagick and ghostscript are needed to convert the PDF figures in lab20.

## Other notes

- `content/doit.sh` publishes `_build/html` to GitHub Pages with `ghp-import`. That still works with JB2, but run it only once v2 looks right, because it will replace the v1 site that `gh-pages` currently serves.
- Remaining build warnings don't affect layout:
  - a few Wikimedia and IPCC images that couldn't be downloaded during the build (the pages link to them online instead)
  - KaTeX math warnings about an invisible Unicode character (U+2061)
  - a few duplicate figure labels (`directive-fig`, `costheta`)
  - a few remaining empty links in `lab1_models-budgets-fun.ipynb` and `hydrostatic_balance.md`
- Nothing was committed. `content/resources/tutorials/historical_data.md` already had uncommitted changes before the session started.
