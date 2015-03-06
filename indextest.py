#!/usr/bin/python3
import pprint
import inspect
import json
import random
from random import getrandbits

class IndexTester:
    def query(self, query, debug=False):
        test = IndexTest(query, self.dbparams, self.dbtype, debug)
        return test

    def runall(self):
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
    def __init__(self, query, dbparams, dbtype, debug):
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
        if self.debug:
            pprint.pprint(self.query)
        cur = self.con.cursor()
        if self.dbtype == 'oracle':
            stmtId = getrandbits(30) # Generate statement Id for explain plan
            cur.execute("EXPLAIN PLAN SET STATEMENT_ID='" + str(stmtId) + "' FOR " + self.query)
            cur.execute("SELECT *" +
                          " FROM plan_table" +
                          " WHERE statement_id = '" + str(stmtId) + "'"+
                          " ORDER BY id")
        elif self.dbtype == 'mysql':
            cur.execute("EXPLAIN FORMAT=TRADITIONAL " + self.query)
        self.result = self._rows_to_dict_list(cur)
        if self.debug:
            pprint.pprint(self.result)
    
    def _rows_to_dict_list(self, cursor):
        columns = [i[0] for i in cursor.description]
        if self.debug:
            pprint.pprint(columns)
        return [dict(zip(columns, row)) for row in cursor]

    def testEqual(self, field, expected):
        if not self.result:
            self._runquery()
        
        for line in self.result:
            actual = line[field]
            if actual == expected:
                result = True
                break
        else:
            result = False

        print('Query: {query}\n'
              'Test: {field} == {value}\n'
              'Result: {value} == {qval}: {result}\n'.format(
               query=self.query, field=field, value=expected, qval=actual, result=result))
        return result
