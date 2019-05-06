
""" The functions in this module can be used to calculated the morphological
shadow index (MSI) and morphological building index (MBI). Additionally,
de-noising functions are included using both morphological smoothing and
labeling methods. These functions were developed  improve flood detection
in urban environments."""


import numpy as np

def selemline(length, theta, dtype=np.uint8):

    """This function calculates a linear structuring element.
    The linear stucturing element is used in the calc_msi and calc_mbi functions

    Parameters
    ------------
    length: numerical (integer) input
    theta: numerical (integer) input for angle of structuring element

    Returns
    ------------
    Structuring element of a specified length and angle
    Data type is an integer
    """
    import numpy as np
    from skimage import draw

    theta_d = theta * np.pi / 180
    X = int(round((length-1)/2. * np.cos(theta_d)))
    Y = int(-round((length-1)/2. * np.sin(theta_d)))
    C, R, V = draw.line_aa(-X, -Y, X, Y)
    M = 2*max(abs(R)) + 1
    N = 2*max(abs(C)) + 1
    selem = np.zeros((M, N)).astype(dtype)
    selem[R + max(abs(R)), C + max(abs(C))] = 1
    return selem

def calc_msi(raster_input, s_min, s_max, s_delta):

    """ Calculates morphological shadow index (MSI) per Huang et al. (2015)
    Assumes use of linear structuring element
    MSI = sum(dxs)(blacktop_hat(morphological profiles))/(D*S)
    d = degrees (0,45, 90, 135)
    D = 4
    s = size of linear structuring element (pixels)
    S = (s_max-s_min)/s_delta + 1

    Parameters
    ------------
    raster_input : 3-dim raster (tif) stack for calculating brightness
    s_min, s_max, s_delta: numerical input (integer)

    Returns
    ------------
    Calculated values for MSI in a numpy array
    """
    import numpy as np
    import numpy.ma as ma
    from skimage.morphology import black_tophat
    from skimage import draw

    # Calculate brightness for cloud masked stack
    brightness=np.nanmax(raster_input, axis=0)

    # Cap brightness values at a max of 1. Replace all values greater than 1 with a value of 1
    brightness_cap=np.where(brightness>1,1,brightness)

    # Initialize inputs for MSI calculation
    selem = selemline(0,0)
    b_tophat_array_sum = black_tophat(brightness_cap, selem)

    # Loop and sum black tophat morphological profiles for MSI calculation
    for i in range(s_min,s_max+s_delta,s_delta):
        for x in range(0, 4):
            selem = selemline(i,45*x)
            b_tophat = black_tophat(brightness_cap,selem)
            b_tophat_array_sum = b_tophat_array_sum.__add__(b_tophat)

    D = 4
    S = ((s_max-s_min)/s_delta) + 1
    msi = b_tophat_array_sum/(D*S)

    return msi


def calc_mbi(raster_input, s_min, s_max, s_delta):

    """ Calculates morphological building index (MBI) per Huang et al. (2015)
    Assumes use of linear structuring element
    MBI = sum(dxs)(whitetop_hat(morphological profiles))/(D*S)
    d = degrees (0,45, 90, 135)
    D = 4
    s = size of linear structuring element (pixels)
    S = (s_max-s_min)/s_delta + 1

    Parameters
    ------------
    raster_input : 3-dim raster (tif) stack for calculating brightness
    s_min, s_max, s_delta: numerical input (integer)

    Returns
    ------------
    Calculated values for MBI in a numpy array
    """

    import numpy as np
    import numpy.ma as ma
    from skimage.morphology import white_tophat
    from skimage import draw

 
    # Calculate brightness for cloud masked stack
    brightness=np.nanmax(raster_input, axis=0)

    # Cap brightness values at a max of 1. Replace all values greater than 1 with a value of 1
    brightness_cap=np.where(brightness>1,1,brightness)

    # Initialize inputs for MBI calculation
    selem = selemline(0,0)
    w_tophat_array_sum = white_tophat(brightness_cap, selem)

    # Loop and sum black tophat morphological profiles for MSI calculation
    for i in range(s_min,s_max+s_delta,s_delta):
        for x in range(0, 4):
            selem = selemline(i,45*x)
            w_tophat = white_tophat(brightness_cap,selem)
            w_tophat_array_sum = w_tophat_array_sum.__add__(w_tophat)

    D = 4
    S = ((s_max-s_min)/s_delta) + 1
    mbi = w_tophat_array_sum/(D*S)

    return mbi


def smooth_disk(index_array,threshold, disk_size):

    """Applies morphological opening to a numpy array
    User inputs numpy array to be opened, threshold and disk_size for disk shaped
    structuring element

    Parameters
    ----------------
    morph_index : numpy array (either MSI or MBI)
    threshold : numerical input (integer, float)
    disk_size : numerical input (integer) size of structuring elements (number of pixels)

    Returns
    ---------------
    Morphologically opened and "smoothed" numpy arrays
    Return is a mask (values of 0 or 1) that has had smal
    """

    from skimage.morphology import opening, disk

    # Create a mask based on user defined threshold values
    index_threshold_mask = (index_array>=threshold).astype(int)
    
    # Define the structure element based on the user defined disk size
    selem = disk(disk_size)
    
    # Apply the morphological opening function to the thresholded raster
    index_opened = opening(index_threshold_mask, selem)

    return index_opened


def remove_small_patches(raster_input, patch_threshold):

    """ Removes noise from raster image based on user-defined threshold
    Connected objects less than the patch_threshold size will be removed
    Written for removing noise from flood and cloud cloud_mask_to_shape

    Parameters
    ----------------
    raster_input : numpy array
    patch_threshold : numerical input (integer) defining patch size (pixels) to be removed

    Returns
    ----------------
    raster_cleaned : numpy array with small patches removed

    """

    from skimage import measure, morphology

    # Labels connected object within the image
    patch_labels = measure.label(raster_input, background=0)
    
    # Removes all objects less than the user defined patch_threshold
    raster_cleaned = morphology.remove_small_objects(patch_labels, min_size=patch_threshold)
    return raster_cleaned
