import psycopg2 as ps
import pandas as p
from flask import Flask , request,redirect,url_for
con = ps.connect(user="postgres",password=1474,host="localhost",port=5432,database="new")
cur = con.cursor()
app = Flask(__name__)

@app.route('/',methods = ['POST','GET'])
def st():
    if request.method == 'POST' :
        choice = request.form.get('choice')
        if choice == 'create':
           return redirect(url_for('create'))
        elif choice == 'add':
            return redirect(url_for('add'))
        elif choice == 'update':
            return redirect(url_for('update'))
        elif choice == 'staff':
            return redirect(url_for('staff'))
        elif choice == 'user':
            return redirect(url_for('user'))
        elif choice == 'delete':
            return redirect(url_for('delete'))
        else :
            return redirect(url_for('st'))


    return '''<h2>To ADD  a user enter --add--  </h2>
              <h2>To UPDATE a user enter --update--  </h2>
              <h2>To SEE all users enter --staff--   </h2>
              <h2>To SEE  a user enter --user--  </h2>
              <h2>To CREATE a table  --create--  </h2>
              <h2>To DELETE a table  --delete--  </h2>
              <form method = "POST">
              choice <input type = "text" name = "choice">
              <input type = "submit">
              </form>'''
@app.route('/create',methods = ['POST','GET'])
def create():
    if request.method == 'POST' :
        tlname = request.form.get('tlname')
        try :

           if tlname is not None:
                cbq = """CREATE TABLE  """ + tlname + """(ID INT PRIMARY KEY     NOT NULL, NAME   TEXT   DEFAULT NULL,EMAIL   varchar(45)   DEFAULT NULL,PASSWORD varchar(255) DEFAULT NULL);"""
                cur.execute(cbq)
                con.commit()
                return redirect(url_for('st'))
           else :
               return '''<h1>ENTER table name <h1> 
                        <form method = "POST" action = "http://127.0.0.1:5000/create">
                        <input type = "submit" name = "Renter">
                        </form>'''
        except Exception as e :
            cur.close()
            con.close()
            return e



    return '''<h1>Enter Table Name  </h1>
              <h1>Default constraints are  id,name,email,passowrd</h1>
              <form method = "POST">
               tlname <input type = "text" name = "tlname">
              <input type = "submit">
              </form>'''
@app.route('/add',methods = ['POST','GET'])
def add():
    if request.method == 'POST' :
        tlname = request.form.get('tlname')
        ID = request.form.get('ID')
        NAME = request.form.get('NAME')
        EMAIL = request.form.get('EMAIL')
        PASSWORD = request.form.get('PASSWORD')
        PASSWORD = PASSWORD.encode(encoding='UTF-8', errors='strict')
        try :
           if tlname is not None:
               isq = """ INSERT INTO  """ + tlname + """(ID, NAME, EMAIL,PASSWORD) VALUES (%s,%s,%s,%s)"""
               val = (ID, NAME, EMAIL,PASSWORD)
               cur.execute(isq, val)
               con.commit()
               return ''' <h1> Table Created</h1>
                          <h1> Return to main page</h1>
                          <form method = "POST" action = "http://127.0.0.1:5000/">
                          <input type = "submit" name = "OK">
                          </form>'''
           else :
               return '''<h1>ENTER table name <h1> 
                        <form method = "POST" action = "http://127.0.0.1:5000/add">
                        <input type = "submit" name = "Renter">
                        </form>'''
        except Exception as e :
            cur.close()
            con.close()
            return e


    return '''<h1>Enter Table Name  </h1>
              <h1>Default constraints are  id,name,email,passowrd</h1>
              <form method = "POST">
              Table Name  <input type = "text" name = "tlname">
              ID  <input type = "text" name = "ID">
              NAME  <input type = "text" name = "NAME">
              EMAIL  <input type = "text" name = "EMAIL">
              PASSWORD  <input type = "text" name = "PASSWORD">
              <input type = "submit">
              </form>'''
@app.route('/update',methods = ['POST','GET'])
def update():
    if request.method == 'POST' :
        tlname = request.form.get('tlname')
        ID = request.form.get('ID')
        CHNAME = request.form.get('CHNAME')
        VALUE = request.form.get('VALUE')
        if CHNAME == "PASSOWRD":
                VALUE =VALUE.encode(encoding='UTF-8', errors='strict')
        try :
                if tlname is not None:
                    upq = """UPDATE """ + tlname + """ SET """ + CHNAME + """ = %s where ID = %s"""
                    cur.execute(upq, (VALUE, ID))
                    con.commit()
                    return ''' <h1> TABLE UPDATED</h1>
                               <h1> Return to main page</h1>
                               <form method = "POST" action = "http://127.0.0.1:5000/">
                               <input type = "submit" name = "OK">
                                </form>'''
                else :
                    return '''<h1>ENTER table name <h1> 
                             <form method = "POST" action = "http://127.0.0.1:5000/update">
                             <input type = "submit" name = "Renter">
                             </form>'''
        except Exception as e :
                cur.close()
                con.close()
                return e


    return '''<h1>Enter Table Name  </h1>
              <h1>Default constraints are  id,name,email,passowrd</h1>
              <form method = "POST">
              Table Name  <input type = "text" name = "tlname">
              ID  <input type = "text" name = "ID">
              CHNAME  <input type = "text" name = "CHNAME">
              VALUE  <input type = "text" name = "VALUE">
              <input type = "submit">
              </form>'''
@app.route('/staff',methods = ['POST','GET'])
def staff():
    if request.method == 'POST' :
        tlname = request.form.get('tlname')
        try :
           if tlname is not None:
                slq = """select * from  """ + tlname
                l = p.read_sql(slq, con=con)
                #record = cur.fetchall()
                #l = p.DataFrame(record)
                #con.commit()
                return l.to_html(),'''<form method = "POST" action = "http://127.0.0.1:5000/">
                        <input type = "submit" name = "OK">
                        </form>'''
           else :
               return '''<h1>ENTER table name <h1> 
                        <form method = "POST" action = "http://127.0.0.1:5000/staff">
                        <input type = "submit" name = "Renter">
                        </form>'''
        except Exception as e :
            cur.close()
            con.close()
            return e

    return '''<h1>Enter Table Name  </h1>
              <form method = "POST">
              Table Name  <input type = "text" name = "tlname">
              <input type = "submit">
              </form>'''
@app.route('/user',methods = ['POST','GET'])
def user():
    if request.method == 'POST' :
        tlname = request.form.get('tlname')
        ID = request.form.get('ID')
        try :
           if tlname is not None:
                stl = "SELECT * FROM "+ tlname + " WHERE ID=%s"
                cur.execute(stl, ID)
                row = cur.fetchone()
                l = p.DataFrame(row)
                con.commit()
                return l.to_html(),''' <form method = "POST" action = "http://127.0.0.1:5000/">
                        <input type = "submit" name = "OK">
                        </form>'''
           else :
               return '''<h1>ENTER table name <h1> 
                        <form method = "POST" action = "http://127.0.0.1:5000/user">
                        <input type = "submit" name = "Renter">
                        </form>'''
        except Exception as e :
            cur.close()
            con.close()
            return e

    return '''<h1>Enter Table Name  </h1>
              <form method = "POST">
              Table Name  <input type = "text" name = "tlname">
              ID  <input type = "text" name = "ID">
              <input type = "submit">
              </form>'''
@app.route('/delete',methods = ['POST','GET'])
def delete():
    if request.method == 'POST' :
        tlname = request.form.get('tlname')
        try :
           if tlname is not None:
                cbq = """DROP TABLE  """ + tlname
                cur.execute(cbq)
                con.commit()
                return ''' <h1> Table deleted</h1>
                        <h1> Return to main page</h1>
                        <form method = "POST" action = "http://127.0.0.1:5000/">
                        <input type = "submit" name = "OK">
                        </form>'''
           else :
               return '''<h1>ENTER table name <h1> 
                        <form method = "POST" action = "http://127.0.0.1:5000/user">
                        <input type = "submit" name = "Renter">
                        </form>'''
        except Exception as e :
            cur.close()
            con.close()
            return e

    return '''<h1>Enter Table Name  </h1>
              <form method = "POST">
              Table Name  <input type = "text" name = "tlname">
              <input type = "submit">
              </form>'''

if __name__ == "__main__":
    app.run(debug = True )