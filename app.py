from flask import flash, Flask, render_template, request
import requests
import sqlite3
from flask_mail import Mail, Message


app = Flask(__name__)
app.secret_key = "super secret key"
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
#mail id and password fields can be filled up and execution can be checked.
app.config['MAIL_USERNAME'] = '<<mail id to send mails from>>'
app.config['MAIL_PASSWORD'] = '<<password>>'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

@app.route('/', methods = ['GET', 'POST'])
def enlist():
    conn = sqlite3.connect('products')
    print ("Opened database successfully")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("select * from products order by product_id")
    rows = cur.fetchall()
    if request.method == 'POST':
        search_string = request.form.get("name")
        conn = sqlite3.connect('products')
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("select * from products where product_name='"+search_string+"';")
        search_data = cur.fetchall()
        if search_data != []:
            return render_template("enlist.html", rows=rows, search_data = search_data[0])
    return render_template("enlist.html", rows = rows)


@app.route('/mailer', methods = ['GET', 'POST'])
def mailer():
    if request.method=="POST":
       mail_id = request.form.get("mail_id")
       msg = Message('Hello', sender = 'clubdanfann@gmail.com', recipients = [mail_id])
       product_id=request.form["product_id"]
       product_name=request.form["product_name"]
       price=request.form["price"]
       msg.body = "The product you are intrested in is " + product_name +". It costs "+ price+" rupees. The unique id for the product is "+product_id
       mail.send(msg)
       return "Mail sent. Click <a href = '/'> here</a> to go back to home page."


if __name__ == "__main__":
    app.run()