import os
import time
import pydicom
import pandas as pd


external_drive_path= r'C:\Users\mmconno2\NMDIDstage1\USB DISK'
# Walk through the directory and remove empty folders
# the folders are sorted into a list by listing all the paths in the directory, it is sorted from smallest to largest,
# hence the reverse = True condition.
folders = sorted(list(os.walk(external_drive_path))[:-1], reverse = True)
for folder in folders:
# for folder in the sorted list 'folders', remove directory of the smallest folder, hence folder[0], the item listed in the 0th position is the smallest
    try:
        os.rmdir(folder[0])
    except OSError as error:
# this stops the os.rmdir as os.rmdir only remvoes empty folders, if a folder with files is passed through os.rmdir, error will be returned
        print("Directory '{}' contains files".format(folder[0]))