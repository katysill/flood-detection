# Flood Detection Workflow

This repository is for a research project focused on improving urban flood detection with a focus on differentiating building shadow from flood waters. The workflow is motivated by the challenges in rapidly and accurately assessing flooding extent utilizing high resolution remote sensing imagery, as shadows from buildings look spectrally similar to water. 

The repository provides code for running three different approaches for identifying floods from DigitalGlobe's WorldView-2 imagery. The three approaches include: thresholding spectral indices, applying supervised machine learning methods and applying unsupervised machine learning methods. Each of the three approaches can be found in the following notebooks:

- Thresholding spectral indices: final_calculating_spectral_indices_koumassi.ipynb and final_calculating_spectral_indices_southeast.ipynb
- Supervised machine learning: final_supervised_ML_SVM_random_forest_combined.ipynb
- Unsupervised machine learning: final_unsupervised_ML_kmeans_GMM_koumassi.ipynb and final_unsupervised_ML_kmeans_GMM_southeast.ipynb

Note that the machine learning notebooks rely on inputs from final_calculating_water_shadow_indices.ipynb

Additional "explorations" notebooks have been included showing more of the process completed to finalize each of the supervised and unsupervised models. Note that the explorations notebooks rely on inputs from final_calculating_water_shadow_indices.ipynb

# Input Data Required

The notebooks were developed using WorldView-2 pan sharpened 8-band geoTIFF files for a flooding event in Abidjan, Ivory Coast on June 17, 2016. Imagery data was accessed using DigitalGlobe's [GBDX portal](https://platform.digitalglobe.com/gbdx/). The analysis was run on an image focused on the Koumassi area of Abidjan. Different pan-sharpened WorldView-2 images can be selected and run by the user. A subscription is required to access DG imagery, though a 30 day trial was available for users at the time of writing (March 2019). 

To validate models, a reference data set is required. Reference data should include known land cover class values for reference points in a CSV format and a shapefile for all reference points. 

To run this analyis, a user must update the area of interest parameter with the name of the imagery directory per instructions within the notebook (line 4). The user aoi imagery directory should contain pan-sharpened 8-band imagery TIF files from WorldView-2. 

# Development Environment
The notebooks were developed using Python 3.7.1 on a Windows system. The workflow utilizes packages from NumPy, Matplotlib, scikit-image, scikit-learn, RasterIO, and EarthPy. The workbook was developed using the [earth-analytics-python environment](https://github.com/earthlab/earth-analytics-python-env)

# Notebooks

Notebooks are named with a tag of "final" or "explorations". "Final" notebooks represent the workflow used to develop the finalized workflow and results which are presented in the Out_of_the_Shadows_Blog.ipynb and Flood_Detection_Project_Summary.ipynb notebooks. The final workflow was developed after using the explorations notebooks to identify parameters such as appropriate thresholds and ideal model inputs. 

## Flood detection via Calculation of Spectral Metrics

### Notebook names: 
* final_calculating_spectral_indices_koumassi.ipynb
* final_calculating_spectral_indices_southeast.ipynb

These notebook calculates spectral indices including the normalized difference water index (NDWI), morphological shadow index (MSI), normalized difference vegetation index (NDVI), and morphological building index (MBI). In addition to index calculations, the notebooks also defines masks for each index based on user defined thresholds.The notebooks combines the four masks into a resulting threshold map with identified areas of flood, shadow, vegetation and buildings. Additionally the accuracy score and confusion matrix are calculated using a reference data set. 

#### outputs
Output spectral index rasters (geoTIFF format) will be placed into  "../final_outputs/raster_files/" directory located within the area of interest imagery directory. This directory is created within each notebook. The notebooks write out each of the individual spectral indices as a geoTIFF to the specified outputs folder. Output thresholding results will be placed in "../explorations_outputs/threshold/" directory located within the imagery director. Each mask and the combined thresholded map is also written out as a geoTIFF. 

Thresholding results are places in a "../final_outputs/threshold/" directory located within the area of interest imagery directory. The thresholded map is written out as a geoTIFF. The confusion matrix is output as a CSV file. 

### Notebook name: explorations_calculating_spectral_indices.ipynb

In addition to the summary described above for the final notebooks, the explorations notebook includes additional experimentation and exploration with different formulations and analyses of NDWI and MSI. The explorations notebook includes additional plots and visualizations compared with the final versions. Also, code is included to create and apply a cloudmask to the 8-band raster stack, followed by the calculation of spectral indices for the cloud  masked image. This cloud mask was not needed for the final areas of interest (Koumassi and Southeast) selected for the research study. 

#### outputs
Output index rasters (geoTIFF format) will be placed into a "../explorations_outputs/raster_files/" directory located within the imagery directory. Output thresholding results will be placed in "../explorations_outputs/threshold/" directory located within the imagery directory. These directories are created within the notebook.

### modules
Two modules were developed and are required to run the 'calculating_spectral_indices' notebooks. The first module, calc_array_mask, contains functions to define and apply a cloud mask to a single array or stack of arrays. The second module, morph_indices, provides functions to calculate MSI, MBI and reduce noise using morphological opening. 

### customizable parameters for calculating_spectral_indices notebooks

The analysis will run on any WV-2 image once the area of interest has been appropriately defined. As each image may have individual features, the user may choose to customize input values within the notebook. Customizable parameters are indicated in markdown within the notebook. Some of the customizable parameter include: 

- Definition/thresholds for the cloud mask 
- Definition/thresholds for the flood masks 
- Definition/thresholds for the NDWI masks 
- Thresholds/disk size for smoothing of flood and vegetation masks 
- Morphological shadow index (MSI) calculation inputs 
- Threshold for shadow mask 
- Morphological building index (MSI) calculation inputs 
- Threshold for building mask 


## Flood detection via Supervised Machine Learning

### Notebook name: 
* final_supervised_ML_SVM_RandomForest_combined.ipynb

This notebook samples shapefiles for both the Koumassi and Southeast areas of interest to collect spectral band and index values at reference points. The notebook combines the raw spectral information with the reference class values to create a training data set for each site. The training data sets for each site are combined in a pandas dataframe to create a combined training data set. The combined data set is split into a training/testing set (60% of total) and an external validation set (40% of total). A linear kernel SVM model is then trained and tested, and the user can select the model with the best accuracy score to write out for later use. The accuracy score and confusion matrix is plotted for the final trained model. The final model is then applied to the external validation data set, along with the accuracy score and confusion matrix. Finally, the model is applied to each area of interest and plot of the result is created. The same process is then followed for the training/testing, external validation and plotting using the random forest classifier.

### Model inputs include the following spectral bands/indices: 
Model inputs were determined after substantial trial and error testing with a variety of spectral bands and indices.
* summation of NIR1, NIR2 and RE bands
* morphological building index (MBI)
* morphological shadow index (MSI)
* normalized difference vegetation index (NDVI)
* normalized difference water index (NDWI coastal/NIR2)
* the difference between NDWI and MSI (NDWIcoastal/NIR2 - MSI)
* normalized difference water index (NDWI yellow/NIR2)
* the difference between NDWI and MSI (NDWIyellowNIR2 - MSI)

### Outputs
All outputs are written out to a "../../combined/" directory. The directory is created within the code. The raw index values for each sample point, along with the internal and external data sets are written out as CSV files for backup purposes. Confusion matrices are  saved as CSV files. Pickled SVM and random forest classifiers are also saved for later use. 


## Flood detection via Unupervised Machine Learning

### Notebook names:
* final_unsupervised_ML_accuracy_scores_koumassi.ipynb
* final_unsupervised_ML_accuracy_scores_southeast.ipynb

These notebooks apply the k-means clustering algorithm to the 8-band raster stack for each image. The accuracy score and confusion matrices for both the entire reference data set and a flood-only focused data set are calculated. 

### Outputs

All outputs are saved in the "../final_outputs/kmeans/" directory. The resulting k-means cluster map is written out as a geoTIFF file and the confusion matrices as CSV files. 

### Notebook names: 
* explorations_unsupervised_ML_kmeans-gmm_koumassi.ipynb
* explorations_unsupervised_ML_kmeans-gmm_southeast.ipynb

These two 'explorations' notebooks explore different options for inputs into the k-means model. Options explored include the 8-band raster stack, stacks of spectral indices and various other combinations. 

### Outputs

All outputs are saved in the "../explorations_outputs/kmeans/" directory. The resulting k-means cluster maps are written out as geoTIFF files.

## Applying machine learning approaches to a new location: Beira, Mozambique
The trainined SVM and random forest models were applied to a flooded image from Beira, Mozambique from March 2019. This is an extension of the primary project and is a work in progress. 

### Notebook names:
explorations_calculating_spectral_indices_beira.ipynb
explorations_supervised_ML_SVM_Random_Forest_applying_to_beira.ipnyb
explorations_unsupervised_ML_kmeans_gmm_beira.ipynb

All outputs are the same as those described above for the final workflow. Outputs are placed in an /../explorations_outputs/ directory. 

# References
- Cloud to Street. Urban Flood Mapping Using Very-High Resolution Satellite Imagery. Available at: https://abidjan.cloudtostreet.info/info

- Huang, X., Xie, C., Fang, X., Zhang, L. (2015) Combining Pixel-and Object-Based Machine Learning for Identification of Water-Body Types from Urban High-Resolution Remote-Sensing Imagery. IEEE J. Sel. Top. Appl. Earth Obs. Remote Sens. 8, 2097–2110.

- Huang, X., and Zhang, L. (2012) Morphological Building/Shadow Index for Building Extraction From High-Resolution Imagery Over Urban Areas. IEEE J. Sel. Top. Appl. Earth Obs. Remote Sens. 5, 161-172.

- McFeeters, S.K. (1996) The use of the Normalized Difference Water Index (NDWI) in the delineation of open water features, International Journal of Remote Sensing, 17:7, 1425-1432, DOI: 10.1080/01431169608948714

- United Nations Office for Disaster Risk Reduction (UNISDR) and Centre for Research on the Epidemiology of Disasters (CRED) (2018). Economic losses, poverty & disasters: 1998-2017. Available at: https://www.preventionweb.net/files/61119_credeconomiclosses.pdf

- Xie, C., Huang, X., Zeng, W., & Fang, X. (2016). A novel water index for urban high-resolution eight-band WorldView-2 imagery. International Journal of Digital Earth, 9(10), 925–941.

- Xu, H. (2006). Modification of normalised difference water index (NDWI) to enhance open water features in remotely sensed imagery. International Journal of Remote Sensing. Vol. 27, No. 14, 3025–3033.
