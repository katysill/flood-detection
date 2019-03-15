# Flood detection workflow

This repository is for a research project focused on differentiating building shadow from flood waters in urban settings during flooding events. The workflow is motivated by the challenges in rapidly and accurately assessing flooding extent utilizing high resolution remote sensing imagery, as shadows from buildings look spectrally similar to water. The workflow utilize packages from scikit-image, scikit-learn, NumPy, glob, os, RasterIO, and EarthPy. 

# notebooks
The 'NDWI_MSI_with_modules' notebook can be used to calculate the normalized difference water index (NDWI), morphological shadow index (MSI), normalized difference vegetation index (NDVI), and morphological building index (MBI). Inputs include WorldView-2 imagery as geoTIFF files. The notebook writes out each of these indices as a geoTIFF to a specified outputs folder. In addition to index calculations, the notebooks also creates masks for each index based on user defined thresholds. For example, as written, the shadow_mask is defined as MSI >= 0.08. Each mask is also written out as a geoTIFF. Finally, the notebook includes some experimentation with different formulations, combinations and analyses of NDWI and MSI. 

# modules
Two modules were developed and are required to run the 'NDWI_MSI_with_modules' notebook. The first module, calc_array_mask, contains functions to define and apply a cloud mask to an N-dimensional array. The second module, morph_indices, provides functions to calculate MSI, MBI and reduce noise using morphological opening. 

# Reproducing the analysis

To run the notebook, the user must have geoTIFF files from an area of interest and update the "aoi" parameter to the name of the folder containing geoTIFF files. Also, ensure to update band_path as necessary. 
