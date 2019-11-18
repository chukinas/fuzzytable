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

>>> import fuzzytable
>>> ft = fuzzytable.FuzzyTable('birthdays.csv')
>>> [field.name for field in ft.fields]
['first_name', 'last_name', 'birthday']


Now let's extract the table using the field parameter. Note how the fields are in the same order as passed to FuzzyTable.

>>> ft = fuzzytable.FuzzyTable(
>>>     'birthdays.csv',
>>>     fields=['last name', 'first name'],
>>> )
>>> [field.name for field in ft.fields]
['last_name', 'first_name']
>>>

Because ``ft.fields`` is a list, you can sort it in place. See https://docs.python.org/3/howto/sorting.html for more details.

>>> from operator import attrgetter
>>> ft.fields.sort(key=attrgetter('col_num'))
>>> [field.name for field in ft.fields]
['first_name', 'last_name']

Finally, let's see how this works with MultiFields.

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
