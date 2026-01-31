import pydicom
import numpy as np
import copy
import os
import matplotlib.pyplot as plt
from scipy import ndimage
from skimage import morphology
external_drive_path= r"C:\Users\mmconno2\NMDIDstage1\USB DISK\case-128925\case-128925\THIN_BN_H-N-UEXT - Copy\CT.1.2.840.113704.1.111.2180.1342725570.113187.dcm"


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
    fig, ax = plt.subplots(1,3, figsize=(15,5))

    ax[0].imshow(thresholded_image, cmap='gray')
    ax[0].set_title('Original Image')   
    ax[0].axis('off')
    ax[1].imshow(mask, cmap='gray')
    ax[1].set_title('Mask')
    ax[1].axis('off')
    ax[2].imshow(masked_image, cmap='gray')
    ax[2].set_title('Final Image')
    ax[2].axis('off')
    plt.savefig('DICOM_MaskImage.png', bbox_inches='tight', pad_inches=0)
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
    # try:
    #     # Save into DCM
    #     print('entering bool mask try')
    #     CTimg = pydicom.dcmread(file_path)
    #     CTimg.set_pixel_data(image, photometric_interpretation= "MONOCHROME2", bits_stored =12)
    #     CTimg.save_as(file_path)
    #     print('out of the bool mask')
    # except AttributeError:
    #     with open("corrupted.txt", "a") as corrupt_file:
    #         corrupt_file.write(str(file_path)+'\n')
    #         print(file_path + ' might be corrupted/ cannot be processed')
    #     corrupt_file.close()
    #     pass

    plt.imshow(image)
    plt.show()
        
    return image
boolean_masking(external_drive_path)