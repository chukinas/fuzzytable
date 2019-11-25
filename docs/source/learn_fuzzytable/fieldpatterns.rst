---------------------------------------
Field Patterns
---------------------------------------

Field Patterns Are Optional
+++++++++++++++++++++++++++++++++++++++

We've seen what happens if the ``fuzzytable fields`` parameter is left blank.
All fields whose headers are non-blank are collected by FuzzyTable.

We've also seen how passing a list of strings to the ``fuzzytable fields``
parameter not only controls which fields are collected, but also what those fields are named,
so they can be reliably referenced.

Field Patterns provide another layer of control.

Separate naming from search criteria
+++++++++++++++++++++++++++++++++++++++
Let's say there's a field you'd like to name ``birthday``, but the spreadsheet header is called ``D.O.B.``
This is where aliases come in.

Let's say you have this very simple table:

=========== ========
Name        DOB
=========== ========
John Doe    1995
123         2003OCt
Jane Doe    1964
True        2019
=========== ========

.. code-block:: python

    # birthdays.py

    from fuzzytable import FuzzyTable, FieldPattern

    name_field = FieldPattern(
        name="name",
        approximate_match=True,
    )

    birthday_field = FieldPattern(
        name="birthday",
        alias="DOB",
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
{'name': 123, 'birthday': '2003Oct'}
{'name': 'Jane Doe', 'birthday': 1964}
{'name': True, 'birthday': 2019}

Combine FieldPatterns and strings
++++++++++++++++++++++++++++++++++++++++++++

while the birthday field is declared using the

.. code-block:: python

    # birthdays_combined.py

    from fuzzytable import FuzzyTable, FieldPattern

    birthday_field = FieldPattern(
        name="birthday",
        alias="dob",
    )

    birthday_table = FuzzyTable(
        path='birthdays.csv',
        fields=['name', birthday_field],  # Mix string literals and FieldPattern objects as desired
        approximate_match=True,
    )

This generates the same result as above:

>>> python birthdays_combined.py
>>> for record in birthday_table.records
...     print(record)
...
{'name': 'John Doe', 'birthday': 1995}
{'name': 123, 'birthday': '2003Oct'}
{'name': 'Jane Doe', 'birthday': 1964}
{'name': True, 'birthday': 2019}