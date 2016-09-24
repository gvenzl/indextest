#!/usr/local/bin/python3
import indextest

# MySQL example
class testerMySQL(indextest.IndexTester):
    def __init__(self):
        dbparams = { 'user': 'msandbox',
                     'password': 'msandbox',
                     'host': 'gvenzl-virtual',
                     'port': '3306',
                     'database': 'sakila'}
        self.dbparams = dbparams
        self.dbtype = 'mysql'

    # Simple comparison of access type = ref
    def test_query1(self):
        q1 = self.query("Simple test", "SELECT * FROM actor WHERE first_name='Tom'")
        return q1.testEqual('type', 'ref')

    # Simple comparison of key = index name
    def test_query2(self):
        q2 = self.query("Simple test on index name", "SELECT * FROM actor WHERE first_name='%Tom'")
        return q2.testEqual('key', 'idx_first_name')

    # Combined comparison of type = ref and key = index name
    def test_query3(self):
        q3 = self.query("Combined test on Index name and type", "SELECT * FROM film WHERE rental_rate = 2.99")
        return (q3.testEqual('type', 'ref') and
                q3.testEqual('key', 'idx_rental_rate'))

    # Example of a failing test
    def test_query4(self):
        q4 = self.query("Wrong plan chosen", "SELECT * FROM film WHERE rental_rate = 3.4")
        return q4.testEqual('type', 'range')
    
run = testerMySQL()
run.runall()


# Oracle example
class testerOracle(indextest.IndexTester):
    def __init__(self):
        dbparams = { 'user': 'hr',
                     'password': 'hr',
                     'host': 'localhost',
                     'port': '1521',
                     'database': 'ORCLPDB1'}
        self.dbparams = dbparams
        self.dbtype = 'oracle'

    # Simple comparison of access option = INDEX
    def test_query1(self):
        q1 = self.query("Simple test on OPERATION", "SELECT first_name, last_name FROM employees WHERE employee_id=1")
        return q1.testEqual('OPERATION', 'INDEX')
    
    # Combined comparison of OPERATION = INDEX and OPTION = RANGE SCAN
    def test_query2(self):
        q2 = self.query("Combined test on OPERATION and OPTIONS", "SELECT department_id FROM departments WHERE location_id=1800")
        return (q2.testEqual('OPERATION', 'INDEX') and
                q2.testEqual('OPTIONS', 'RANGE SCAN'))
    
    # Combined comparison of OPERATION = INDEX, OPTIONS = RANGE SCAN and OBJECT_NAME = index name
    def test_query3(self):
        q3 = self.query("Combined test on OPERATION, OPTIONS AND Index name", "SELECT department_id FROM departments WHERE location_id=1800")
        return (q3.testEqual('OPERATION', 'INDEX') and
                q3.testEqual('OPTIONS', 'RANGE SCAN') and
                q3.testEqual('OBJECT_NAME', 'DEPT_LOCATION_IX'))

    # Example of a failing test
    def test_query4(self):
        q4 = self.query("Wrong plan chosen", "SELECT department_id FROM departments WHERE location_id=1800")
        return q4.testEqual('OPTIONS', 'UNIQUE SCAN')

run = testerOracle()
run.runall()
