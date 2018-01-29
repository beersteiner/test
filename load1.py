import pymysql
import sqlalchemy as sa
from odo import odo


## GLOBALS

#HOST = 'MySQL_Server_5.7.21_Auto_Generated_Server_Certificate'
wCliOpt = '/home/john/client-ssl/CastawayCay_MySQL/.writeclient.cnf'
DB_NAME = 'iris'
#URI = host+'?'+'read_default_file='+wCliOpt
#CA = '/home/john/client-ssl/CastawayCay_MySQL/ca.pem'
#CCERT = '/home/john/client-ssl/CastawayCay_MySQL/client-cert.pem'
#CKEY = '/home/john/client-ssl/CastawayCay_MySQL/client-key.pem'

# Table Creation Statements
#TABLES = {}
#TABLES['data'] = {}
#TABLES['data'] = {
#        'csv':'iris_ch.data',
#        'create':(
#                "CREATE TABLE `data` ("
#                "    `sepal-length` FLOAT(10),"
#                "    `sepal-width` FLOAT(10),"
#                "    `petal-length` FLOAT(10),"
#                "    `petal-width` FLOAT(10),"
#                "    `class` VARCHAR(20)"
#                ")"),
#        'populate':(
#                "INSERT INTO data "
#                "(sepal-length, sepal-width, petal-length, petal-width, class) "
#                "VALUES (%f, %f, %f, %f, %s)")
#        }


## FUNCTIONS

# DO NOT MODIFY! - Creates a connection to MySQL Server
def mysql_connect_w():
    return pymysql.connect(read_default_file=wCliOpt)

# DO NOT MODIFY! - Creates a connection to MySQL Database
def db_connect_w():
    return pymysql.connect(read_default_file=wCliOpt, db=DB_NAME)

# DO NOT MODIFY! - Creates a database or returns an error
def create_database(cursor):
    try: cursor.execute(
            'CREATE DATABASE {}'.format(DB_NAME))
    except pymysql.MySQLError as err:
        print('Database {} already exists.'.format(err))
        #exit(1)

# DO NOT MODIFY! - Adds an additional auto-increment column to table
def add_autoinc_col(db, t):
    conn = db.raw_connection()
    cursor = conn.cursor()
    cursor.execute('ALTER TABLE `'+t+'` ADD `id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST')
    cursor.close() # Close handle for SQL server
    conn.close() # Close the connection to the SQL server


## MAIN

# Create Database
sql_eng = sa.create_engine('mysql+pymysql://', creator=mysql_connect_w)
conn = sql_eng.raw_connection()
cursor = conn.cursor() 
create_database(cursor)
cursor.close() # Close handle for SQL server
conn.close() # Close the connection to the SQL server

# Creat the sqlalchemy engine
db_eng = sa.create_engine('mysql+pymysql://', creator=db_connect_w)
metadata = sa.MetaData(bind=db_eng) # holds database information

# create the table object
tbl = sa.Table(
        'data',
        metadata,
        #sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('sepal_length', sa.Float),
        sa.Column('sepal_width', sa.Float),
        sa.Column('petal_length', sa.Float),
        sa.Column('petal_width', sa.Float),
        sa.Column('class', sa.String(20)),
        )

# Use odo to bulk-load data into the table object
odo('iris_ch.data', tbl)

# Add AUTOINCREMENT COLUMN
add_autoinc_col(db_eng, 'data')

