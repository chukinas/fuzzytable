# EXCELerator

## Use Case
Excel is often used to generator forms. Those forms are sometimes modified, even if slightly. Sometimes the header row gets displaced a few rows down or a few columns to the right. Sometimes a header is changed slightly - perhaps a whitespace was added to the end or a newline was inserted to make the header look nicer to the user.

Either way, by the time it got back to you, it changed *just enough* to throw a wrench into the pandas, openpyxl, or xlrd script you wrote. 

This library seeks to aide you in reading the content of such forms by providing you with high-level classes and functions for reading data out of excel sheets.

## Future
Currently, this is a barebones library. But more feature will come quickly.

## Tutorial
```powershell
pip install EXCELerator
```

```python
from excelerator import TableReader

path = 'path\to\excel\sheet.xlsx'
sheetname = 'worksheet name'
tr = TableReader()
my_table_as_dict = tr.read_from(path, sheetname)
```