from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
from myemail import Email
from sqlalchemy import exc
app = Flask(__name__)
app.secret_key = 'KeepItSecretKeepItSafe'
mysql = MySQLConnector(app,'emails_db')

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/success")
def success():
    query = "SELECT email, DATE_FORMAT(emails.created_at,'%M/%d/%Y') as date FROM emails" # define your query
    emails = mysql.query_db(query)# run query with query_db()
    return render_template("/success.html", all_emails=emails) # pass data to our template

@app.route('/create', methods=['POST'])
def create_email():
    try:
        # TODO: write a string function for email class
        email = request.form["email"]
        Email(email)
        query = "INSERT INTO emails (email, created_at, updated_at) VAlUES(:email, NOW(), NOW())"
        data = {
            "email": email
        }
        mysql.query_db(query, data)
    except exc.IntegrityError:
        flash("Duplicate Email")
        return redirect("/")
    except Exception as e:
        flash(str(e))
        return redirect("/")
    session["email"] = email
    return redirect("/success")
app.run(debug=True)
