----------
Change Log
----------


v0.6
----
- TableReader:
    - moved ``path`` and ``sheetname`` parameters from ``get_fields`` and ``get_records`` methods to ``TableReader()``
    - converted normalize functions to classes.
    - updated documentation


v0.5
----
- TableReader
    - ``read_from()`` method renamed to ``get_fields()``
    - new method: ``get_records()``

v0.4
----
- excelerator.normalize:
    - ``n.STRING()``
    - ``n.INTEGER()``
    - ``n.INTEGER_LIST()``
- add ``normalize`` parameter to TableReader

v0.3
----
- add ``header_row_num`` param to ``TableReader``
