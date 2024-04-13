import xarray as xr
import math

from . import Utils


# Internal functions:


def _rsnpp_day_img(ri1, ri2, ri3, bi4, bi5, nmask):
    """
        Day reflectance/thermal I-bands cloud test
        Based on the M.Piper, T.Bahr (2015).
        A RAPID CLOUD MASK ALGORITHM FOR SUOMI NPP VIIRS IMAGERY EDRS
    Args:
        ri1 (list|np.ndarray|xr.Dataset): I01 in reflectance calibration
        ri2 (list|np.ndarray|xr.Dataset): I02 in reflectance calibration
        ri3 (list|np.ndarray|xr.Dataset): I03 in reflectance calibration
        bi4 (list|np.ndarray|xr.Dataset): I04 in BT calibration
        bi5 (list|np.ndarray|xr.Dataset): I05 in BT calibration
        nmask (list|np.ndarray|xr.Dataset): Day/night mask (True is night)
    Returns:
        (list|np.ndarray|xr.Dataset): binary cloud mask,
            True is cloud, False is clear pixel
            Can contain NaN values
    """

    t1 = xr.where(ri1 > 8, True, False)

    # TODO: check this test
    ndsi = (ri1 - ri3) / (ri1 + ri3)
    t2 = xr.where(ndsi < 0.7, True, False)
    t2 = xr.where(ri2 > 11, t2, False)

    t3 = xr.where(bi5 < 300, True, False)

    ri3_max = Utils.max_values(ri3)
    t4 = xr.where((ri3_max - ri3) * bi5 / 100 < 410, True, False)

    t5 = xr.where(ri2 / ri1 < 2, True, False)

    t6 = xr.where(ri2 / ri3 > 1, True, False)

    cm = xr.where(t1, t2, False)
    cm = xr.where(t3, cm, False)
    cm = xr.where(t4, cm, False)
    cm = xr.where(t5, cm, False)
    cm = xr.where(t6, cm, False)

    cm = xr.where(nmask is False, cm, math.nan)

    return cm


def _thermal_img(bi4, bi5):
    """
        Night termal I-bands cloud test
        Based on the W.Schroeder, P.Oliva, L.Giglio, I.A.Csiszar (2014).
        The New VIIRS 375 m active fire detection data product:
            Algorithm description and initial assessment
    Args:
        bi4 (list|np.ndarray|xr.Dataset): I04 in BT calibration
        bi5 (list|np.ndarray|xr.Dataset): I05 in BT calibration
    Returns:
        (list|np.ndarray|xr.Dataset): binary cloud mask,
            True is cloud, False is clear pixel
            Can contain NaN values
    """
    cm = xr.where(bi4 < 265, True, False)
    cm = xr.where(bi5 < 295, cm, False)
    cm = xr.where(bi4.notnull(), cm, math.nan)

    return cm


# Public wrappers:


def rsnpp_day_img(ri1, ri2, ri3, bi4, bi5, nmask):
    """
        Day reflectance/thermal I-bands cloud test
        Based on the M.Piper, T.Bahr (2015).
        A RAPID CLOUD MASK ALGORITHM FOR SUOMI NPP VIIRS IMAGERY EDRS
    Args:
        ri1 (list|np.ndarray|xr.Dataset): I01 in reflectance calibration
        ri2 (list|np.ndarray|xr.Dataset): I02 in reflectance calibration
        ri3 (list|np.ndarray|xr.Dataset): I03 in reflectance calibration
        bi4 (list|np.ndarray|xr.Dataset): I04 in BT calibration
        bi5 (list|np.ndarray|xr.Dataset): I05 in BT calibration
        nmask (list|np.ndarray|xr.Dataset): Day/night mask (True is night)
    Returns:
        (list|np.ndarray|xr.Dataset): binary cloud mask,
            True is cloud, False is clear pixel
            Can contain NaN values
    """
    Utils._check_data(ri1)
    Utils._check_data(ri2)
    Utils._check_data(ri3)
    Utils._check_data(bi4)
    Utils._check_data(bi5)
    Utils._check_data(nmask)

    return _rsnpp_day_img(
        ri1, ri2, ri3,
        bi4, bi5,
        nmask
    )


def thermal_img(bi4, bi5):
    """
        Night termal I-bands cloud test
        Based on the W.Schroeder, P.Oliva, L.Giglio, I.A.Csiszar (2014).
        The New VIIRS 375 m active fire detection data product:
            Algorithm description and initial assessment
    Args:
        bi4 (list|np.ndarray|xr.Dataset): I04 in BT calibration
        bi5 (list|np.ndarray|xr.Dataset): I05 in BT calibration
    Returns:
        (list|np.ndarray|xr.Dataset): binary cloud mask,
            True is cloud, False is clear pixel
            Can contain NaN values
    """
    Utils._check_data(bi4)
    Utils._check_data(bi5)
    return _thermal_img(bi4, bi5)


def day_night_img(ri1, ri2, ri3, bi4, bi5, nmask):
    """
        Wrapper for getting cloud mask for any time
        using RSNPP and thermal cloud masks algs
    Args:
        ri1 (list|np.ndarray|xr.Dataset): I01 in reflectance calibration
        ri2 (list|np.ndarray|xr.Dataset): I02 in reflectance calibration
        ri3 (list|np.ndarray|xr.Dataset): I03 in reflectance calibration
        bi4 (list|np.ndarray|xr.Dataset): I04 in BT calibration
        bi5 (list|np.ndarray|xr.Dataset): I05 in BT calibration
        nmask (list|np.ndarray|xr.Dataset): Day/night mask (True is night)
    Returns:
        (list|np.ndarray|xr.Dataset): binary cloud mask,
            True is cloud, False is clear pixel
            Can contain NaN values
    """
    Utils._check_data(ri1)
    Utils._check_data(ri2)
    Utils._check_data(ri3)
    Utils._check_data(bi4)
    Utils._check_data(bi5)
    Utils._check_data(nmask)

    dcm = _rsnpp_day_img(ri1, ri2, ri3, bi4, bi5)
    ncm = _thermal_img(bi4, bi5)

    return xr.where(nmask, ncm, dcm)


# Public xr.Dataset wrappers:


def rsnpp_day_img_ds(ds, nmask):
    """
        Wrapper for day reflectance/thermal I-bands cloud test
            for xr.Dataset objects
        Based on the M.Piper, T.Bahr (2015).
        A RAPID CLOUD MASK ALGORITHM FOR SUOMI NPP VIIRS IMAGERY EDRS
    Args:
        ds (xr.Dataset): dataset with I01-I05 bands data
        nmask (xr.Dataset): Day/night mask (True is night)
    Returns:
        (xr.Dataset): binary cloud mask,
            True is cloud, False is clear pixel
            Can contain NaN values
    """
    if not isinstance(ds, xr.Dataset):
        raise ValueError(
            "Incorrect input data format"
        )
    if not isinstance(nmask, xr.DataArray):
        raise ValueError(
            "Incorrect input data format"
        )
    return rsnpp_day_img(
        ds['I01'],
        ds['I02'],
        ds['I03'],
        ds['I04'],
        ds['I05'],
        nmask
    )


def thermal_img_ds(ds):
    """
        Wrapper for Night termal I-bands cloud test for xr.Dataset
        Based on the W.Schroeder, P.Oliva, L.Giglio, I.A.Csiszar (2014).
        The New VIIRS 375 m active fire detection data product:
            Algorithm description and initial assessment
    Args:
        ds (xr.Dataset): dataset with I01-I05 bands data
        nmask (list|np.ndarray|xr.Dataset): Day/night mask (True is night)
    Returns:
        (xr.Dataset): binary cloud mask,
            True is cloud, False is clear pixel
            Can contain NaN values
    """
    if not isinstance(ds, xr.Dataset):
        raise ValueError(
            "Incorrect input data format"
        )
    return thermal_img(
        ds['I04'],
        ds['I05']
    )


def day_night_img_ds(ds, nmask):
    """
        Wrapper for getting cloud mask for any time
        using RSNPP and thermal cloud masks algs
        from xr.Dataset object
    Args:
        ds (xr.Dataset): dataset with I01-I05 bands data
        nmask (list|np.ndarray|xr.Dataset): Day/night mask (True is night)
    Returns:
        (xr.Dataset): binary cloud mask,
            True is cloud, False is clear pixel
            Can contain NaN values
    """
    if not isinstance(ds, xr.Dataset):
        raise ValueError(
            "Incorrect input data format"
        )
    if not isinstance(nmask, xr.DataArray):
        raise ValueError(
            "Incorrect input data format"
        )
    return day_night_img(
        ds['I01'],
        ds['I02'],
        ds['I03'],
        ds['I04'],
        ds['I05'],
        nmask
    )
