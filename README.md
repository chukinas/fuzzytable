![Logo](https://raw.githubusercontent.com/jonathanchukinas/fuzzytable/master/docs/source/_static/logo.png "fuzzytable logo")

[![Travis (.com)](https://img.shields.io/travis/com/jonathanchukinas/fuzzytable)](https://travis-ci.com/jonathanchukinas/fuzzytable)
[![Codecov](https://img.shields.io/codecov/c/github/jonathanchukinas/fuzzytable)](https://codecov.io/gh/jonathanchukinas/fuzzytable)
[![Read the Docs](https://img.shields.io/readthedocs/fuzzytable)](https://fuzzytable.readthedocs.io/)
[![PyPI](https://img.shields.io/pypi/v/fuzzytable)](https://pypi.org/project/fuzzytable/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/fuzzytable)](https://github.com/jonathanchukinas/fuzzytable/blob/master/tox.ini)
[![PyPI - Wheel](https://img.shields.io/pypi/wheel/fuzzytable)](https://pypi.org/project/fuzzytable/#modal-close)
[![GitHub last commit](https://img.shields.io/github/last-commit/jonathanchukinas/fuzzytable)](https://github.com/jonathanchukinas/fuzzytable/commits/master)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/fuzzytable)](https://pypistats.org/packages/fuzzytable)

fuzzytable is a set of tools for extracting tabular data out of messy spreadsheets.

This library meets the needs of projects relying on spreadsheet data that has been handled by many people.
Headers are often missing or misspelled. 
The data is incorrectly formatted.
The table is on the wrong worksheet or you don't know the correct spreadsheet name. Etc...

fuzzytable allows you to quickly extract that data instead of arduously QC'ing the data ahead of time.
After extraction, you can inspect the FuzzyTable attributes to e.g. determine
which fields were found and how closely the desired header matches the actual header.

# Installation

```shell
pip install fuzzytable
```

# Example Usage

Here's a light-hearted demo. To read this messy file using, say, the csv module, we'd have to first:
- Delete rows 1 and 2.
- Delete columns A and B.
- Rename the headers. 

| A         | B 	| C          	| D      	    | E 	|
|----------	|-----	|------------	|----------	    |--------	|
| These    	| are 	| not        	| the      	    | droids 	|
| you      	| are 	| looking    	| for.     	    | He     	|
| can      	| go  	| c o l o r     | first name 	| GivenName	|
| about    	| his 	| Gold   	    | C          	| 3PO      	|
| business 	| .   	| Blue   	    | R2         	| D2       	|

Let's instead leverage the FuzzyTable class.

```bash
>>> from fuzzytable import FuzzyTable

>>> droids = FuzzyTable(
...     path='droids.csv',
...     fields=['first_name', 'last_name', 'color'],
...     approximate_match=True,
...     min_ratio=.3
... )
```

Now let's play with the data we've extracted.

```bash
>>> droids['color']
['Gold', 'Blue']

>>> for droid in droids.records:
...     print(f"{droid['first_name']}-{droid['last_name']} is {droid['color']}.")
C-3PO is Gold.
R2-D2 is Blue.

>>> droids.fields['first_name'].col_num
3

>>> droids.sheet.header_row
2
```

# Links

- Documentation (tutorials, etc): [fuzzytable.readthedocs.io](https://fuzzytable.readthedocs.io/)
- PyPI: [pypi.org/project/fuzzytable](https://pypi.org/project/fuzzytable/)
- github: [github.com/jonathanchukinas/fuzzytable](https://github.com/jonathanchukinas/fuzzytable)
- Submit issues: [github.com/jonathanchukinas/fuzzytable/issues](https://github.com/jonathanchukinas/fuzzytable/issues)

# Supported Formats
- Excel (.xlsx, .xlsm, .xltx, .xltm)
- csv (.csv)

Basically, anything that can be read by the openpyxl or csv modules. 
