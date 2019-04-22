# Flood detection workflow

This repository is for a research project focused on differentiating building shadow from flood waters in urban settings during flooding events. The workflow is motivated by the challenges in rapidly and accurately assessing flooding extent utilizing high resolution remote sensing imagery, as shadows from buildings look spectrally similar to water. The workflow utilizes packages from NumPy, Matplotlib, scikit-image, scikit-learn, RasterIO, and EarthPy. The workbook was developed using the [earth-analytics-python environment](https://github.com/earthlab/earth-analytics-python-env)

The repository includes provides code for running three different methods for identifying floods from DigitalGlobe's WorldView-2 imagery. The three methods include: thresholding spectral indices, applying supervised machine learning methods and applying unsupervised machine learning methods. Each of the three methods can be found in the following notebooks:

- Thresholding spectral indices: final_calculating_water_shadow_indices.ipynb
- Supervised machine learning: final_supervised_ML_SVM_random_forest.ipynb
- Unsupervised machine learning: final_unsupervised_ML_kmeans_GMM.ipynb

Note that the supervised machine learning notebook relies on inputs from final_calculating_water_shadow_indices.ipynb

Additional "explorations" notebooks have been included showing more of the process completed to finalize each of the supervised and unsupervised models. Note that the explorations notebooks rely on inputs from final_calculating_water_shadow_indices.ipynb

# input data required

The notebooks were developed using WorldView-2 pan sharpened 8-band geoTIFF files for a flooding event in Abidjan, Ivory Coast on June 17, 2016. Imagery data was accessed using DigitalGlobe's [GBDX portal](https://platform.digitalglobe.com/gbdx/). The analysis was run on an image focused on the Koumassi area of Abidjan. Different pan-sharpened WorldView-2 images can be selected and run by the user. A subscription is required to access DG imagery, though a 30 day trial was available for users at the time of writing (March 2019). 

To run this analyis, a user must update the area of interest parameter with the name of the imagery directory per instructions within the notebook (line 4). The user aoi imagery directory should contain pan-sharpened 8-band imagery TIF files from WorldView-2. 
# notebooks

## NDWI_MSI_with_modules
The 'NDWI_MSI_with_modules' notebook can be used to calculate the normalized difference water index (NDWI), morphological shadow index (MSI), normalized difference vegetation index (NDVI), and morphological building index (MBI). The notebook writes out each of these indices as a geoTIFF to a specified outputs folder. In addition to index calculations, the notebook also creates masks for each index based on user defined thresholds. Each mask is also written out as a geoTIFF. Finally, the notebook includes some experimentation and exploration with different formulations and analyses of NDWI and MSI. 

### customizable parameters

The analysis will run on any WV-2 image once the AOI and working directory have been appropriately defined. As each image may have individual features, the user may choose to customize input values within the notebook for the following:
- Definition/thresholds for the cloud mask (line 18)
- Definition/thresholds for the flood masks (line 30)
- Definition/thresholds for the NDWI masks (line 31)
- Thresholds/disk size for smoothing of flood and vegetation masks (line 34)
- Morphological shadow index (MSI) calculation inputs (line 40)
- Threshold for shadow mask (line 44)
- Morphological building index (MSI) calculation inputs (line 70)
- Threshold for building mask (line 73)

### outputs

Output rasters (geoTIFF format) will be placed into an "outputs/raster" directory located within the imagery directory. This directory is created within the notebook. 

## k-means_exploration and SVM_exploration

The 'k-means_exploration' and 'SVM_exploration' notebooks are working notebooks to explore how unsupervised and supervised learning might improve the workflow goal of differentiating building shadow from flood waters. 

### outputs

Output rasters (geoTIFF format) from the k_means_exploration notebook are placed into an "outputs/kmeans" directory within the imagery directory. Outputs include resulting rasters from k-means and Gaussian Mixture Model (GMM) algorithms. 

## Label_kmeans 
The 'Labeling_kmeans' notebook is a working notebook to explore the characteristics of the resulting kmeans clusters from the 'k-means exploration' notebook. The input to the 'Labeling_kmeans' notebook is the geoTIFF of the 8-cluster kmeans result. The notebook uses regionprops to define characteristics of different clusters compared to known reference points. The goal of the analysis is to redefine sub-clusters to separate building shadow and flood waters into unique clusters. 

# modules
Two modules were developed and are required to run the 'NDWI_MSI_with_modules' notebook. The first module, calc_array_mask, contains functions to define and apply a cloud mask to a single array or stack of arrays. The second module, morph_indices, provides functions to calculate MSI, MBI and reduce noise using morphological opening. 

# development environment
The notebooks were developed using Python 3.7.1 on a Windows system
