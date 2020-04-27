# To run this program in the CSC 315 VM you first need to make the following one-time configuration changes:
## install psycopg2 python package
sudo apt-get update
sudo apt-get install postgres-psycopg2
## The above commands may not work. Try running these instead:
sudo apt-get install python3 libpq-dev python-dev python3-dev
pip install psycopg2
# set the postgreSQL password for user 'osc'
sudo -u postgres psql
...ALTER USER osc PASSWORD 'osc';
...\q
## install flask
sudo apt-get install python-pip
pip install flask
## logout, then login again to inherit new shell environment
## initialize database
. initialize_db.txt

# CSC 315 Project
# Group 4 - CivicStats
# Gordon Petry, Jason Kantner, Michael Williams, Casey Lishko
### Usage Debug Mode Off:
export FLASK_APP=app.py
flask run
#### then browse to http://127.0.0.1:5000/
### Usage Debug Mode On:
python app.py
#### then browse to http://127.0.0.1:5000/
## Purpose:
Utilizing data pulled from sustainablejersey.com, this
program will allow to user to look at data between different
counties, municipalities, counties and actions plotted on
a bar graph.

## Useful Links

[Sustainability Institute](https://si.tcnj.edu/)

[Markdown Cheatsheet](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet)

[GitHub Desktop Download](https://desktop.github.com/)

[Community List](http://www.sustainablejersey.com/fileadmin/media/Homepage/Final_11_X_17_SJ_Communities_Poster.pdf)
