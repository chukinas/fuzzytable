# Overview
EXCELerator is high-level, configurable library for reading tabular data from Excel worksheets.
It is a wrapper around the excellent openpyxl library.

# Use Case
The primary use case for EXCELerator is for reading data from excel 
forms that were filled out by someone other than yourself. If you're ever had
to do this, you'll recognize the following issues: 
- The worksheet does not the right name.
- The headers are in the wrong place (displaced down and/or to the right or in the wrong order)
- The headers are slightly modified (maybe whitespace or a new line characters added for aesthetics)
- Entire fields are missing. Or there are extra fields.

Whatever the changes - by the time it got back to you, the Excel form has changed *just enough* 
to throw a wrench into the pandas, openpyxl, or xlrd script you wrote. 
At this point, you could quality check each form manually. But this is arduous and error prone.

Or you could do the heavy lifting using EXCELerator's 
TableParser, FieldParser, WorksheetParser, and Normalize classes:
- Specificy the field names you expect to find
- Allow approximate field matches.
- Allow or suppress exceptions for missing fields or worksheets.
- Set the headers row number or have EXCELerator find the header row.  
- Normalize data per field or for the entire table
- Read data as a collection of records (i.e. rows) or fields (i.e. columns)  

This is just a small sampling of EXCELerator fuctionality. 
See [the documentation](https://excelerator.readthedocs.io/) for full details.  

# Basic Usage
```powershell
pip install EXCELerator
```

```python
from excelerator import TableParser

path = r'path\to\excel\sheet.xlsx'
sheetname = 'worksheet name'
tr = TableReader()
my_table_as_dict = tr.get_fields(path, sheetname)
```

# A Work in Progress
The library currently has a sparse set of features. More are coming quickly.
