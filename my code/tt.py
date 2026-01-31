import pydicom
import numpy as np
import os
import matplotlib.pyplot as plt
from scipy import ndimage
from skimage import morphology

# external_drive_path= r'C:\Users\mmconno2\NMDIDstage1\USB DISK\case-100335\omi\incomingdir\case-100335\STANDARD_HEAD-NECK-U-EXT\BONE_H-N-UXT_3X3'
# file_list = list()
# file_notdcm = list()
# path_list = list()

#for root, dirs, files in os.walk(external_drive_path):
    # for name in files:
    #     if name.lower().endswith('.dcm'):
    #         file_list.append(os.path.join(root, name))
    #         #print(file_list)
    #     else:
    #         file_notdcm.append(os.path.join(root,name))
    #         # print(file_notdcm)     
            
#print(file_list)
#reading a dcm file
ds= pydicom.dcmread(r'C:\Users\mmconno2\NMDIDstage1\USB DISK\case-134040\case-134040\THIN_BN_H-N-UEXT - Copy\CT.1.2.840.113704.1.111.536.1453138002.71356.dcm')

print(ds)

#step 1 find out pixel dim to calc the area in mm^2
