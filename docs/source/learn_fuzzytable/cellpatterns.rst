.. _tutcellpatterns:

---------------------------------------
Cell Patterns
---------------------------------------

:ref:`Cell patterns<apicellpatterns>` allow you to normalize the data on a per-field basis.

fuzzytable Built-Ins
+++++++++++++++++++++++++++++++++++++++

Let's say you have this very simple table:

=========== ========
Name        DOB
=========== ========
John Doe    1995
123         2003OCt
Jane Doe    1964
True        2019
=========== ========

You want to ensure the first field (Name) returns only strings and the
Birthday column returns integers.

.. code-block:: python

    # birthdays.py

    from fuzzytable import FuzzyTable, FieldPattern, cellpatterns

    name_field = FieldPattern(
        name="name",
        alias="Name",
        cellpattern=cellpatterns.String,
    )

    birthday_field = FieldPattern(
        name="birthday",
        alias="DOB",
        cellpattern=cellpatterns.Integer,
    )

    birthday_table = FuzzyTable(
        path='birthdays.csv',
        fields=[name_field, birthday_field],
    )


>>> python birthdays.py
>>> for record in birthday_table.records
...     print(record)
...
{'name': 'John Doe', 'birthday': 1995}
{'name': '123', 'birthday': 2003}
{'name': 'Jane Doe', 'birthday': 1964}
{'name': '', 'birthday': 2019}

Custom Callables
+++++++++++++++++++++++++++++++++++++++

You're not limited to the :ref:`built-in cell patterns<apicellpatterns>` provided by fuzzytable.
You can also create your own.

In this example, we'll return the type of the variable in the ``Name`` column.

.. code-block:: python

    # birthdays_customcallable.py

    from fuzzytable import FuzzyTable, FieldPattern, cellpatterns

    # This is new
    def value_type(value):
        return type(value)

    name_field = FieldPattern(
        name="name",
        alias="Name",
        cellpattern=value_type,  # This is new.
        # Note that we don't call the function here.
    )

    birthday_field = FieldPattern(
        name="birthday",
        alias="DOB",
        cellpattern=cellpatterns.Integer,
    )

    birthday_table = FuzzyTable(
        path='birthdays.csv',
        fields=[name_field, birthday_field],
    )


>>> python birthdays_customcallable.py
>>> for record in birthday_table.records
...     print(record)
...
{'name': <class 'str'>, 'birthday': 1995}
{'name': <class 'int'>, 'birthday': 2003}
{'name': <class 'str'>, 'birthday': 1964}
{'name': <class 'bool'>, 'birthday': 2019}

Piping
+++++++++++++++++++++++++++++++++++++++

You can also string multiple cell patterns together.
Here we'll pipe the :obj:`~fuzzytable.cellpatterns.String` output into a custom ``first_char`` function.

.. code-block:: python

    # birthdays_piping.py

    from fuzzytable import FuzzyTable, FieldPattern, cellpatterns

    # This is new
    def first_char(value):
        # Because we are piping the output of cellpattern.String
        # to this function, value is guaranteed to be a string.
        # Therefore, the only potential exception we have to
        # handle is IndexError (in case value = '').
        try:
            return value[0]
        except IndexError:
            return ''

    name_field = FieldPattern(
        name="name",
        alias="Name",
        cellpattern=[cellpatterns.String, first_char],  # This is new
    )

    # replace `birthday_field` with a string literal 'DOB' below.

    birthday_table = FuzzyTable(
        path='birthdays.csv',
        fields=[name_field, 'DOB'],
    )


>>> python birthdays_piping.py
>>> for record in birthday_table.records
...     print(record['name'])
...
'J'
'1'
'J'
''
