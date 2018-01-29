import mysql.connector
import numpy as np
import pandas as pd
import csv

## GLOBALS

wCliOpt = '/home/john/client-ssl/CastawayCay_MySQL/.writeclient.cnf'
rCliOpt = '/home/john/client-ssl/CastawayCay_MySQL/.readclient.cnf'
DB_NAME = 'iris'
D_FILE = 'iris_ch.data'
CNK_SIZE = 100

# Table Creation Statements
TABLES = {}
TABLES['data'] = {}
TABLES['data'] = {
        'csv':'iris_ch.data',
        'create':(
                "CREATE TABLE `data` ("
                "    `sepal-length` FLOAT(10),"
                "    `sepal-width` FLOAT(10),"
                "    `petal-length` FLOAT(10),"
                "    `petal-width` FLOAT(10),"
                "    `class` VARCHAR(20)"
                ")"),
        'populate':(
                "INSERT INTO data "
                "(sepal-length, sepal-width, petal-length, petal-width, class) "
                "VALUES (%f, %f, %f, %f, %s)")
        }


## FUNCTIONS

# DO NOT MODIFY!
# Creates a database or returns an error
def create_database(cursor):
    try: cursor.execute(
            'CREATE DATABASE {}'.format(DB_NAME))
    except mysql.connector.Error as err:
        print('Failed creating database: {}'.format(err))
        exit(1)


## MAIN

# DO NOT MODIFY!
# Establish connection and cursor
conn = mysql.connector.connect(option_files=wCliOpt) # establish connection
cursor = conn.cursor()                               # grab a cursor
# Use or establish database
try: conn.database = DB_NAME # try to use database
except mysql.connector.Error as err:
    if err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
        create_database(cursor) # if database doesn't exist, create it
        conn.database = DB_NAME # use the created database
    else: # print any other error
        print(err)
        exit(1)
# Create tables
for table in TABLES.keys(): # Iterate through the table creation statements
    try:
        print 'Creating table %s: ' % table,
        cursor.execute(TABLES[table]['create']) # create the table
    except mysql.connector.Error as err:
        if err.errno == mysql.connector.errorcode.ER_TABLE_EXISTS_ERROR:
            print 'already exists.'
        else:
            print err.msg
    else:
        # Populate the table
        data = csv.reader(file(TABLES[table]['csv']))
        next(data) # skip header file
        for row in data:
            print row
            cursor.execute(TABLES[table]['populate'], row)
        print 'OK.'






cursor.close() # Close handle for SQL server
conn.close() # Close the connection to the SQL server
