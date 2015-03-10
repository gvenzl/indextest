#Index Tester
Index Tester is a tool that allows you to unit test your indexes. It supports both, Oracle RDBMS as well as MySQL RDBMS.
It uses the explain plan facility to examine whether your index is used for the statement.
For further explanation on explain plans and their format look at:
* [MySQL Explain Output Format](http://dev.mysql.com/doc/refman/5.7/en/explain-output.html)
* [Generating and Displaying Execution Plans](http://docs.oracle.com/database/121/TGSQL/tgsql_genplan.htm)

## Requirements
* [MySQL](http://mysql.com/) >= 5.0
* [mysql-connector-python](http://dev.mysql.com/doc/connector-python/en/) >= 2.0.3
* [Oracle](http://www.oracle.com/database/index.html) >= 10.2.0.1
* [cx_Oracle](http://cx-oracle.sourceforge.net/) >= 5.1.3

## Examples 
### MySQL
    $ ./example.py
    Test: Simple test
    Query: SELECT * FROM actor WHERE first_name='Tom'
    Test: type == ref
    Result: ref == ref: True
    
    Test: Simple test on index name
    Query: SELECT * FROM actor WHERE first_name='%Tom'
    Test: key == idx_first_name
    Result: idx_first_name == idx_first_name: True
    
    Test: Combined test on Index name and type
    Query: SELECT * FROM film WHERE rental_rate = 2.99
    Test: type == ref
    Result: ref == ref: True
    
    Test: Combined test on Index name and type
    Query: SELECT * FROM film WHERE rental_rate = 2.99
    Test: key == idx_rental_rate
    Result: idx_rental_rate == idx_rental_rate: True
    
    Test: Wrong plan chosen
    Query: SELECT * FROM film WHERE rental_rate = 3.4
    Test: type == range
    Result: range == ref: False
    
    Tested 4 queries, Pass: 3, Fail: 1

### Oracle
    $ ./example.py
    Test: Simple test on OPERATION
    Query: SELECT first_name, last_name FROM employees WHERE employee_id=1
    Test: OPERATION == INDEX
    Result: INDEX == INDEX: True
    
    Test: Combined test on OPERATION and OPTIONS
    Query: SELECT department_id FROM departments WHERE location_id=1800
    Test: OPERATION == INDEX
    Result: INDEX == INDEX: True
    
    Test: Combined test on OPERATION and OPTIONS
    Query: SELECT department_id FROM departments WHERE location_id=1800
    Test: OPTIONS == RANGE SCAN
    Result: RANGE SCAN == RANGE SCAN: True
    
    Test: Combined test on OPERATION, OPTIONS AND Index name
    Query: SELECT department_id FROM departments WHERE location_id=1800
    Test: OPERATION == INDEX
    Result: INDEX == INDEX: True
    
    Test: Combined test on OPERATION, OPTIONS AND Index name
    Query: SELECT department_id FROM departments WHERE location_id=1800
    Test: OPTIONS == RANGE SCAN
    Result: RANGE SCAN == RANGE SCAN: True
    
    Test: Combined test on OPERATION, OPTIONS AND Index name
    Query: SELECT department_id FROM departments WHERE location_id=1800
    Test: OBJECT_NAME == DEPT_LOCATION_IX
    Result: DEPT_LOCATION_IX == DEPT_LOCATION_IX: True
    
    Test: Wrong plan chosen
    Query: SELECT department_id FROM departments WHERE location_id=1800
    Test: OPTIONS == UNIQUE SCAN
    Result: UNIQUE SCAN == RANGE SCAN: False
    
    Tested 4 queries, Pass: 3, Fail: 1