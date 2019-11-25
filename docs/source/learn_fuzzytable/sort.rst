.. _tutsort:

Field Sorting
---------------------------------------

Summary
+++++++++++++++++++++++++++++++++++++++

- By default, ``ft.fields`` provides a list sorted by column number in ascending order.
- If you passed a sequence of desired fields (``FuzzyTable(fields=...)``), the ``ft.fields`` fields will be sorted in the same order.
- :obj:`~fuzzytable.datamodel.MultiField` subfields are sorted by column number

Details
+++++++++++++++++++++++++++++++++++++++

Let's read the following csv file.

=========== =========== ============
first_name  last_name   birthday
=========== =========== ============
John        Doe         3-Mar-85
Typhoid     Mary        2-Aug-83
Jane        Smith       23-Oct-46
=========== =========== ============

Let's extract this table using all the default settings.
Notice how ``ft.fields`` returns the three fields in the same order they appear in the spreadsheet.


>>> import fuzzytable
>>> ft = fuzzytable.FuzzyTable('birthdays.csv')
>>> [field.name for field in ft.fields]
['first_name', 'last_name', 'birthday']


But now let's extract the table using the ``field`` parameter.
Notice now how ``ft.fields`` returns the fields in the order as passed to FuzzyTable.

>>> ft = fuzzytable.FuzzyTable(
>>>     'birthdays.csv',
>>>     fields=['last name', 'first name'],
>>> )
>>> [field.name for field in ft.fields]
['last_name', 'first_name']
>>>

But what if you don't want them in that order?
What if you'd prefer to have them sorted in the order they appear in the spreadsheet? Easy.
Because ``ft.fields`` is a list, you can sort it in place. See https://docs.python.org/3/howto/sorting.html for more details.

>>> from operator import attrgetter
>>> ft.fields.sort(key=attrgetter('col_num'))
>>> [field.name for field in ft.fields]
['first_name', 'last_name']

The subfields collected by a ``multifield=True FieldPattern`` are stored in spreadsheet order.
The ``col_num`` of a ``multifield FieldPattern`` is equal to the smallest ``col_num`` of its subfields.

>>> names = fuzzytable.FieldPattern(
>>>     name='names',
>>>     alias=['last name', 'first name'],
>>>     multifield=True,
>>>     approximate_match=True,
>>> )
>>>
>>> ft = fuzzytable.FuzzyTable(
>>>     'birthdays.csv',
>>>     fields=[names, 'birthday'],
>>> )
>>>
>>> [field.name for field in ft.fields]
['names', 'birthday']
>>> namesfield = ft.get_field('names')
>>> namesfield.headers
['first_name', 'last_name']
>>> # Note that these are in their original table order, not the alias order.
