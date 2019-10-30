# Overview
EXCELerator is high-level, very configurable library for reading tabular data from Excel worksheets. It is a wrapper around the excellent openpyxl library

# Yet another library for reading from Excel!?
Yes. At the time of this library's authoring, excel readers fell into two camps:
- lower-level libraries like openpyxl and xlrd, which offer high functionality. But as a frequent Excel user, I found myself often rewriting the same code to perform the same tasks.
- simple libraries like excel2dict and excel2json
- middleware like django-excel and pyexcel whose focus is reading from and writing to excel.

The use case that none of these helped with was reading tabular data from excel forms that have been filled out by your coworkers. You know how this works. They're given a form to fill out, and by the time it gets back to you, it's been modified, even if slightly. Sometimes the header row gets displaced a few rows down or a few columns to the right. Sometimes a header is changed slightly - perhaps a whitespace was added to the end or a newline was inserted to make the header look nicer to the user.

Either way, by the time it got back to you, it changed *just enough* to throw a wrench into the pandas, openpyxl, or xlrd script you wrote. 

Up until now, you were forced to simply normalize each of these forms before reading the data. But now you can let EXCELerator do the heavy lifting.

# Future
The library current has a sparse set of features. But more are coming quickly.

# Tutorial
```powershell
pip install EXCELerator
```

```python
from excelerator import TableReader

path = r'path\to\excel\sheet.xlsx'
sheetname = 'worksheet name'
tr = TableReader()
my_table_as_dict = tr.read_from(path, sheetname)
```