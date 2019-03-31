# Flood detection workflow

This repository is for a research project focused on differentiating building shadow from flood waters in urban settings during flooding events. The workflow is motivated by the challenges in rapidly and accurately assessing flooding extent utilizing high resolution remote sensing imagery, as shadows from buildings look spectrally similar to water. The workflow utilizes packages from NumPy, Matplotlib, scikit-image, scikit-learn, RasterIO, and EarthPy. THe workbook was developed using the [earth-analytics-python environment](https://github.com/earthlab/earth-analytics-python-env)

# data required

The notebooks were developed using WorldView-2 pan sharpened 8-band geoTIFF files for a flooding event in Abidjan, Ivory Coast on June 17, 2016. Data was accessed using DigitalGlobe's [GBDX portal](https://platform.digitalglobe.com/gbdx/). A subscription is required to access the imagery, though a 30 day trial was available for users at the time of writing (March 2019). 

The analysis was run on an image focused on the Koumassi area of Abidjan. Different pan-sharpened WorldView-2 images can be run. 

# notebooks
The 'NDWI_MSI_with_modules' notebook can be used to calculate the normalized difference water index (NDWI), morphological shadow index (MSI), normalized difference vegetation index (NDVI), and morphological building index (MBI). The notebook writes out each of these indices as a geoTIFF to a specified outputs folder. In addition to index calculations, the notebook also creates masks for each index based on user defined thresholds. Each mask is also written out as a geoTIFF. Finally, the notebook includes some experimentation and exploration with different formulations and analyses of NDWI and MSI. 
- To run the notebook, the user must update the "aoi" parameter to the name of the folder containing geoTIFF files from a location of interest. Also, ensure to update band_path as necessary.


The 'k-means_exploration' and 'SVM_exploration' notebooks are working notebooks to explore how unsupervised and supervised learning might improve the workflow goal of differentiating building shadow from flood waters. 

# modules
Two modules were developed and are required to run the 'NDWI_MSI_with_modules' notebook. The first module, calc_array_mask, contains functions to define and apply a cloud mask to a single array or stack of arrays. The second module, morph_indices, provides functions to calculate MSI, MBI and reduce noise using morphological opening. 

# development environment
The notebooks were developed using Python 3.7.1 on a Windows system
