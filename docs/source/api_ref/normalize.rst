Normalizing Data
-----------------------------


Basic Use
++++++++++

Let's say you have this very simple table:

=========== ========
Name        Birthday
=========== ========
John Doe    1995
123         2003OCt
Jane Doe    1964
River Song  2019
=========== ========

You want to ensure the first field (Name) returns only strings and the
Birthday column returns integers.

.. code-block:: python

    from excelerator import TableReader
    from excelerator import normalize as n

    tr = TableReader(
        path='path/to/excel.xlsx',
        sheetname='names and birthdays',
        fields='Name Birthday'.split(),
        normalize=[n.STRING(), n.INTEGER()],
    )
    fields = tr.get_fields()

``fields['Name']`` returns ``['John Doe', '123', 'Jane Doe', 'River Song']``

``fields['Birthday']`` returns ``[1995, 2003, 1964, 2019]``

.. note::
   Here's a common "gotcha": Make sure to instantiate the normalization classes.
   That is, ``normalize=[n.STRING(), n.INTEGER()]`` instead of ``normalize=[n.STRING, n.INTEGER]``


Create Custom Normalizing Classes
+++++++++++++++++++++++++++++++++++++

But let's say we don't want the full string from ``Names``, but just the first name.

We could subclass either ``NormalizeBase`` or one of its subclasses. Let's subclass ``STRING``.

.. code-block:: python

    # Continuing our code from above...

    class FirstString(n.STRING)

        norm_func = n.STRING().normalize
        # Note the lack of parentheses after normalize
        # We do this here instead of in the normalize method
        # so that n.STRING gets instantiated only once.

        def normalize(self, value):
            # This is the function that gets called to norm your data.
            strings = norm_func(value).split()
            return strings[0]

    tr.normalize = [n.FirstString(), n.INTEGER()]
    fields = tr.get_fields()

``fields['Name']`` returns ``['John', '123', 'Jane', 'River']``

Pretty easy, right?

Classes
++++++++++

.. autoclass:: excelerator.normalize.NormalizeBase
   :members:

.. automodule:: excelerator.normalize
   :members:
   :exclude-members: NormalizeBase
