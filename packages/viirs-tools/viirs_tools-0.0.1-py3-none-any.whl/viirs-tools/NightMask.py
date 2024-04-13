import xarray as xr
import numpy as np
import math

from . import Utils

# Public functions:


def naive(refband, btband):
    """
        Get night mask from any reflectance and brightness bands
        Day/Night state here meets the condition SZA < 90 deg
        Assumed that data was loaded in the reflectance or
            brightness-temperature, not radiance calibration
    Args:
        refband (list|np.ndarray|xr.DataArray):
            any reflectance data
        btband (list|np.ndarray|xr.DataArray):
            any brightness-temperature data
    Returns:
        (list|np.ndarray|xr.DataArray): bool mask,
            True means night state, False means day state,
            Can contain NaN values in case of missing data in BT band
    """
    bmask = None
    rmask = None
    t1 = xr.DataArray
    t2 = (list, np.ndarray)
    if isinstance(refband, t1) and isinstance(btband, t1):
        bmask = btband.notnull()
        rmask = refband.isnull()
    elif isinstance(refband, t2) and isinstance(btband, t2):
        bmask = np.logical_not(np.isnan(btband))
        rmask = np.isnan(refband)
    else:
        raise ValueError(
            "Incorrect input data format"
        )
    return xr.where(bmask, rmask, math.nan)


# Internal wrappers:


def _naive_ds(ds, refbands, btbands):
    """
        Internal wrapper for getting night mask from xr.Dataset
        Day/Night state here meets the condition SZA < 90 deg
        Assumed that data was loaded in the reflectance or
            brightness-temperature, not radiance calibration
    Args:
        ds (xr.Dataset): original data
        refbands (list of strings): names of reflectance datasets
        btbands (list of strings): names of BT datasets
    Returns:
        (xr.Dataset): night mask
    """
    if not isinstance(ds, xr.Dataset):
        raise ValueError(
            "Incorrect input data format"
        )
    refband = None
    btband = None
    for b in refbands:
        if b in ds.data_vars:
            refband = b
            break
    for b in btbands:
        if b in ds.data_vars:
            btband = b
            break
    if refband is None or btband is None:
        raise ValueError(
            "Input data does not contain both ref and bt data"
        )
    rd = Utils._get_da(ds, refband)
    bd = Utils._get_da(ds, btband)
    return naive(rd, bd)


# Public xr.Dataset wrappers:


def naive_ds_img(ds):
    """
        Wrapper for getting night mask from xr.Dataset directly
            using imagery resolution (I-bands)
        Day/Night state here meets the condition SZA < 90 deg
        Assumed that data was loaded in the reflectance or
            brightness-temperature, not radiance calibration
    Args:
        ds (xr.Dataset): contains both reflectance and
            brightness-temperature data
    Returns:
        (xr.DataArray): night mask, as described
            in the naive(refband, btband)
    """
    rbands = ['I{}'.format(i) for i in range(1, 3 + 1)]
    bbands = ['I{}'.format(i) for i in range(4, 5 + 1)]
    return _naive_ds(ds, rbands, bbands)


def naive_ds_mod(ds):
    """
        Wrapper for getting night mask from xr.Dataset directly
            using moderate resolution (M-bands)
        Day/Night state here meets the condition SZA < 90 deg
        Assumed that data was loaded in the reflectance or
            brightness-temperature, not radiance calibration
    Args:
        ds (xr.Dataset): contains both reflectance and
            brightness-temperature data
    Returns:
        (xr.DataArray): night mask, as described
            in the naive(refband, btband)
    """
    rbands = ['M{}'.format(i) for i in range(1, 11 + 1)]
    bbands = ['M{}'.format(i) for i in range(12, 16 + 1)]
    return _naive_ds(ds, rbands, bbands)
