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

<img src="images/dask_horizontal.svg" align="left" width="30%">

+++

# Dask Arrays with Xarray

Dask Array provides a parallel, larger-than-memory, n-dimensional array using blocked algorithms. Simply put: distributed Numpy.

*  **Parallel**: Uses all of the cores on your computer
*  **Larger-than-memory**:  Lets you work on datasets that are larger than your available memory by breaking up your array into many small pieces, operating on those pieces in an order that minimizes the memory footprint of your computation, and effectively streaming data from disk.
*  **Blocked Algorithms**:  Perform large computations by performing many smaller computations

This notebook demonstrates one of Xarray's most powerful features: the ability to wrap dask arrays and allow users to seamlessly execute analysis code in parallel.


## Learning Objectives

- Learn the distinction between *eager* and *lazy* execution, and how Xarray can work either way
- Understand key features of dask arrays
- Work with Dask Arrays in much the same way you would work with a NumPy array
- Learn that xarray DataArrays and Datasets are "dask collections" i.e. you can execute top-level dask functions such as dask.visualize(xarray_object)
- Learn that all xarray built-in operations can transparently use dask

## Prerequisites


| Concepts | Importance | Notes |
| --- | --- | --- |
| [Introduction to NumPy](../numpy/numpy-basics) | Necessary | Familiarity with Data Arrays |
| [Introduction to Xarray](xarray-intro) | Necessary | Familiarity with Xarray Data Structures |


- **Time to learn**: *30-40 minutes*

+++

## Imports

```{code-cell} ipython3
import dask
import dask.array as da
import numpy as np
import xarray as xr
from dask.diagnostics import ProgressBar
from dask.utils import format_bytes
from pythia_datasets import DATASETS
```

## Blocked algorithms

A *blocked algorithm* executes on a large dataset by breaking it up into many small blocks.

For example, consider taking the sum of a billion numbers, in a single computation. This would take a while. We might instead break up the array into 1,000 chunks, each of size 1,000,000, take the sum of each chunk, and then take the sum of the intermediate sums.

We achieve the intended result (one sum on one billion numbers) by performing many smaller results (one thousand sums on one million numbers each, followed by another sum of a thousand numbers.)

+++

### `dask.array` contains these algorithms

`dask.array` implements a subset of the NumPy ndarray interface using blocked algorithms, cutting up the large array into many small arrays. This lets us compute on arrays larger than memory using multiple cores. Dask coordinates these blocked algorithms using Dask graphs. Dask Arrays are also **lazy**, meaning that they do not evaluate until you explicitly ask for a result using the compute method.

+++

### Create a `dask.array` object

If we want to create a 3D NumPy array of random values, we do it like this:

```{code-cell} ipython3
:tags: []

shape = (600, 200, 200)
arr = np.random.random(shape)
arr
```

```{code-cell} ipython3
format_bytes(arr.nbytes)
```

This array contains `~183 MB` of data

+++

Now let's create the same array using Dask's array interface.

```{code-cell} ipython3
darr = da.random.random(shape, chunks=(300, 100, 200))
```

A chunk size to tell us how to block up our array, like `(300, 100, 200)`. 

+++

<div class="admonition alert alert-info">
    <p class="admonition-title" style="font-weight:bold">Specifying Chunks</p>
    There are <a href="https://docs.dask.org/en/latest/array-chunks.html">several ways to specify chunks</a>. In this tutorial, we will use a block shape.


</div>


```{code-cell} ipython3
darr
```

Notice that we just see a symbolic representation of the array, including its `shape`, `dtype`, and `chunksize`. No data has been generated yet. Let's visualize the constructed task graph. 

```{code-cell} ipython3
darr.visualize()
```

Our array has four chunks. To generate it, Dask calls `np.random.random` four times and then concatenates this together into one array.

+++

### Manipulate a `dask.array` object as you would a numpy array


Now that we have an `Array` we perform standard numpy-style computations like arithmetic, mathematics, slicing, reductions, etc..

The interface is familiar, but the actual work is different. `dask_array.sum()` does not do the same thing as `numpy_array.sum()`.

#### What's the difference?

`dask_array.sum()` builds an expression of the computation. It does not do the computation yet, also known as **lazy execution**. `numpy_array.sum()` computes the sum immediately (**eager execution**).

#### Why the difference?

A `dask.array` is split into chunks. Each chunk must have computations run on that chunk explicitly. If the desired answer comes from a small slice of the entire dataset, running the computation over all data would be wasteful of CPU and memory.

```{code-cell} ipython3
total = darr.sum()
total
```

```{code-cell} ipython3
total.visualize()
```

#### Compute the result

`dask.array` objects are lazily evaluated.  Operations like `.sum` build up a graph of blocked tasks to execute.  

We ask for the final result with a call to `.compute()`.  This triggers the actual computation.

```{code-cell} ipython3
%%time
total.compute()
```

### Exercise with `dask.arrays`
Modify the chunk size (or shape) in the random dask array, call `.sum()` on the new array, and visualize how the task graph changes.

```{code-cell} ipython3
da.random.random(shape, chunks=(50, 200, 400)).sum().visualize()
```

Here we see Dask's strategy for finding the sum. This simple example illustrates the beauty of Dask: it automatically designs an algorithm appropriate for custom operations with big data.

+++

If we make our operation more complex, the graph gets more complex:

For an example, we use an arbitrarily complex calculation.

```{code-cell} ipython3
z = darr.dot(darr.T).mean(axis=0)[::2, :].std(axis=1)
z
```

```{code-cell} ipython3
z.visualize()
```

### Testing a bigger calculation

The examples above were toy examples; the data (180 MB) is probably not big enough to warrant the use of Dask.

We can make it a lot bigger! Let's create a new, big array

```{code-cell} ipython3
darr = da.random.random((4000, 100, 4000), chunks=(1000, 100, 500)).astype('float32')
darr
```

This dataset is `~6 GB`, rather than 32 MB! This is probably close to or greater than the amount of available RAM than you have in your computer. Nevertheless, Dask has no problem working on it.

```{code-cell} ipython3
z = (darr + darr.T)[::2, :].mean(axis=2)
```

```{code-cell} ipython3
z.visualize()
```

```{code-cell} ipython3
with ProgressBar():
    computed_ds = z.compute()
```

## Dask Arrays with Xarray

Often times, you won't be directly interacting with `dask.arrays` directly; odds are you will be interacting with them via [`Xarray`!](http://xarray.pydata.org/en/stable/
) Xarray wraps NumPy arrays similar to how we showed in the previous section, helping the user jump right into the dask array interface!

+++

### Reading data with `Dask` and `Xarray`

Recall that a Dask's array consists of many chunked arrays:

```{code-cell} ipython3
darr
```

To read data as Dask arrays with Xarray, we need to specify the `chunks` argument to `open_dataset()` function. 

```{code-cell} ipython3
ds = xr.open_dataset(DATASETS.fetch('CESM2_sst_data.nc'), chunks={})
ds.tos
```

Passing `chunks={}` to `open_dataset()` works, but since we didn't tell dask how to split up (or chunk) the array, Dask will create a single chunk for our array.

The `chunks` here indicate how values should go into each chunk - for example, `chunks={'time':90}` will tell `Xarray` + `Dask` to place 90 time slices into a single chunk.

Notice how `tos` (sea surface temperature) is now split in the time dimension, with two chunks (since there are a total of 180 time slices in this dataset).

```{code-cell} ipython3
ds = xr.open_dataset(
    DATASETS.fetch('CESM2_sst_data.nc'),
    engine="netcdf4",
    chunks={"time": 90, "lat": 180, "lon": 360},
)
ds.tos
```

Calling `.chunks` on the `tos` `xarray.DataArray` displays the number of slices in each dimension within each chunk, with (`time`, `lat`, `lon`). Notice how there are now **two** chunks each with 90 time slices for the time dimension.

```{code-cell} ipython3
ds.tos.chunks
```

### Xarray data structures are first-class dask collections

This means you can call the following functions 

- `dask.visualize(...)`
- `dask.compute(...)`

on both `xarray.DataArray` and `xarray.Dataset` objects backed by `dask.array`.

Let's visualize our dataset using Dask!

```{code-cell} ipython3
dask.visualize(ds)
```

### Parallel and lazy computation using `dask.array` with Xarray


Xarray seamlessly wraps Dask so all computation is deferred until explicitly requested. 

```{code-cell} ipython3
z = ds.tos.mean(['lat', 'lon']).dot(ds.tos.T)
z
```

As you can see, `z` contains a Dask array. This is true for all Xarray built-in operations including subsetting

```{code-cell} ipython3
z.isel(lat=0)
```

We can visualize this subset too!

```{code-cell} ipython3
dask.visualize(z)
```

Now that we have prepared our calculation, we can go ahead and call `.compute()`

```{code-cell} ipython3
with ProgressBar():
    computed_ds = z.compute()
```

---

+++

## Summary

We saw that we can use `Xarray` to access `dask.arrays`, which required passing a `chunks` argument to upon opening the dataset. Once the data were loaded into Xarray, we could interact with the `xarray.Datasets` and `xarray.DataArrays` as we would if we were working with `dask.arrays`. This can be a powerful tool for working with larger-than-memory datasets!

### Dask Shortcomings

Dask Array does not implement the entire Numpy interface.  Users expecting this
will be disappointed.  Notably Dask Array has the following failings:

1.  Dask Array does not support some operations where the resulting shape
    depends on the values of the array. For those that it does support
    (for example, masking one Dask Array with another boolean mask),
    the chunk sizes will be unknown, which may cause issues with other
    operations that need to know the chunk sizes.
2.  Dask Array does not attempt operations like ``sort`` which are notoriously
    difficult to do in parallel and are of somewhat diminished value on very
    large data (you rarely actually need a full sort).
    Often we include parallel-friendly alternatives like [``topk``](https://pytorch.org/docs/stable/generated/torch.topk.html).
3.  Dask development is driven by immediate need, and so many lesser used
    functions, like ``np.sometrue`` have simply not been implemented yet.  These would make excellent community contributions.

## Learn More

Visit the [Dask Array documentation](https://docs.dask.org/en/latest/array.html). In particular, this [array screencast](https://youtu.be/9h_61hXCDuI) will reinforce the concepts you learned here.


```{code-cell} ipython3
from IPython.display import YouTubeVideo

YouTubeVideo(id="9h_61hXCDuI", width=600, height=300)
```

## Resources and references

* Reference
    *  [Dask Docs](https://dask.org/)
    *  [Dask Examples](https://examples.dask.org/)
    *  [Dask Code](https://github.com/dask/dask/)
    *  [Dask Blog](https://blog.dask.org/)
    
    *  [Xarray Docs](https://xarray.pydata.org/)
  
*  Ask for help
    *   [`dask`](http://stackoverflow.com/questions/tagged/dask) tag on Stack Overflow, for usage questions
    *   [github discussions: dask](https://github.com/dask/dask/discussions) for general, non-bug, discussion, and usage questions
    *   [github issues: dask](https://github.com/dask/dask/issues/new) for bug reports and feature requests
     *   [github discussions: xarray](https://github.com/pydata/xarray/discussions) for general, non-bug, discussion, and usage questions
    *   [github issues: xarray](https://github.com/pydata/xarray/issues/new) for bug reports and feature requests
    
* Pieces of this notebook are adapted from the following sources
  * [Dask Array Tutorial](https://tutorial.dask.org/02_array.html)
  * [Parallel Computing with Xarray and Dask](https://tutorial.xarray.dev/intermediate/xarray_and_dask.html)

```{code-cell} ipython3

```
