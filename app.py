from flask import Flask, render_template, request, redirect
import mysql.connector



# MySQL Connection (XAMPP)
import random
import os
from urllib.parse import urlparse
 
app = Flask(__name__)
 
# 🔥 GET DATABASE URL
db_url = os.getenv("mysql://root:zGnVakCaTSnnnyOjEZqGQToNENUUhdLm@interchange.proxy.rlwy.net:35615/railway")
 
# 👉 fallback for local testing (IMPORTANT)
if not db_url:
    db_url = "mysql://root:zGnVakCaTSnnnyOjEZqGQToNENUUhdLm@interchange.proxy.rlwy.net:35615/railway"
 
url = urlparse(db_url)
 
# 🔥 DATABASE CONNECTION
db = mysql.connector.connect(
    host=url.hostname,
    user=url.username,
    password=url.password,
    database=url.path[1:],   # ✅ correct way (remove "/")
    port=url.port
)
 
cursor = db.cursor()

cursor = db.cursor(dictionary=True)

# HOME (READ)
@app.route('/')
def index():
    cursor.execute("SELECT * FROM customer")
    data = cursor.fetchall()
    return render_template('index.html', customers=data)

# CREATE
@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    mobile = request.form['mobile']
    amount = request.form['amount']
    location = request.form['location']

    sql = "INSERT INTO customer (name, mobile, amount, location) VALUES (%s, %s, %s, %s)"
    val = (name, mobile, amount, location)
    cursor.execute(sql, val)
    db.commit()

    return redirect('/')

# DELETE
@app.route('/delete/<string:mobile>')
def delete(mobile):
    cursor.execute("DELETE FROM customer WHERE mobile=%s", (mobile,))
    db.commit()
    return redirect('/')

# UPDATE (load data)
@app.route('/edit/<string:mobile>')
def edit(mobile):
    cursor.execute("SELECT * FROM customer WHERE mobile=%s", (mobile,))
    customer = cursor.fetchone()
    return render_template('index.html', edit_data=customer)

# UPDATE (submit)
@app.route('/update', methods=['POST'])
def update():
    name = request.form['name']
    mobile = request.form['mobile']
    amount = request.form['amount']
    location = request.form['location']

    sql = "UPDATE customer SET name=%s, amount=%s, location=%s WHERE mobile=%s"
    val = (name, amount, location, mobile)
    cursor.execute(sql, val)
    db.commit()

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)