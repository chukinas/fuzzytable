---------------------------------------
Change Log
---------------------------------------

0.19 (16 Dec 2019)
---------------------------------------
- Add ``case_sensitive`` parameter to:

  - ``FuzzyTable``
  - ``FieldPattern``

0.18 (15 Dec 2019)
---------------------------------------
- cellpatterns.StringChoice, FuzzyTable, FieldPattern:

  - deprecate approximate_match, contains_match
  - add ``mode`` parameter (and ``exceptions.ModeError`` for invalid values)

- add searchterms_exclude to Fuzzy
- improve API Documentation

  - autodocsumm
  - :autosummary:

0.17 (10 Dec 2019)
---------------------------------------
- additions to cell pattern: StringChoice:

  - add approximate_match
  - add min_ratio
  - add case_sensitive

0.16 (05 Dec 2019)
---------------------------------------
- new cell pattern: StringChoiceMulti
- documentation:

  - add Boolean example
  - add StringChoiceMulti example

0.15-alpha (04 Dec 2019)
---------------------------------------
- new cell pattern: StringChoice
- Travis CI - master only
- documentation:

  - add FieldPatterns page
  - add CellPatterns page
  - add links to README shields
  - add Contributing.md

0.14-alpha (23 Nov 2019)
---------------------------------------
- add MissingFieldError

0.13-alpha (23 Nov 2019)
---------------------------------------
- add cellpatterns

  - WordList
  - Boolean
  - Digit

0.12-alpha (22 Nov 2019)
---------------------------------------
- fix PyPI docs link
- fix PyPI homepage link
- add cellpatterns

  - String
  - Float
  - Integer
  - IntegerList

- add spreadsheet terminology to docs
- add MIT license file
- add travis & codecov integration
- add How to Contribute page to docs

0.11-alpha (18 Nov 2019)
---------------------------------------
- add MultiField
- add FuzzyTable.get_field()

0.10-alpha (15 Nov 2019)
---------------------------------------
- add FieldPattern

0.9-alpha (14 Nov 2019)
---------------------------------------
- add approximate matching

0.8-alpha (12 Nov 2019)
---------------------------------------
- rebrand EXCELerator to fuzzytable
- rebuild data model
