----------
Change Log
----------

v0.5
----
- TableReader:
    - ``read_from()`` method renamed to ``get_fields()``
    - new method: ``get_records()``

v0.4
----
- add normalization functions:
    - ``n.STRING()``
    - ``n.INTEGER()``
    - ``n.INTEGER_LIST()``
- add ``normalize`` parameter to TableReader

v0.3
----
- add ``header_row_num`` param to ``TableReader``
