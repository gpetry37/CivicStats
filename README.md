## CSC 315 Group 4 - CivicStats
#### Gordon Petry, Jason Kantner, Michael Williams, Casey Lishko

### Purpose:
Utilizing data pulled from sustainablejersey.com, this
program will allow to user to look at data between different
counties, municipalities, counties and actions plotted on
a bar graph.

### To run this program in the CSC 315 VM you first need to make the following one-time configuration changes:

#### Install Psycopg2 Python Package
`sudo apt-get update`  
`sudo apt-get install postgres-psycopg2`

#### The above commands may not work. Try running these instead:
`sudo apt-get install python3 libpq-dev python-dev python3-dev`  
`pip install psycopg2`

#### Set the PostgreSQL password for user 'osc'
`sudo -u postgres psql`  

* `ALTER USER osc PASSWORD 'osc';`  
* `\q`

#### Install Flask
`sudo apt-get install python-pip`  
`pip install flask`

#### Initialize Database
`. initialize_db.txt`

#### Logout, then login again to inherit new shell environment

### Usage:

#### Usage Debug Mode Off:
`export FLASK_APP=app.py`  
`flask run`
##### Then browse to http://127.0.0.1:5000/

#### Usage Debug Mode On:
`python app.py`
##### Then browse to http://127.0.0.1:5000/

### Database Source

[Sustainability Institute](https://si.tcnj.edu/)
