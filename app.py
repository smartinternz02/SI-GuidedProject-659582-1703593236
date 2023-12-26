# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 00:41:34 2023

@author: Lenovo
"""

# =============================================================================
#from flask import Flask, render_template,request,url_for,redirect
from flask import *
from datetime import datetime

import ibm_db
# 
# 
app = Flask(__name__,template_folder='template')
conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=6667d8e9-9d4d-4ccb-ba32-21da3bb5aafc.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=30376;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=fqr84171;PWD=b9VLdFMZ1xDRiRKr;", '', '')

#@app.route("/", methods=['GET'])
@app.route("/")
def home():
    return render_template("home.html")


#@app.route("/login", methods=['GET'])
@app.route("/login")
def login():
    return render_template('login.html')

# # 
@app.route("/newuser")
def newuser():
    return render_template("newuser.html")
   
@app.route("/newsubmit",methods = ['POST'])
def newsubmit():
    x= [x for x in request.form.values()]
    Fname=x[0]
    Lname = x[1]
    Designation=x[2]
    Organisation = x[3]
    email=x[4]
    phone=x[5]
    password = x[6]
    sql = "SELECT * FROM FQR84171.REGISTER WHERE EMAIL = ?"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt, 1, email)
    ibm_db.execute(stmt)
    account = ibm_db.fetch_assoc(stmt)
    #print(account)
    if account:
        return render_template('login.html', pred="You are already a member, please login using your details")
    else:
        insert_sql = "INSERT INTO  REGISTER VALUES (?, ?, ?, ?, ?, ?, ?)"
        prep_stmt = ibm_db.prepare(conn, insert_sql)
        ibm_db.bind_param(prep_stmt, 1, Fname)
        ibm_db.bind_param(prep_stmt, 2, Lname) 
        ibm_db.bind_param(prep_stmt, 3, Designation)
        ibm_db.bind_param(prep_stmt, 4, Organisation)
        ibm_db.bind_param(prep_stmt, 5, email) 
        ibm_db.bind_param(prep_stmt, 6, phone)
        ibm_db.bind_param(prep_stmt, 7, password)
        ibm_db.execute(prep_stmt)
        return render_template('login.html', pred="Registration Successful, please login using your details")
      
 
 
@app.route('/submit',methods=['POST'])
def login1():
    email = request.form['email']
    password = request.form['password']
    sql = "SELECT * FROM REGISTER WHERE email =? AND password=?"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt,1,email)
    ibm_db.bind_param(stmt,2,password)
    ibm_db.execute(stmt)
    account = ibm_db.fetch_assoc(stmt)
    if account:
        return render_template('Booking.html',result=email)
    else:
        return render_template('login.html', pred="Login unsuccessful. Incorrect username/password !") 

@app.route('/book', methods=['POST'])
def book():
    p=request.form['pickup']
    d=request.form['drop']
    return render_template('Display.html',result=p,d=d,pred="Your Ride is Confirmed.. Our Person will call you shortly",datetime = str(datetime.now()))

@app.route('/cancel', methods=['POST'])
def cancel():
    p=""
    d=""
    return render_template('Display.html',result=p,d=d,predic="Your Ride is Cancelled",datetime = str(datetime.now()))


@app.route('/co2test', methods=['GET','POST'])
def co2test():
    return render_template('co2test.html')


 
if __name__ == "__main__":
    app.run(debug=True,port=5000)

