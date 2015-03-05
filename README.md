#Index Tester
Index Tester is a tool that allows you to unit test your indexes. It supports both, Oracle RDBMS as well as MySQL RDBMS.

## Requirements
* MySQL >= 5.6
* mysql-connector-python >= 2.0.3
* Oracle >= 11.2.0.1
* cx_Oracle >= 5.1.3

## Examples 
### MySQL:
    $ ./example.py 
    Query: SELECT * FROM movies WHERE rank>9.8
    Test: query_block.table.access_type == range
    Result: range == range: True
  
    Query: SELECT * FROM actors WHERE first_name='Tom'
    Test: query_block.table.access_type == range
    Result: range == ref: False
  
    Query: SELECT * FROM actors WHERE first_name='%Tom'
    Test: query_block.table.key == idx_first_name
    Result: idx_first_name == idx_first_name: True
  
    Tested 3 queries, Pass: 2, Fail: 1
