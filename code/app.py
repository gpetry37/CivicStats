#! /usr/bin/python2

"""
IMPORTANT

To run this example in the CSC 315 VM you first need to make
the following one-time configuration changes:

# install psycopg2 python package
sudo apt-get update
sudo apt-get install postgres-psycopg2

# set the postgreSQL password for user 'osc'
sudo -u postgres psql
    ALTER USER osc PASSWORD 'osc';
    \q

# install flask
sudo apt-get install python-pip
pip install flask
# logout, then login again to inherit new shell environment

"""

"""
CSC 315
Spring 2020
John DeGood

Usage:
export FLASK_APP=app.py
flask run
# then browse to http://127.0.0.1:5000/

Purpose:
Demonstrate Flask/Python to PostgreSQL using the psycopg
adapter. Connects to the 7dbs database from "Seven Databases
in Seven Days" in the CSC 315 VM.

This example uses Python 2 because Python 2 is the default in
Ubuntu 18.04 LTS on the CSC 315 VM.

For psycopg documentation:
https://www.psycopg.org/

This example code is derived from:
https://www.postgresqltutorial.com/postgresql-python/
https://scoutapm.com/blog/python-flask-tutorial-getting-started-with-flask
https://www.geeksforgeeks.org/python-using-for-loop-in-flask/
"""

import psycopg2
from config import config
from flask import Flask, render_template, request
from datetime import time
import functools
import operator

def connect(query):
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the %s database...' % (params['database']))
        conn = psycopg2.connect(**params)
        print('Connected.')

        # create a cursor
        cur = conn.cursor()

        # execute a query using fetchall()
        cur.execute(query)
        rows = cur.fetchall()

       # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
    # return the query result from fetchall()
    return rows

def convertTuple(tup):
    str = functools.reduce(operator.add, (tup))
    return str

# app.py

app = Flask(__name__)


# serve form web page
@app.route("/")
@app.rout("home")
def form():
    return render_template('home.html')

# example page
@app.route("/bar")
def bar():
    labels = [
        'JAN', 'FEB', 'MAR', 'APR',
        'MAY', 'JUN', 'JUL', 'AUG',
        'SEP', 'OCT', 'NOV', 'DEC'
    ]
    values = [
        967.67, 1190.89, 1079.75, 1349.19,
        2328.91, 2504.28, 2873.83, 4764.87,
        4349.29, 6458.30, 9907, 16297
    ]
    bar_labels=labels
    bar_values=values
    return render_template('chart.html', title='Bitcoin Monthly Price in USD', max=17000, labels=bar_labels, values=bar_values)


@app.route("/pt_tot_category")
def pt_tot_category():
    xaxis = []
    yaxis = []
    names = connect('SELECT cname FROM pt_tot_category')
    for name in names:
        new_name = convertTuple(name)
        xaxis.append(new_name)
        # print(new_name)
        # print(type(new_name))
    totals = connect('SELECT sum FROM pt_tot_category')
    for total in totals:
        new_total = convertTuple(total)
        yaxis.append(int(new_total))
        # print(new_total)
        # print(type(new_total))
    return render_template('chart.html', title='Point Total per Category', max=210, values=yaxis, labels=xaxis)

@app.route("/tot_pts_cty")
def tot_pts_cty():
    xaxis = []
    yaxis = []
    names = connect('SELECT ctyname FROM tot_pts_cty')
    for name in names:
        new_name = convertTuple(name)
        xaxis.append(new_name)
        # print(new_name)
        # print(type(new_name))
    totals = connect('SELECT total_points FROM tot_pts_cty')
    for total in totals:
        new_total = convertTuple(total)
        yaxis.append(int(new_total))
        # print(new_total)
        # print(type(new_total))
    return render_template('chart.html', title='Point Total per County', max=520, values=yaxis, labels=xaxis)

if __name__ == '__main__':
    app.run(debug = True)
