import os
import pytz
import flask
import smtplib
import pyrebase
from telebot import TeleBot
from datetime import datetime
from email.message import EmailMessage

API_KEY = os.getenv("API_KEY")

def send_email(to_mail, from_mail, passwd):
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(from_mail, passwd)

        mail = EmailMessage()
        
        mail["Subject"] = "MESSAGE RECEIVED"
        mail["From"] = from_mail
        mail["To"] = to_mail

        mail.add_alternative("""\
<!DOCTYPE html>
<html>
    <style>
        .container {
          width: auto;
          height: auto;
        }
        img {
          width: auto;
          height: auto;
          object-fit: contain;
        }
    </style>
    <body>
        <div class="container">
            <img src="https://i.stack.imgur.com/8xeHT.jpg">
        </div>
    </body>
</html>""", subtype="html")

        smtp.send_message(mail)

config = {
    "apiKey"            : os.getenv("apiKey"),
    "authDomain"        : os.getenv("authDomain"),
    "projectId"         : os.getenv("projectId"),
    "storageBucket"     : os.getenv("storageBucket"),
    "messagingSenderId" : os.getenv("messagingSenderId"),
    "appId"             : os.getenv("appId"),
    "databaseURL"       : os.getenv("databaseURL"),
    "measurementId"     : os.getenv("measurementId"),
}

app = flask.Flask(__name__)
bot = TeleBot(API_KEY, parse_mode="HTML")
firebase = pyrebase.initialize_app(config)
database = firebase.database()

@app.route('/')
def index():
    return flask.render_template("Home.html")

@app.route('/submit', methods=["POST"])
def contact():

    name    = flask.request.form["name"]
    email   = flask.request.form["email"]
    message = flask.request.form["message"]

    timestamp = datetime.now(pytz.timezone('Asia/Kolkata'))
    date = timestamp.strftime("%d-%m-%Y")
    time = timestamp.strftime("%H:%M")

    database.push({"name" : name, "email" : email,
        "message" : message, "date" : date, "time" : time})

    bot.send_message(-1001772806833, f"<b>🔔 NEW VIDEO REQUEST! 🔔\n\
        \nName: {name}\n\nEmail: {email}\n\nMessage: {message}\n\
        \nDate: {date}\t\tTime: {time}</b>")

    send_email(email, os.getenv("MAIL_ID"), os.getenv("SECRET_KEY"))

    return flask.redirect("/")

if __name__ == '__main__':
    app.run(debug=True)

