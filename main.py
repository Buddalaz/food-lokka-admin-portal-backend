from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

db_path = os.path.join(os.path.dirname(__file__), 'food_lokka.db')


app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
db = SQLAlchemy(app)

# cerate databases


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=True, nullable=False)
    # lastUpdateDateTime = db.Column(db.String(120), unique=True, nullable=False)


db.create_all()


@app.route("/")
def index():
    return "Hello world"


@app.route("/get-resturents", methods=["GET"])
def getAllResturentDetails():
    return "Hello world"


@app.route("/save-resturents")
def save():
    return "Hello world"


@app.route("/update-resturents")
def update():
    return "Hello world"


@app.route("/delete-resturents")
def delete():
    return "Hello world"


if __name__ == "__main__":
    app.run(debug=True)
