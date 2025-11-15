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
        with open("notproper1.txt", "a") as proper_file: 
            proper_file.write(str(file)+'\n')  
            print(file + ' is not a proper DICOM file')
        proper_file.close()

        pass
    return result

external_drive_path= r'C:\Users\mmconno2\NMDIDstage1\USB DISK'
for root, dirs, files in os.walk(external_drive_path):
    for dir in dirs:
       for file in files:
            file_path = os.path.join(root, file)
            is_dicom_image(file_path)


def delete_notdcm(directory_path):
    st = time.time()
    
    directory_path=os.getcwd()

    file_notdcm = []
    
    # load the txt list from is_dicom_image to for-loop below
    
    for root, dirs, files in os.walk(directory_path):
            for name in files:
                if name.lower().endswith('notproper1.txt'):
                    txt_file = open('notproper1.txt', 'r')
                    file_notdcm = txt_file.readlines()
                    txt_file.close()                
        
    for file in file_notdcm:
        if os.path.exists(file):
            try:
                os.remove(file)
                print ('removing file:', file)
            except Exception as e:
                print('Error while deleting file:', file, e)
        else:
            print('The file does not exist:', file)      

       #os.remove(file)
    et = time.time()
    elapsed_time = et - st
    print('deleting corrupt files took:', elapsed_time, 'seconds')

clean_out= r'C:\Users\mmconno2\preprocessing\preprocessing_pipeline'
delete_notdcm(clean_out)