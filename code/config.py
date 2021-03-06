#!/usr/bin/python

"""
CSC 315 Project
Group 4 - CivicStats
Gordon Petry, Jason Kantner, Michael Williams, Casey Lishko

This code is from:
https://www.postgresqltutorial.com/postgresql-python/
"""

from ConfigParser import ConfigParser


def config(filename='database.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db
