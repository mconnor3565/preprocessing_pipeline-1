import pydicom
import os
import shutil

external_drive_path= r'C:\Users\mmconno2\NMDIDstage1\USB DISK\case-100335\omi\incomingdir\case-100335\STANDARD_HEAD-NECK-U-EXT\COR_BONE_TORSO'
extension = "*.dcm"
patientpaths = []
dicompaths = []
def dcms (filename, extension = ['*.dcm']):
    return any(filename.endswith('.dcm') for e in extension)


for root, dirs, files in os.walk(external_drive_path):
    for filename in filter(dcms, files):
        patientpaths.append(os.path.abspath(root))

for root, dirs, files in os.walk(external_drive_path):
    for filename in filter(dcms, files):
        dicompaths.append(os.path.join(root, filename))


# removes duplicates from paths
# set() removes duplicates from list
# ptpaths is list of paths to the CT folder of the Patient folder
ptpaths = set(patientpaths)
print(len(ptpaths))
# print(ptpaths)
# dicompaths is the list of paths to each dicom file
print(len(dicompaths))


for file in dicompaths:
    dicom_data = pydicom.dcmread(file)
    series_number = dicom_data.get('SeriesNumber', None)
    series_string = f"series_{series_number}"
    filepath = '\\'.join(file.split('\\')[:-1]) + '\\' + series_string
    if not os.path.exists(filepath):
        os.makedirs(filepath)
        shutil.move(file, filepath)
filn=r'C:\Users\mmconno2\NMDIDstage1\USB DISK\case-100335\omi\incomingdir\case-100335\STANDARD_HEAD-NECK-U-EXT\COR_BONE_TORSO\CT.1.2.840.113704.7.1.1.9084.1457366555.194.dcm'
dicom_data = pydicom.dcmread(filn)
print(dicom_data)
ds = dicom_data.PixelData
                        