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

class ValOption:
    def __init__(self, view, title):
        self.title = title
        self.view = view


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

def page_template(label_type, label_choices, val_choices, label_query, value_query, title_, max_value):
    xaxis = []
    yaxis = []
    names = connect(label_query)
    for name in names:
        new_name = convertTuple(name)
        new_name = new_name.replace('&', 'and')
        xaxis.append(new_name)
    totals = connect(value_query)
    # print(totals)
    for total in totals:
        new_total = convertTuple(total)
        yaxis.append(int(new_total))
        # print(new_total)
    return render_template('chart.html', label_type=label_type, label_choices=label_choices, val_choices=val_choices, title=title_, max=max_value, values=yaxis, labels=xaxis)

# app.py

app = Flask(__name__)


# serve form web page
@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/categories")
def categories():
    label_type = "Categories"
    label_choices = []
    label_options = connect("SELECT cname FROM Categories")
    for label_option in label_options:
        new_label_option = convertTuple(label_option)
        # new_label_option = new_label_option.replace('&', 'and')
        label_choices.append(new_label_option)
    v1 = ValOption("pt_tot_category", "Total Points")
    v2 = ValOption("no_priority_cat", "NonPriority Actions")
    v3 = ValOption("yes_priority_cat", "Priority Actions")
    v4 = ValOption("no_required_cat", "NonRequired Actions")
    v5 = ValOption("yes_required_cat", "Required Actions")
    val_choices = [v1, v2, v3, v4, v5]

    return render_template('chart.html', label_type=label_type, label_choices=label_choices, val_choices=val_choices)

@app.route('/categories', methods=['POST'])
def handle_data_c():
    label_type = "Categories"
    label_choices = []
    label_options = connect("SELECT cname FROM pt_tot_category")
    for label_option in label_options:
        new_label_option = convertTuple(label_option)
        # new_label_option = new_label_option.replace('&', 'and')
        label_choices.append(new_label_option)
    v1 = ValOption("pt_tot_category", "Total Points")
    v2 = ValOption("no_priority_cat", "NonPriority Actions")
    v3 = ValOption("yes_priority_cat", "Priority Actions")
    v4 = ValOption("no_required_cat", "NonRequired Actions")
    v5 = ValOption("yes_required_cat", "Required Actions")
    val_choices = [v1, v2, v3, v4, v5]
    labels = request.form.getlist('label')
    val = request.form.get('val')
    if len(labels) == 0:
        if val == "pt_tot_category":
            label_query='SELECT cname FROM ' + val
            value_query='SELECT total_points FROM ' + val
            title_='Total Points per Category'
            max_value=210
            # print("test")
        elif val == "no_priority_cat":
            label_query='SELECT cname FROM ' + val
            value_query='SELECT Total_NonPriority_Actions FROM ' + val
            title_='Total Non-Priority Actions per Category'
            max_value=18
            # print("test2")
        elif val == "yes_priority_cat":
            label_query='SELECT cname FROM ' + val
            value_query='SELECT total_priority_actions FROM ' + val
            title_='Total Priority Actions per Category'
            max_value=5
            # print("test2")
        elif val == "no_required_cat":
            label_query='SELECT cname FROM ' + val
            value_query='SELECT total_nonrequired_actions FROM ' + val
            title_='Total Non-Required Actionsper Category'
            max_value=20
            # print("test2")
        elif val == "yes_required_cat":
            label_query='SELECT cname FROM ' + val
            value_query='SELECT total_required_actions FROM ' + val
            title_='Total Required Actions per Category'
            max_value=2
            # print("test2")
        else:
            label_query='SELECT cname FROM pt_tot_category'
            value_query='SELECT total_points FROM pt_tot_category'
            title_='Check Inputs'
            max_value=210
    elif len(labels) == 1:
        if val == "pt_tot_category":
            # labels[0].replace('and', '&')
            label_query="SELECT cname FROM " + val + " WHERE cname=\'" + labels[0] + "\'"
            value_query="SELECT total_points FROM " + val + " WHERE cname=\'" + labels[0] + "\'"
            title_='Total Points in ' + labels[0]
            max_value=210
            # print(label_query)
            # print("test")
        elif val == "no_priority_cat":
            label_query="SELECT cname FROM " + val + " WHERE cname=\'" + labels[0] + "\'"
            value_query='SELECT Total_NonPriority_Actions FROM ' + val + ' WHERE cname=\"' + labels[0] + '\"'
            title_='Total Non-Priority Actions in ' + labels[0]
            max_value=18
            # print("test2")
        elif val == "yes_priority_cat":
            label_query='SELECT cname FROM ' + val + " WHERE cname=\'" + labels[0] + "\'"
            value_query='SELECT total_priority_actions FROM ' + val + " WHERE cname=\'" + labels[0] + "\'"
            title_='Total Priority Actions in ' + labels[0]
            max_value=5
            # print("test2")
        elif val == "no_required_cat":
            label_query='SELECT cname FROM ' + val + " WHERE cname=\'" + labels[0] + "\'"
            value_query='SELECT total_nonrequired_actions FROM ' + val + " WHERE cname=\'" + labels[0] + "\'"
            title_='Total Non-Required Actions in ' + labels[0]
            max_value=20
            # print("test2")
        elif val == "yes_required_cat":
            label_query='SELECT cname FROM ' + val + " WHERE cname=\'" + labels[0] + "\'"
            value_query='SELECT total_required_actions FROM ' + val + " WHERE cname=\'" + labels[0] + "\'"
            title_='Total Required Actions in ' + labels[0]
            max_value=2
            # print("test2")
        else:
            label_query='SELECT cname FROM pt_tot_category'
            value_query='SELECT total_points FROM pt_tot_category'
            title_='Check Inputs'
            max_value=210
    else:
        if val == "pt_tot_category":
            # labels[0].replace('and', '&')
            list = labels
            label = list.pop(0)
            label_query="SELECT cname FROM " + val + " WHERE cname IN (\'" + label + "\'"
            value_query="SELECT total_points FROM " + val + " WHERE cname IN (\'" + label + "\'"
            title_='Total Points in ' + label
            while list:
                label = list.pop(0)
                label_query+= ", \'" + label + "\'"
                value_query+= ", \'" + label + "\'"
                title_+= " and " + label
            label_query+= ");"
            value_query+= ");"
            max_value=210
            # print(label_query)
            # print(value_query)
            # print("test")
        elif val == "no_priority_cat":
            list = labels
            label = list.pop(0)
            label_query="SELECT cname FROM " + val + " WHERE cname IN (\'" + label + "\'"
            value_query="SELECT Total_NonPriority_Actions FROM " + val + " WHERE cname IN (\'" + label + "\'"
            title_='Total Points in ' + label
            while list:
                label = list.pop(0)
                label_query+= ", \'" + label + "\'"
                value_query+= ", \'" + label + "\'"
                title_+= " and " + label
            label_query+= ");"
            value_query+= ");"
            max_value=18
            # print("test2")
        elif val == "yes_priority_cat":
            list = labels
            label = list.pop(0)
            label_query="SELECT cname FROM " + val + " WHERE cname IN (\'" + label + "\'"
            value_query="SELECT Total_Priority_Actions FROM " + val + " WHERE cname IN (\'" + label + "\'"
            title_='Total Points in ' + label
            while list:
                label = list.pop(0)
                label_query+= ", \'" + label + "\'"
                value_query+= ", \'" + label + "\'"
                title_+= " and " + label
            label_query+= ");"
            value_query+= ");"
            max_value=5
            # print("test2")
        elif val == "no_required_cat":
            list = labels
            label = list.pop(0)
            label_query="SELECT cname FROM " + val + " WHERE cname IN (\'" + label + "\'"
            value_query="SELECT total_nonrequired_actions FROM " + val + " WHERE cname IN (\'" + label + "\'"
            title_='Total Points in ' + label
            while list:
                label = list.pop(0)
                label_query+= ", \'" + label + "\'"
                value_query+= ", \'" + label + "\'"
                title_+= " and " + label
            label_query+= ");"
            value_query+= ");"
            max_value=20
            # print("test2")
        elif val == "yes_required_cat":
            list = labels
            label = list.pop(0)
            label_query="SELECT cname FROM " + val + " WHERE cname IN (\'" + label + "\'"
            value_query="SELECT Total_required_Actions FROM " + val + " WHERE cname IN (\'" + label + "\'"
            title_='Total Points in ' + label
            while list:
                label = list.pop(0)
                label_query+= ", \'" + label + "\'"
                value_query+= ", \'" + label + "\'"
                title_+= " and " + label
            label_query+= ");"
            value_query+= ");"
            max_value=2
            # print("test2")
        else:
            list = labels
            label = list.pop(0)
            label_query="SELECT cname FROM " + val + " WHERE cname IN (\'" + label + "\'"
            value_query="SELECT pt_tot_category FROM " + val + " WHERE cname IN (\'" + label + "\'"
            title_='Check Values' + label
            while list:
                label = list.pop(0)
                label_query+= ", \'" + label + "\'"
                value_query+= ", \'" + label + "\'"
                title_+= " and " + label
            label_query+= ");"
            value_query+= ");"
            max_value=210

    return page_template(label_type=label_type, label_choices=label_choices, val_choices=val_choices, label_query=label_query, value_query=value_query, title_=title_, max_value=max_value)

@app.route("/counties")
def counties():
    label_type = "Counties"
    label_choices = []
    label_options = connect("SELECT ctyname FROM Counties")
    for label_option in label_options:
        new_label_option = convertTuple(label_option)
        # new_label_option = new_label_option.replace('&', 'and')
        label_choices.append(new_label_option)
    v1 = ValOption("tot_act_cty", "Total Actions")
    v2 = ValOption("tot_pts_cty", "Total Points")
    v3 = ValOption("tot_cat_cty", "Total Categories")
    v4 = ValOption("bronze_stars_cty", "Total Bronze")
    v5 = ValOption("silver_stars_cty", "Total Silver")
    val_choices = [v1, v2, v3, v4, v5]

    return render_template('chart.html', label_type=label_type, label_choices=label_choices, val_choices=val_choices)

@app.route('/counties', methods=['POST'])
def handle_data_cty():
    label_type = "Counties"
    label_choices = []
    label_options = connect("SELECT ctyname FROM Counties")
    for label_option in label_options:
        new_label_option = convertTuple(label_option)
        # new_label_option = new_label_option.replace('&', 'and')
        label_choices.append(new_label_option)
    v1 = ValOption("tot_act_cty", "Total Actions")
    v2 = ValOption("tot_pts_cty", "Total Points")
    v3 = ValOption("tot_cat_cty", "Total Categories")
    v4 = ValOption("bronze_stars_cty", "Total Bronze")
    v5 = ValOption("silver_stars_cty", "Total Silver")
    val_choices = [v1, v2, v3, v4, v5]

    labels = request.form.getlist('label')
    val = request.form.get('val')
    if len(labels) == 0:
        if val == "tot_act_cty":
            label_query='SELECT ctyname FROM ' + val
            value_query='SELECT count_action FROM ' + val
            title_='Total Actions Completed per County'
            max_value=90
            # print("test")
        elif val == "tot_pts_cty":
            label_query='SELECT ctyname FROM ' + val
            value_query='SELECT total_points FROM ' + val
            title_='Total Points per County'
            max_value=850
            # print("test2")
        elif val == "tot_cat_cty":
            label_query='SELECT ctyname FROM ' + val
            value_query='SELECT count_category FROM ' + val
            title_='Total Categories per County'
            max_value=20
            # print("test2")
        elif val == "bronze_stars_cty":
            label_query='SELECT ctyname FROM ' + val
            value_query='SELECT total_bronze FROM ' + val
            title_='Total Bronze Certifications per County'
            max_value=5
            # print("test2")
        elif val == "silver_stars_cty":
            label_query='SELECT ctyname FROM ' + val
            value_query='SELECT total_silver FROM ' + val
            title_='Total Silver Certifications per County'
            max_value=5
            # print("test2")
        else:
            label_query='SELECT cname FROM pt_tot_category'
            value_query='SELECT total_points FROM pt_tot_category'
            title_='Check Inputs'
            max_value=210
    elif len(labels) == 1:
        if val == "tot_act_cty":
            # labels[0].replace('and', '&')
            label_query="SELECT ctyname FROM " + val + " WHERE ctyname=\'" + labels[0] + "\'"
            value_query="SELECT count_action FROM " + val + " WHERE ctyname=\'" + labels[0] + "\'"
            title_='Total Actions Completed in ' + labels[0]
            max_value=90
            # print(label_query)
            # print("test")
        elif val == "tot_pts_cty":
            label_query="SELECT ctyname FROM " + val + " WHERE ctyname=\'" + labels[0] + "\'"
            value_query='SELECT total_points FROM ' + val + ' WHERE ctyname=\"' + labels[0] + '\"'
            title_='Total Points in ' + labels[0]
            max_value=850
            # print("test2")
        elif val == "tot_cat_cty":
            label_query='SELECT ctyname FROM ' + val + " WHERE ctyname=\'" + labels[0] + "\'"
            value_query='SELECT count_category FROM ' + val + " WHERE ctyname=\'" + labels[0] + "\'"
            title_='Total Categories Contributed to in ' + labels[0]
            max_value=20
            # print("test2")
        elif val == "bronze_stars_cty":
            label_query='SELECT ctyname FROM ' + val + " WHERE ctyname=\'" + labels[0] + "\'"
            value_query='SELECT total_bronze FROM ' + val + " WHERE ctyname=\'" + labels[0] + "\'"
            title_='Total Bronze Certifications in ' + labels[0]
            max_value=5
            # print("test2")
        elif val == "silver_stars_cty":
            label_query='SELECT ctyname FROM ' + val + " WHERE ctyname=\'" + labels[0] + "\'"
            value_query='SELECT total_silver FROM ' + val + " WHERE ctyname=\'" + labels[0] + "\'"
            title_='Total Silver Certifications in ' + labels[0]
            max_value=5
            # print("test2")
        else:
            label_query='SELECT cname FROM pt_tot_category'
            value_query='SELECT total_points FROM pt_tot_category'
            title_='Check Inputs'
            max_value=210
    else:
        if val == "tot_act_cty":
            # labels[0].replace('and', '&')
            list = labels
            label = list.pop(0)
            label_query="SELECT ctyname FROM " + val + " WHERE ctyname IN (\'" + label + "\'"
            value_query="SELECT count_action FROM " + val + " WHERE ctyname IN (\'" + label + "\'"
            title_='Total Actions in ' + label
            while list:
                label = list.pop(0)
                label_query+= ", \'" + label + "\'"
                value_query+= ", \'" + label + "\'"
                title_+= " and " + label
            label_query+= ");"
            value_query+= ");"
            max_value=90
            # print(label_query)
            # print(value_query)
            # print("test")
        elif val == "tot_pts_cty":
            list = labels
            label = list.pop(0)
            label_query="SELECT ctyname FROM " + val + " WHERE ctyname IN (\'" + label + "\'"
            value_query="SELECT total_points FROM " + val + " WHERE ctyname IN (\'" + label + "\'"
            title_='Total Points in ' + label
            while list:
                label = list.pop(0)
                label_query+= ", \'" + label + "\'"
                value_query+= ", \'" + label + "\'"
                title_+= " and " + label
            label_query+= ");"
            value_query+= ");"
            max_value=850
            # print("test2")
        elif val == "tot_cat_cty":
            list = labels
            label = list.pop(0)
            label_query="SELECT ctyname FROM " + val + " WHERE ctyname IN (\'" + label + "\'"
            value_query="SELECT count_category FROM " + val + " WHERE ctyname IN (\'" + label + "\'"
            title_='Total Categories Contributed to in ' + label
            while list:
                label = list.pop(0)
                label_query+= ", \'" + label + "\'"
                value_query+= ", \'" + label + "\'"
                title_+= " and " + label
            label_query+= ");"
            value_query+= ");"
            max_value=20
            # print("test2")
        elif val == "bronze_stars_cty":
            list = labels
            label = list.pop(0)
            label_query="SELECT ctyname FROM " + val + " WHERE ctyname IN (\'" + label + "\'"
            value_query="SELECT total_bronze FROM " + val + " WHERE ctyname IN (\'" + label + "\'"
            title_='Total Bronze Certifications in ' + label
            while list:
                label = list.pop(0)
                label_query+= ", \'" + label + "\'"
                value_query+= ", \'" + label + "\'"
                title_+= " and " + label
            label_query+= ");"
            value_query+= ");"
            max_value=5
            # print("test2")
        elif val == "silver_stars_cty":
            list = labels
            label = list.pop(0)
            label_query="SELECT ctyname FROM " + val + " WHERE ctyname IN (\'" + label + "\'"
            value_query="SELECT total_silver FROM " + val + " WHERE ctyname IN (\'" + label + "\'"
            title_='Total Silver Certifications in ' + label
            while list:
                label = list.pop(0)
                label_query+= ", \'" + label + "\'"
                value_query+= ", \'" + label + "\'"
                title_+= " and " + label
            label_query+= ");"
            value_query+= ");"
            max_value=5
            # print("test2")
        else:
            list = labels
            label = list.pop(0)
            label_query="SELECT cname FROM " + val + " WHERE cname IN (\'" + label + "\'"
            value_query="SELECT pt_tot_category FROM " + val + " WHERE cname IN (\'" + label + "\'"
            title_='Check Values' + label
            while list:
                label = list.pop(0)
                label_query+= ", \'" + label + "\'"
                value_query+= ", \'" + label + "\'"
                title_+= " and " + label
            label_query+= ");"
            value_query+= ");"
            max_value=210

    return page_template(label_type=label_type, label_choices=label_choices, val_choices=val_choices, label_query=label_query, value_query=value_query, title_=title_, max_value=max_value)

@app.route("/municipalities")
def municipalities():
    label_type = "Municipalities"
    label_choices = []
    label_options = connect("SELECT mname FROM Municipalities")
    for label_option in label_options:
        new_label_option = convertTuple(label_option)
        # new_label_option = new_label_option.replace('&', 'and')
        label_choices.append(new_label_option)
    v1 = ValOption("tot_act_mun", "Total Actions")
    v2 = ValOption("tot_pts_mun", "Total Points")
    v3 = ValOption("tot_cat_mun", "Total Categories")
    val_choices = [v1, v2, v3]

    return render_template('chart.html', label_type=label_type, label_choices=label_choices, val_choices=val_choices)

@app.route('/municipalities', methods=['POST'])
def handle_data_m():
    label_type = "Municipalities"
    label_choices = []
    label_options = connect("SELECT mname FROM Municipalities")
    for label_option in label_options:
        new_label_option = convertTuple(label_option)
        # new_label_option = new_label_option.replace('&', 'and')
        label_choices.append(new_label_option)
    v1 = ValOption("tot_act_mun", "Total Actions")
    v2 = ValOption("tot_pts_mun", "Total Points")
    v3 = ValOption("tot_cat_mun", "Total Categories")
    val_choices = [v1, v2, v3]

    labels = request.form.getlist('label')
    val = request.form.get('val')
    if len(labels) == 0:
        if val == "tot_act_mun":
            label_query='SELECT mname FROM ' + val
            value_query='SELECT count_action FROM ' + val
            title_='Total Actions Completed per Municipality'
            max_value=50
            # print("test")
        elif val == "tot_pts_mun":
            label_query='SELECT mname FROM ' + val
            value_query='SELECT total_points FROM ' + val
            title_='Total Points per Municipality'
            max_value=550
            # print("test2")
        elif val == "tot_cat_mun":
            label_query='SELECT mname FROM ' + val
            value_query='SELECT count_category FROM ' + val
            title_='Total Categories Contributed to per Municipality'
            max_value=18
            # print("test2")
        else:
            label_query='SELECT cname FROM pt_tot_category'
            value_query='SELECT total_points FROM pt_tot_category'
            title_='Check Inputs'
            max_value=210
    elif len(labels) == 1:
        if val == "tot_act_mun":
            # labels[0].replace('and', '&')
            label_query="SELECT mname FROM " + val + " WHERE mname=\'" + labels[0] + "\'"
            value_query="SELECT count_action FROM " + val + " WHERE mname=\'" + labels[0] + "\'"
            title_='Total Actions Completed in ' + labels[0]
            max_value=50
            # print(label_query)
            # print("test")
        elif val == "tot_pts_mun":
            label_query="SELECT mname FROM " + val + " WHERE mname=\'" + labels[0] + "\'"
            value_query='SELECT total_points FROM ' + val + ' WHERE mname=\"' + labels[0] + '\"'
            title_='Total Points in ' + labels[0]
            max_value=550
            # print("test2")
        elif val == "tot_cat_mun":
            label_query='SELECT mname FROM ' + val + " WHERE mname=\'" + labels[0] + "\'"
            value_query='SELECT count_category FROM ' + val + " WHERE mname=\'" + labels[0] + "\'"
            title_='Total Categories Contributed to in ' + labels[0]
            max_value=18
            # print("test2")
        else:
            label_query='SELECT cname FROM pt_tot_category'
            value_query='SELECT total_points FROM pt_tot_category'
            title_='Check Inputs'
            max_value=210
    else:
        if val == "tot_act_mun":
            # labels[0].replace('and', '&')
            list = labels
            label = list.pop(0)
            label_query="SELECT mname FROM " + val + " WHERE mname IN (\'" + label + "\'"
            value_query="SELECT count_action FROM " + val + " WHERE mname IN (\'" + label + "\'"
            title_='Total Actions in ' + label
            while list:
                label = list.pop(0)
                label_query+= ", \'" + label + "\'"
                value_query+= ", \'" + label + "\'"
                title_+= " and " + label
            label_query+= ");"
            value_query+= ");"
            max_value=50
            # print(label_query)
            # print(value_query)
            # print("test")
        elif val == "tot_pts_mun":
            list = labels
            label = list.pop(0)
            label_query="SELECT mname FROM " + val + " WHERE mname IN (\'" + label + "\'"
            value_query="SELECT total_points FROM " + val + " WHERE mname IN (\'" + label + "\'"
            title_='Total Points in ' + label
            while list:
                label = list.pop(0)
                label_query+= ", \'" + label + "\'"
                value_query+= ", \'" + label + "\'"
                title_+= " and " + label
            label_query+= ");"
            value_query+= ");"
            max_value=550
            # print("test2")
        elif val == "tot_cat_mun":
            list = labels
            label = list.pop(0)
            label_query="SELECT mname FROM " + val + " WHERE mname IN (\'" + label + "\'"
            value_query="SELECT count_category FROM " + val + " WHERE mname IN (\'" + label + "\'"
            title_='Total Categories Contributed to in ' + label
            while list:
                label = list.pop(0)
                label_query+= ", \'" + label + "\'"
                value_query+= ", \'" + label + "\'"
                title_+= " and " + label
            label_query+= ");"
            value_query+= ");"
            max_value=18
            # print("test2")
        else:
            list = labels
            label = list.pop(0)
            label_query="SELECT cname FROM " + val + " WHERE cname IN (\'" + label + "\'"
            value_query="SELECT pt_tot_category FROM " + val + " WHERE cname IN (\'" + label + "\'"
            title_='Check Values' + label
            while list:
                label = list.pop(0)
                label_query+= ", \'" + label + "\'"
                value_query+= ", \'" + label + "\'"
                title_+= " and " + label
            label_query+= ");"
            value_query+= ");"
            max_value=210

    return page_template(label_type=label_type, label_choices=label_choices, val_choices=val_choices, label_query=label_query, value_query=value_query, title_=title_, max_value=max_value)

@app.route("/actions")
def actions():
    label_type = "Actions"
    label_choices = []
    label_options = connect("SELECT aname FROM Actions")
    for label_option in label_options:
        new_label_option = convertTuple(label_option)
        # new_label_option = new_label_option.replace('&', 'and')
        label_choices.append(new_label_option)
    v1 = ValOption("pt_tot_act", "Total Points")
    val_choices = [v1]

    return render_template('chart.html', label_type=label_type, label_choices=label_choices, val_choices=val_choices)

@app.route('/actions', methods=['POST'])
def handle_data_a():
    label_type = "Actions"
    label_choices = []
    label_options = connect("SELECT aname FROM Actions")
    for label_option in label_options:
        new_label_option = convertTuple(label_option)
        # new_label_option = new_label_option.replace('&', 'and')
        label_choices.append(new_label_option)
    v1 = ValOption("pt_tot_act", "Total Points")
    val_choices = [v1]

    labels = request.form.getlist('label')
    val = request.form.get('val')
    if len(labels) == 0:
        if val == "pt_tot_act":
            label_query='SELECT aname FROM ' + val
            value_query='SELECT total_points FROM ' + val
            title_='Total Points per Action'
            max_value=30
        else:
            label_query='SELECT cname FROM pt_tot_category'
            value_query='SELECT total_points FROM pt_tot_category'
            title_='Check Inputs'
            max_value=210
    elif len(labels) == 1:
        if val == "pt_tot_act":
            label_query="SELECT aname FROM " + val + " WHERE aname=\'" + labels[0] + "\'"
            value_query='SELECT total_points FROM ' + val + " WHERE aname=\'" + labels[0] + "\'"
            title_='Total Points in ' + labels[0]
            max_value=30
            # print("test2")
        else:
            label_query='SELECT cname FROM pt_tot_category'
            value_query='SELECT total_points FROM pt_tot_category'
            title_='Check Inputs'
            max_value=210
    else:
        if val == "pt_tot_act":
            list = labels
            label = list.pop(0)
            label_query="SELECT aname FROM " + val + " WHERE aname IN (\'" + label + "\'"
            value_query="SELECT total_points FROM " + val + " WHERE aname IN (\'" + label + "\'"
            title_='Total Points in ' + label
            while list:
                label = list.pop(0)
                label_query+= ", \'" + label + "\'"
                value_query+= ", \'" + label + "\'"
                title_+= " and " + label
            label_query+= ");"
            value_query+= ");"
            max_value=30
            # print("test2")
        else:
            list = labels
            label = list.pop(0)
            label_query="SELECT cname FROM " + val + " WHERE cname IN (\'" + label + "\'"
            value_query="SELECT pt_tot_category FROM " + val + " WHERE cname IN (\'" + label + "\'"
            title_='Check Values' + label
            while list:
                label = list.pop(0)
                label_query+= ", \'" + label + "\'"
                value_query+= ", \'" + label + "\'"
                title_+= " and " + label
            label_query+= ");"
            value_query+= ");"
            max_value=210

    return page_template(label_type=label_type, label_choices=label_choices, val_choices=val_choices, label_query=label_query, value_query=value_query, title_=title_, max_value=max_value)


if __name__ == '__main__':
    app.run(debug = True)
