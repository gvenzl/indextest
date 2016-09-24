#!/usr/local/bin/python3
import pprint
import inspect
import json
import random
from random import getrandbits

class IndexTester:
    def query(self, testname, query, debug=False):
        test = IndexTest(testname, query, self.dbparams, self.dbtype, debug)
        return test

    def runall(self):
        """Runs all test methods that start with "test_"."""
        testcount = 0
        resultpass = 0
        resultfail = 0

        members = inspect.getmembers(self, predicate=inspect.ismethod)
        for membername, method in members:
            if membername.startswith('test_'):
                testcount += 1
                result = method()
                if result is True:
                    resultpass += 1
                elif result is False:
                    resultfail += 1
        print('Tested {} queries, Pass: {}, Fail: {}'.format(
               testcount, resultpass, resultfail))

class IndexTest:
    def __init__(self, testname, query, dbparams, dbtype, debug):
        self.testname = testname
        self.dbtype = dbtype
        if self.dbtype == 'oracle':
            import cx_Oracle
            dns = cx_Oracle.makedsn(dbparams['host'], dbparams['port'], service_name = dbparams['database']) # Build dns string
            self.con = cx_Oracle.connect(dbparams['user'], dbparams['password'], dns)
        elif self.dbtype == 'mysql':
            import mysql.connector
            self.con = mysql.connector.connect(**dbparams)
        else:
            raise ValueError("Database type '" + self.dbtype + "' not supported!")
        self.query = query
        self.debug = debug
        self.result = None
    
    def _runquery(self):
        """Runs the explain plan for the query."""
        if self.debug:
            pprint.pprint(self.query)
        cur = self.con.cursor()
        if self.dbtype == 'oracle':
            stmtId = str(getrandbits(30)) # Generate statement Id for explain plan
            cur.execute("EXPLAIN PLAN SET STATEMENT_ID = '" + stmtId + "' FOR " + self.query) # No bind variables for DDL statements
            cur.execute("SELECT *" +
                          " FROM plan_table" +
                          " WHERE statement_id = :1"+
                          " ORDER BY id", (stmtId,))
        elif self.dbtype == 'mysql':
            cur.execute("EXPLAIN FORMAT=TRADITIONAL " + self.query)
        self.result = self._rows_to_dict_list(cur)
        if self.debug:
            pprint.pprint(self.result)
    
    def _rows_to_dict_list(self, cursor):
        """Converts rows and columns into a list of dictionaries"""
        columns = [i[0] for i in cursor.description]
        return [dict(zip(columns, row)) for row in cursor]

    def testEqual(self, field, expected):
        """Tests whether a given operation has been executed.
        
        This method takes a given field and an expected value within that field and tests whether the explain plan has produced such an outcome.
        The field resolves to a column within the explain plan and is case sensitive.
        If the field doesn't exist the function will handle the situation gracefully and return False
        """
        if not self.result:
            self._runquery()

        res = False        
        for line in self.result:
            # The field is not in the explain plan columns dictionary due to e.g. a type the test inherently false
            if field not in line:
                print ("Test '{0}' - WARNING: There is no field '{1}' in the explain plan!\nCheck for a typo in the field parameter.\n".format(self.testname, field))
                actual = None
                break
            actual = line[field]
            if actual == expected:
                res = True
                break

        print('Test: {testname}\n'
              'Query: {query}\n'
              'Test: {field} == {value}\n'
              'Result: {value} == {qval}: {result}\n'.format(
               testname=self.testname, query=self.query, field=field, value=expected, qval=actual, result=res))
        return res
