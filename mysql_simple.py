#!/usr/bin/env python
#-*- coding: UTF-8 -*-


'''
#Module: mysql_simple
#Created by Leo Wen on 2017-06-08 21:22:13
'''
import MySQLdb

class MysqlCtl(object):
    '''Control mysql database.
    Connect >> execute >> close
    '''
    def __init__(self):
        self.db_host = 'localhost'
        #self.db_user = 'leo'
        #self.db_password = '123456'
        self.db_user = 'root'
        self.db_password = 'lj'
        self.db_name = 'pydb'
        self.cursor = None
        self.conn = None
        self.db_connect()
        #self.db_drop()

    def set_db_name(self,db_name):
        self.db_name = db_name

    def execute(self,db_cmd):
        self.cursor.execute(db_cmd)

    def db_created (self):
        self.cursor.execute('create database if not exists pydb')
        print 'created a database'

    def db_drop(self):
        try:
            self.cursor.execute('drop database pydb')
            print 'drop a database'
        except MySQLdb.Error, e:
            print 'Mysql error: ',e

    def db_connect(self):
        self.conn = MySQLdb.connect(self.db_host, self.db_user, self.db_password, self.db_name)
        if self.conn:
            self.cursor = self.conn.cursor()
            print 'connect successfully.'

    def db_close(self):
        self.cursor.close()
        self.conn.close()

    def created_table(self, table_dict):
        cmd = ''

def test():
    '''Test'''
    print 'Please test here.'
    db = MysqlCtl()
    db.db_created ()
    #db.db_connect()

if __name__ == '__main__':
    test()
