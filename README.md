## MDRF CSV Occurrence Extractor

This utility is used for extracting event occurrences from a csv file generated 
from an MDRF (Mosaic Data Recording Format) file. Event occurrences can be
recorded using MosaicLib's MDRFRecordingEngine. Source of this can be found at
https://github.com/mosaicsys/MosaicLibCS.

#### Usage
First, you must extract the original MDRF file to CSV, using Mosaic's ExtractMDRFtoCSV
tool. The -io flag must be set to include occurrences in the product's CSV
file. After this, you are ready to extract the occurrences.

You may specify the -d flag to delete the occurrences in the input file, after
extracting to the output file. 
``` bash
$ extract_occurrences.py [-d] in.csv out.csv
```
