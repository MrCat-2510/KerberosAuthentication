from flask import Flask, render_template, request, flash, redirect
from Alice import Alice
from KDC import check_Token_status
from Privated_Key import decrypted
from KDC import KDC_name
from Key_Generate import create_privated_key
import sys
import sys


app = Flask(__name__)
app.secret_key = "Kerberos Authentication"
authentication = Alice()

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/", methods = ["POST", "GET"])
def home_access():
    if request.method == "POST":
        if((request.form['name_input'] == "Alice") and (request.form['password_input'] == '123')):
            try:
                authorization = authentication.get_access(request.form['Token_input'])
                if authorization:
                    flash(str(""), category='success')
                else:
                    flash(str(""), category='error1')
                return redirect("/")
            except:
                flash(str(""), category='error1')
                return redirect("/")
        else:
            flash(str(""), category='error')
            return redirect("/")
    else:
        return redirect("/")

@app.route("/Token")
def Token_Home():
    return render_template("Token.html")

@app.route("/Token", methods = ["POST", "GET"])
def Token_Get():
    if request.method == "POST":
        if((request.form['name_input'] == "Alice") and (request.form['password_input'] == '123')):
            try:
                Token = authentication.get_Token()
                flash(str(Token), category='success')
                return redirect("/Token")
            except:
                flash(str(""), category='error')
                return redirect("/Token")
        else:
            flash(str(""), category='error')
            return redirect("/Token")
    else:
        return redirect("/Token")

@app.route("/Checkstatus")
def Status_Home():
    return render_template("Status.html")
@app.route("/Checkstatus", methods = ["POST", "GET"])
def Check_Token():
    if request.method == "POST":
        try:
            timestamp, lefttime = check_Token_status(request.form['ticket_input'])
            if (timestamp != None):
                flash(str(str(lefttime) + " ||  Date created:" + timestamp), category='timestamp')
                return redirect("/Checkstatus")
            else:
                flash(str(""), category='error')
                return redirect("/Checkstatus")
        except:
            flash(str(""),category='error')
            return redirect("/Checkstatus")
    else:
        return redirect("/Checkstatus")

if __name__ == '__main__':
    app.run(debug=True)



