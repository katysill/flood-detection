import numpy as np
import pandas as pd
import rasterio as rio

def sample_vals(aoi, x_coords,y_coords,raw_list):
    i = 0
    index_list = []
    filename = []
    if len(aoi) == 17:
        a = 57
    else:
        a = 52

    for raw in raw_list:
        sampled_values = []

        # Sample raster at each combo of x and y coordinates
        with rio.open(raw) as src:
            for val in src.sample(zip(x_coords, y_coords)):
                i = i+1
                # Note that each val is an individual numpy array
                sampled_values.append(val)
            arr = np.array([sampled_values]).squeeze()
            index_list.append([arr])
            filename.append(raw[a:77])

    labels = filename
    index_vals = pd.DataFrame(np.concatenate(index_list))
    index_vals = index_vals.transpose()
    index_vals.columns = labels
    return index_vals
