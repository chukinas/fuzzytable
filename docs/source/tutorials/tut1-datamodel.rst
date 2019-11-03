.. _tutdatamodel:

Tutorial 1: The Data Model
--------------------------

Let's read the following csv file.

=========== =========== ============
first_name  last_name   birthday
John        Doe         3-Mar-85
Typhoid     Mary        2-Aug-83
Jane        Smith       23-Oct-46
=========== =========== ============

>>> import fuzzytable
>>> ft = fuzzytable.FuzzyTable('birthdays.csv')

.. _datamodel-fuzzytable:

Data View 1: ``FuzzyTable`` as dictionary
+++++++++++++++++++++++++++++++++++++++++++++++++++

A ``FuzzyTable`` object behaves like a dictionary, where keys are field names and values are lists of column values:

>>> keys = ft.keys()
>>> list(keys)
['first_name', 'last_name', 'birthday']
>>> for col in ft.values():
...     print(col)
...
['John', 'Typhoid', 'Jane']
['Doe', 'Mary', 'Smith']
['3 March 1985', '2 Aug 1983', '23 Oct 1946']

Loop through first names:

>>> for first_name in ft['first_name']:
...     print(first_name)
John
Typhoid
Jane

See the :obj:`fuzzytable.FuzzyTable` API Reference for more details.

Data View 2: ``FuzzyTable.records`` - list of rows as dictionaries
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

``FuzzyTable``'s ``records`` attribute is a sequence of dictionaries each representing a row of data.

>>> ft.records[1]
{'first_name': 'Typhoid', 'last_name': 'Mary', 'birthday': '2-Aug-83', 'row': 3}

Note that a ``'row'`` key was automatically included.
You can change this behavior via the ``include_row_num`` property:

>>> ft.records.include_row_num = False
>>> for record in ft.records:
...     print(record)
...
{'first_name': 'John', 'last_name': 'Doe', 'birthday': '3-Mar-85'}
{'first_name': 'Typhoid', 'last_name': 'Mary', 'birthday': '2-Aug-83'}
{'first_name': 'Jane', 'last_name': 'Smith', 'birthday': '23-Oct-46'}

See the :obj:`fuzzytable.datamodel.Records` API Reference for more details.

Data View 3: ``FuzzyTable.fields`` - list of ``Field`` objects
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

``FuzzyTable``'s ``fields`` attribute is a list of ``Field`` objects which contain field name, data, and additional metadata e.g. column number.

>>> fields = ft.fields
>>> first_name = fields[0]
>>> first_name.col_num
1
>>> first_name.data
['John', 'Typhoid', 'Jane']
>>> str(first_name)
"<Field 'first_name' 0x10dcce8>"

See the :obj:`fuzzytable.datamodel.Field` API Reference for more details.

Data View 4: ``FuzzyTable.sheet`` - spreadsheet metadata
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

``FuzzyTable``'s ``sheet`` attribute contains metadata about the sheet itself (path, header row number, number of rows):

>>> sheet = ft.sheet
>>> sheet.header_row_num
1
>>> sheet.row_count
4
>>> sheet.path
WindowsPath('birthdays.csv')

See the :obj:`fuzzytable.datamodel.Sheet` API Reference for more details.

Go back to :ref:`top of page<tutdatamodel>`
