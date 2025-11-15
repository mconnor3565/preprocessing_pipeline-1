# -*- coding: utf-8 -*-
"""
S1.1: datacleaning.py

This script (part of S1) allows you to catch corrupted files through the is_dicom_image function
    The function appends corrupted file paths to a list (notproper.txt), which is then removed from the entire directory 
    using a for-loop and the delete_corrupt function

@author: m3lo4
"""
## packages required
import os
import time
import pydicom
import pandas as pd
from pathlib import Path


def is_dicom_image(file: str) -> bool:
    # Boolean specifying if the file in question is a proper DICOM file with an image
    result = False
    try:
        img = pydicom.dcmread(file, force=True)
        if 'TransferSyntaxUID' not in img.file_meta:
            img.file_meta.TransferSyntaxUID = pydicom.uid.ImplicitVRLittleEndian
        img.pixel_array
        result = True
    except (AttributeError, TypeError, KeyError, ):
        with open("notproper.txt", "a") as proper_file: 
            proper_file.write(str(file)+'\n')  
            print(file + ' is not a proper DICOM file')
            if os.path.exists(file):
                try:
                    os.remove(file)
                    print ('removing file:', file)
                except Exception as e:
                    print('Error while deleting file:', file, e)
            else:
               print('The file does not exist:', file)      
        proper_file.close()

        pass
    return result

external_drive_path= r'C:\Users\mmconno2\NMDIDstage1\USB DISK'
for root, dirs, files in os.walk(external_drive_path):
       for file in files:
            file_path = os.path.join(root, file)
            is_dicom_image(file_path)

