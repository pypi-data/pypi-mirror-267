Changelog
=========
## [v1.0.2] - 2024-03-29
#### Summarize:
The compatibility for ClickHouse has been greatly improved. It provides good compatibility conversion for the to_char function of Oracle and Postgres. It has made many differentiated adaptations for date format conversion in all dialects. At the same time, it can be regarded as Backticks are automatically added to keyword fields, which greatly improves the compatibility of the converted SQL to be executed directly in doris.
### :sparkles: New Features and :bug: Bug Fixes
#### Presto/Trino
  1. fix JSON function transform 
  2. fix array_range and  regexp_extract function
#### Clickhouse
  1. fix clickhouse's trim function transform
  2. add generateUUIDv4 function transform
  3. add mutiif function transform
  4. add final clause generator
  5. add countdistinct function transform
  6. fix date_sub function transform eg.  date_sub(toDate('2018-01-01'), interval 1 month)
  7. add TOINT64 and TOINT64ORZEROfunction transform
  8. add modulo function transform
  9. add minif function transform
  10. Fix doris does not support global in
  11. fix positionCaseInsensitiveUTF8 and positionCaseInsensitive function transform
  12. add intDiv function transfrom
  13. fix arrayElement and indexof  transform
  14. add ARRAYENUMERATE -> ARRAY_ENUMERATE,IsNotNull -> NOT_NULL_OR_EMPTY
  15. add formatDateTime -> DATE_FORMA
  16. add flatten conversion to doris
  17. add toStartOfInterval conversion to doris
  18. add the implementation of toFloat32
#### Postgres
  1. fix to_char function transform
  2. fix identifiers parse
#### Oracle
  1. add oracle's trim function transform
  2. fix to_char and to_date functions transform
#### Hive
  1. add bigint function transform
#### Spark
  1. Add spark3 dialect support
  2. Add quote_identifier to doris keywords


## [v1.0.1] - 2024-02-18
### :sparkles: New Features
- [`4a8eb691`](https://github.com/selectdb/sqlglot/commit/4a8eb691961e624a7b5d569b2bd8a67386235788) - support explain verbose,explain memo plan,explain physical plan,explain shape plan
  - Automatic conversion of explain statements is supported, including
    - explain
    - explain verbose
    - explain mem plan
    - explain physical plan
    - explain shape plan
- [`10b4e690`](https://github.com/selectdb/sqlglot/commit/10b4e6900913ec4b08b80ebbd254a4b054cb4976) - support match_any/match_all parse
### :bug: Bug Fixes
- Fixed format conversion conflicts in the date function 
- Improved the json type function path parsing and conversion function 
- Repaired several conversion error cases in actual scenarios, optimized the analytic generation of multiple cases, and improved the compatibility to a greater extent