from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
import json
from dataclasses import dataclass

app = Flask(__name__)

db_path = os.path.join(os.path.dirname(__file__), 'food_lokka.db')


app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
db = SQLAlchemy(app)

# cerate databases


@dataclass
class User(db.Model):
    id: int
    username: str
    email: str
    password: str

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=True, nullable=False)
    # lastUpdateDateTime = db.Column(db.String(120), unique=True, nullable=False)
    resturent = db.relationship(
        'Resturent', backref=db.backref('user', lazy=True))

    def __init__(self, username, email, password) -> None:
        super().__init__()
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self) -> str:
        return f"User : ['id'=> {self.id}, 'username' => {self.username}, 'email' => {self.email}, 'password' => {self.password} ]"


@dataclass
class Resturent(db.Model):

    id: int
    resturent_name: str
    address: str
    password: str
    user_id: int

    id = db.Column(db.Integer, primary_key=True)
    resturent_name = db.Column(db.String(80), unique=True, nullable=False)
    address = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=True, nullable=False)
    # lastUpdateDateTime = db.Column(db.String(120), unique=True, nullable=False)
    user_id = db.Column(
        db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, resturent_name, address, password, user_id) -> None:
        super().__init__()
        self.resturent_name = resturent_name
        self.address = address
        self.password = password
        self.user_id = user_id

    def __repr__(self) -> str:
        return f"Resturent : ['id'=> {self.id}, 'resturent_name' => {self.resturent_name}, 'address' => {self.address}, 'password' => {self.password}, , 'user_id' => {self.user_id} ]"


db.create_all()


@app.route("/save-user", methods=["POST"])
def saveUser():
    req = request.get_json()

    # save users details
    user = User(username=req['userName'],
                email=req['email'], password=req['password'])
    db.session.add(user)
    db.session.commit()

    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route("/get-user/<username>", methods=["GET"])
def getUserDetails(username):
    try:
        result = User.query.filter_by(username=username).first()
        response_data = {
            "email": result.email,
            "username": result.username,
            "password": result.password
        }
        return jsonify({'status': 'Success', 'data': response_data}), 200
    except Exception as e:
        return jsonify({'status': 'Fail', 'data': e.__cause__}), 400


@app.route("/get-resturents", methods=["GET"])
def getAllResturentDetails():
    try:
        resturents = db.session.query(Resturent).all()
        return jsonify({'status': 'Success', 'data': resturents}), 200
    except Exception as e:
        return jsonify({'status': 'Fail', 'data': e.__cause__}), 400


@app.route("/save-resturents", methods=["POST"])
def saveResturent():

    req = request.get_json()
    resturent_name = req['resturent_name']
    address = req['address']
    password = req['password']
    user_id = req['user_id']
    # save resturent details
    if resturent_name != None and address != None and password != None and user_id != None:
        resturent = Resturent(resturent_name=resturent_name,
                              address=address, password=password, user_id=user_id)
        db.session.add(resturent)
        db.session.commit()
        return jsonify({'status': 'Success'})
    else:
        return jsonify({'status': 'Fail'})

    # if resturent is None:
    #     return json.dumps({'success': False}), 500, {'ContentType': 'application/json'}
    # else:
    #     return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route("/update-resturents", methods=["PUT"])
def update():
    try:
        data = request.get_json()
        db.session.query(Resturent).filter_by(id=id).update(
            dict(description=data.itemDesc, unit_price=data.itemPrice, qty=data.itemQty))
        db.session.commit()
        return jsonify({'status': 'Success'}), 200
    except Exception as e:
        return jsonify({'status': 'Fail', 'data': e.__cause__}), 400


@app.route("/delete-resturents/<restId>", methods=["DELETE"])
def delete(restId):
    # print(type(restId))
    deleteId = int(restId)
    print(type(deleteId))
    try:
        db.session.query(Resturent).filter(id == deleteId).delete()
        db.session.commit()
        db.session.flush()
        return jsonify({'status': 'Success'}), 200
    except Exception as e:
        return jsonify({'status': 'Fail', 'data': e.__cause__}), 400


if __name__ == "__main__":
    app.run(debug=True)
