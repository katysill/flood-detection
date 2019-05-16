''' The functions in this module can be used to define and apply a mask
to an individual or stack of raster files. The functions were designed
specfically to define and apply a cloud mask to a raster stack.'''

import numpy as np
import numpy.ma as ma
from skimage.morphology import disk, opening


def define_mask(band1, band2,threshold1, threshold2, disk_size):

    """ This function creates a mask (values of 0 or 1) based on two user
    defined inputs and two thresholds.
    This function was developed to create a cloud mask based on two input
    bands and associated thresholds.
    Finally, this function applies morphological opening using the user
    input disk_size for structuring element

    Parameters
    -----------
    band1 & band2 : numpy arrays
    threshold1 & threshold2 : numeric value (e.g., integer, float)
    disk_size : numeric value (integer)

    Returns
    -----------
    Morphologically opened numpy array mask (values of 0 or 1)

    """
    if not (band1.shape == band2.shape):
        raise ValueError("Both arrays should have the same dimensions")

    cloud = ((band1 >= threshold1) & (band2 >= threshold2)).astype(int)
    selem = disk(disk_size)
    cloud_opened = opening(cloud, selem)
    return cloud_opened


def apply_mask(mask_array, raster_input):

    """ Applies mask to raster. Function was written to apply a
    previously defined cloud mask to a raster stack.

    Parameters
    -----------
    input_mask : output from define_mask function; numpy array
    raster_file: raster to be masked. can be single raster or stack

    Returns
    ----------
    Cloud masked raster file or stack as a numpy array
    """

    mask_to_shape = np.broadcast_to(mask_array == 1, raster_input.shape)
    raster_masked = ma.masked_array(raster_input,
                                      mask=mask_to_shape)

    return raster_masked
