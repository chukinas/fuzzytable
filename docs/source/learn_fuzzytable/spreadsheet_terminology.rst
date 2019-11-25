--------------------------
Terminology
--------------------------

.. image:: /_static/spreadsheet_table.png
   :alt: spreadsheet example


Glossary
----------------------------

- **Row/Column Number** - Counting starts at one.
  This is the primary way of referrring to a row or column.
  The reason is because fuzzytable was written primarily for Excel users, where row numbering starts at one.
  Column A has a col_num of 1, etc. Contrast with Row/Column Index.
- **Row/Column Index** - Like Row/Column Number, but counting starts at zero.
- **terms** - a list of strings that a desired field compares to cell values when seeking its header cell. The field name is always one of the terms. So are any aliases passed to :obj:`~fuzzytable.FieldPattern`.
