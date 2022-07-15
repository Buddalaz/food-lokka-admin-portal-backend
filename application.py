from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
import json
from dataclasses import dataclass

application = Flask(__name__)
application.config['SECRET_KEY'] = 'some_random_secret'
db_path = os.path.join(os.path.dirname(__file__), 'food_lokka.db')


application.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(application)

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
    area: str
    resturentName: str
    street: str
    locationLink: str
    city: str
    zipCode: str
    country: str
    phone: str
    meals: str
    priceRange: str
    userId: int

    id = db.Column(db.Integer, primary_key=True)
    area = db.Column(db.String(80), nullable=False)
    resturentName = db.Column(db.String(80), nullable=False)
    street = db.Column(db.String(120), nullable=False)
    locationLink = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    zipCode = db.Column(db.String(120), nullable=False)
    country = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    meals = db.Column(db.String(120), nullable=False)
    priceRange = db.Column(db.String(120), nullable=False)
    userId = db.Column(
        db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, area, resturentName, street, locationLink, city, zipCode, country, phone, meals, priceRange, userId) -> None:
        super().__init__()
        self.area = area
        self.resturentName = resturentName
        self.street = street
        self.locationLink = locationLink
        self.city = city
        self.zipCode = zipCode
        self.country = country
        self.phone = phone
        self.meals = meals
        self.priceRange = priceRange
        self.userId = userId

    def __repr__(self) -> str:
        return f"Resturent : ['id'=> {self.id}, 'resturent_name' => {self.resturent_name}, 'address' => {self.address}, 'password' => {self.password}, , 'user_id' => {self.user_id} ]"


db.create_all()


@application.route("/")
def index():
    return render_template('login.html')


@application.route('/dash', methods=['GET'])
def route_dash():
    return render_template('index.html')


@application.route("/save-user", methods=["POST"])
def saveUser():
    req = request.get_json()

    # save users details
    user = User(username=req['userName'],
                email=req['email'], password=req['password'])
    db.session.add(user)
    db.session.commit()

    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@application.route("/get-user/<username>", methods=["GET"])
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


@application.route("/get-resturents", methods=["GET"])
def getAllResturentDetails():
    try:
        resturents = db.session.query(Resturent).all()
        return jsonify({'status': 'Success', 'data': resturents}), 200
    except Exception as e:
        return jsonify({'status': 'Fail', 'data': e.__cause__}), 400


@application.route("/save-resturents", methods=["POST"])
def saveResturent():

    req = request.get_json()

    area = req['area']
    resturent_name = req['resturentName']
    street = req['street']
    loca_link = req['locationLink']
    city = req['city']
    zip_code = req['zipCode']
    country = req['country']
    phone = req['phoneNumber']
    meals = req['meals']
    price_range = req['priceRange']
    user_id = req['userId']

    # save resturent details
    if area != None and resturent_name != None and street != None and loca_link != None:
        resturent = Resturent(area=area, resturentName=resturent_name, street=street, locationLink=loca_link, city=city,
                              zipCode=zip_code, country=country, phone=phone, meals=meals, priceRange=price_range, userId=user_id)
        db.session.add(resturent)
        db.session.commit()
        return jsonify({'status': 'Success'})
    else:
        return jsonify({'status': 'Fail'})


@application.route("/update-resturents", methods=["PUT"])
def update():
    try:
        data = request.get_json()
        db.session.query(Resturent).filter_by(id=id).update(
            dict(description=data.itemDesc, unit_price=data.itemPrice, qty=data.itemQty))
        db.session.commit()
        return jsonify({'status': 'Success'}), 200
    except Exception as e:
        return jsonify({'status': 'Fail', 'data': e.__cause__}), 400


@application.route("/delete-resturents/<restId>", methods=["DELETE"])
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
    application.run(debug=True)
