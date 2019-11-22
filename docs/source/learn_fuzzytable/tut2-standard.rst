.. _tutstandard:

--------------------------
Standard Usage
--------------------------

- You know which fields you want.(list of strings)
- You don't know where (which col, which rows) they are

=========   =========   =========   =========== =========== ============
These       are         not
the
droids
you                                 first_name  last_name   birthday
are                                 John        Doe         3-Mar-85
looking                             Typhoid     Mary        2-Aug-83
for.                                Jane        Smith       23-Oct-46
=========   =========   =========   =========== =========== ============

Instantiate a fuzzy table:

>>> tf = fuzzy_table.FuzzyTable(
...     fields='first_name last_name birthday'.split()
...     path='path/to/excel.xslx'
...     sheetname='name of my worksheet',
... )

