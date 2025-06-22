# Digitizing U.S. Tariffs, 1989-1996

This repo contains the code to digitize U.S. MFN and Column 2 tariffs between
1989 and 1996. Relative to Feenstra, Romalis, and Schott's version of the same
data, this version makes correction to products whose tariff rates are
a combination of ad valorem and specific. A more-complete comparison
of the two datasets is available [here](https://www.acostamiguel.com/data/HTS8996/HTS8996.pdf). 

The file `FRS.csv` contains the cleaned data. The paper
"[The Regressive Nature of the U.S. Tariff Code: Origins and Implications](https://www.acostamiguel.com/papers/regressive_tariffs.pdf)" 
by Miguel Acosta and Lydia Cox is the appropriate citation for these data. 

# Code overview 

## 1. Download PDF files

The file `pull.sh` in the directory folder `HTS8996` downloads all of the PDF files
used to construct the dataset. It is a Linux shell script, but it also contains
the URLs where the files can be found. If these URLs change, please let us know
and we can share the PDF files directly. 


## 2. Parse the PDFs 

The file `HTSPDF.py` in the `python` directory converts the PDFs into CSV files. 
It's designed to be run from the command line, one chapter and year at a time. 
The file `run_HTSPDF.py` is a shell script to do that. 
The files still contain the full text description of tariffs (e.g., 
$1.50 + 10%). 

## 3. Parse the tariffs

The file `HTSPDF_parse.py` in the `python` directory parses the tariff rates
and creates the final file. Note: this file relies on code to parse tariff
rates that we haven't added to this repo yet, but can share upon request. 
