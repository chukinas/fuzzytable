[![Documentation Status](https://readthedocs.org/projects/fuzzytable/badge/?version=latest)](https://fuzzytable.readthedocs.io/en/latest/?badge=latest)

# Overview
fuzzytable is a set of tools for extracting tabular data out of messy spreadsheets.

This library was developed to meet the needs of projects relying on spreadsheet data that has been handled by many people. Headers are often missing or mispelled. The data is incorrectly formatted. The table is on the wrong worksheet or you don't know the correct spreadsheet name. Etc...

fuzzytable allows you to quickly extract that data instead of arduously QC'ing the data ahead of time. After extraction, you can query the FuzzyTable attributes to e.g. determine which fields were found and how closely the desired header matches the actual header.

# Features
- Seek specific fields or extract them all. 
- Find the best-fit table from a specific sheet or anywhere in the spreadsheet.
- Set the header row or have fuzzytable find it.
- Normalize the data - either for the entire table or per field. (to be implemented...)
- Allow exact or approximate header matches.
- Enable or suppress exceptions for missing fields. 

# Documentation

- [readthedocs](https://fuzzytable.readthedocs.io/)  

# Supported Formats
- Excel (.xlsx, .xlsm, .xltx, .xltm)
- csv (.csv)

Basically, anything that can be read by the openpyxl or csv modules. 

# Installation

```powershell
# terminal
pip install fuzzytable
```

# Example Usage

```python
# python

from fuzzytable import FuzzyTable

path = 'path/to/excel/sheet.xlsx'
sheetname = 'worksheet name'
fields = ['first_name', 'last_name', 'birthday']
ft = FuzzyTable(
    path=path,
    sheetname=sheetname,
    fields=fields
)
```


