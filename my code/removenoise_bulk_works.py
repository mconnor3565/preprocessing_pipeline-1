# -*- coding: utf-8 -*-
"""
@author: martin lo

Created on Fri May 20 11:42:30 2022

Saving the boolean'd array as pixel_array and pixeldata on the dcm itself
For loop allows all DCMs in the directory to be processed

"""
# Packages required
import pydicom
import copy
import numpy as np
import os
import matplotlib.pyplot as plt
from scipy import ndimage
from skimage import morphology

# Functions required
def transform_to_hu(medical_image, image):

    intercept = getattr(medical_image, 'RescaleIntercept', 0.0)
    print(intercept)
    slope = getattr(medical_image, 'RescaleSlope', 1.0)
    print(slope)
    hu_image = image * slope + intercept

    return hu_image

def window_image(image, window_center, window_width):
    img_min = window_center - window_width // 2
    img_max = window_center + window_width // 2
    window_image = copy.deepcopy(image) 

    window_image[window_image < img_min] = img_min
    window_image[window_image > img_max] = img_max 
    
    return window_image

def mask_only(file_path):
    medical_image = pydicom.dcmread(file_path, force=True)
    image = medical_image.pixel_array

    hu_image = transform_to_hu(medical_image, image)
    thresholded_image = window_image(hu_image, 40, 80)
    
    segmentation = morphology.dilation(thresholded_image, np.ones((4, 4)))
    labels, label_nb = ndimage.label(segmentation)
    array = labels
    # print(array)

    # array = array.astype(int)
    array = np.ravel(array)
    label_count = np.bincount(array)
    label_count[0] = 0

    mask = labels == label_count.argmax()
    
    # Improve the mask
    mask = morphology.dilation(mask, np.ones((1, 1)))
    mask = ndimage.binary_fill_holes(mask)
    mask = morphology.dilation(mask, np.ones((3, 3)))
   
    
    masked_image = mask * thresholded_image
    # fig, ax = plt.subplots(1,3, figsize=(15,5))

    # ax[0].imshow(thresholded_image, cmap='gray')
    # ax[0].set_title('Original Image')   
    # ax[0].axis('off')
    # ax[1].imshow(mask, cmap='gray')
    # ax[1].set_title('Mask')
    # ax[1].axis('off')
    # ax[2].imshow(masked_image, cmap='gray')
    # ax[2].set_title('Final Image')
    # ax[2].axis('off')
    # plt.show()

    return mask   


def mask_array(file_path):
    mask = mask_only(file_path)
    #print(mask)

    # Invert the bool array generated in mask_only function
    inverted_mask = np.logical_not(mask)
    # check inveted_mask array
    #print(inverted_mask)

    # turn inverted_mask into int array
    inverted_mask_int  = np.where(inverted_mask, 0, 1)
    # check inveted_mask_int array
    # print(inverted_mask_int)

    # find minimum value in dcm
    image = pydicom.dcmread(file_path)
    image = image.pixel_array
    minval = np.min(image)

    # replace _int 1s with min_img[0] aka minval
    new_mask = np.where(inverted_mask_int > 0, inverted_mask_int, minval)
    # print(new_mask)
    
    return new_mask

def boolean_masking(file_path):
    masking = mask_array(file_path)
    image = pydicom.dcmread(file_path).pixel_array
    n = np.min(masking)
    masking_value = (masking == n)
    image[masking_value] = masking[masking_value]
    
    # # Try Except Pass added 12/7/2022 to 'detect' corrupted files and skip over them, 
    # # print statement will provide the corrupted filepath/file folder in question
    # # the corrupted filepaths in question should be saved to the "corrupt.txt" file
    try:
        # Save into DCM
        print('entering bool mask try')
        CTimg = pydicom.dcmread(file_path)
        CTimg.set_pixel_data(image, photometric_interpretation= "MONOCHROME2", bits_stored =12)
        CTimg.save_as(file_path)
        print('out of the bool mask')
    except AttributeError:
        with open("corrupted.txt", "a") as corrupt_file:
            corrupt_file.write(str(file_path)+'\n')
            print(file_path + ' might be corrupted/ cannot be processed')
        corrupt_file.close()
        pass

    # plt.imshow(image)
    # plt.show()
        
    return image

# Function to avoid dcms that are not proper DICOM files readable image and metadata
def is_dicom_image(file: str) -> bool:
    # Boolean specifying if the file in question is a proper DICOM file with an image
    # The parameters 
    result = False
    try:
        img = pydicom.dcmread(file, force=True)
        if 'TransferSyntaxUID' not in img.file_meta:
            img.file_meta.TransferSyntaxUID = pydicom.uid.ImplicitVRLittleEndian
        img.pixel_array
        result = True
    except (AttributeError, TypeError, KeyError):
        with open("notproper.txt", "a") as proper_file: 
            proper_file.write(str(file)+'\n')  
            print(file + ' is not a proper DICOM file')
        proper_file.close()
        pass
    return result

# The below forloop should run in the directory housing all the DCMs
external_drive_path= r"C:\Users\mmconno2\NMDIDstage1\USB DISK\case-133799\case-133799\THIN_BONE_HD-UXT\series_6\series_6 - Copy"
file_list = list()
file_notdcm = list()
path_list = list()

for root, dirs, files in os.walk(external_drive_path):
    for name in files:
        if name.lower().endswith('.dcm'):
            file_list.append(os.path.join(root, name))
            #print(file_list)
        else:
            file_notdcm.append(os.path.join(root,name))
            # print(file_notdcm)     
            
print(file_list)
# Removes dcm files that do not have metadata and will cause the boolean masking loop to interrupt
# from the list of paths which will be passed through the boolean_masking function
for path in file_list:
    x = is_dicom_image(path)
    if x == True:
        path_list.append(path)
print(path_list)
# Does the boolean masking and removes the bed
for path in path_list[:]:
      # file_size = os.path.getsize(path)
      # if file_size == 0:
      #     continue
      # else:
          boolean_masking(path)
  #prints path done
          #print(path + ' done')
print(path_list)
  	
