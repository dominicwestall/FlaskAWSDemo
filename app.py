import os
import psycopg2
from flask import Flask, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Init App
app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisissecret'

# our database uri
if 'RDS_DB_NAME' in os.environ:
    app.config['SQLALCHEMY_DATABASE_URI'] = \
        'postgresql://{username}:{password}@{host}:{port}/{database}'.format(
        username=os.environ['RDS_USERNAME'],
        password=os.environ['RDS_PASSWORD'],
        host=os.environ['RDS_HOSTNAME'],
        port=os.environ['RDS_PORT'],
        database=os.environ['RDS_DB_NAME'],
    )
else:
    # our database uri
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://domadmin:2021Shades@localhost:5432/contacts_demo_db"

db = SQLAlchemy()
db.init_app(app)
migrate = Migrate(app, db)

# Create A Model For Table
class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(1000))
    last_name = db.Column(db.String(1000))
    email_address = db.Column(db.String(500))
    mobile = db.Column(db.String(30))
    home_address = db.Column(db.String(1000))
    url_of_picture = db.Column(db.String(1000))

class Login(db.Model):
    __tablename__ = 'login'
    id = db.Column(db.Integer, primary_key=True)
    access_code = db.Column(db.Integer)
    email_address = db.Column(db.String(500))

@app.route('/', methods=['GET'])
def index():
   
    #userdata = Users.query.all()
    usersdata = db.session.execute(db.select(Users).order_by(Users.id)).scalars()
    return render_template('users.html', usersdata=usersdata)

@app.route('/users', methods=['GET'])
def users():
   
    #userdata = Users.query.all()
    usersdata = db.session.execute(db.select(Users).order_by(Users.id)).scalars()
    return render_template('users.html', usersdata=usersdata)

@app.route('/registeruser', methods=['GET', 'POST'])
def registeruser():

    if request.method == "POST":

        # get user data
        firstnameData = request.form['firstname']
        lastnameData = request.form['lastname']
        emailaddressData = request.form['emailaddress']
        mobileData = request.form['mobilephone']
        homeaddressData = request.form['homeaddress']
        pictureData = request.form['picture']

        # populate database
        newUser = Users(first_name=firstnameData, last_name=lastnameData, email_address=emailaddressData, 
                           mobile=mobileData, home_address=homeaddressData, url_of_picture=pictureData)
        db.session.add(newUser)
        db.session.commit()

        usersdata = db.session.execute(db.select(Users).order_by(Users.id)).scalars()
        return render_template('users.html', usersdata=usersdata)
        #return "<h4>User created</h4>"
    return render_template('register.html')

@app.route('/loginuser', methods=['GET', 'POST'])
def loginuser():
    if request.method == "POST":
        #get login data
        accesscodeData = request.form['accesscode']
        # database lookup
        
        user = Login.query.filter_by(access_code=accesscodeData).first()
        if user:
            usersdata = db.session.execute(db.select(Users).order_by(Users.id)).scalars()
            return render_template('users.html', usersdata=usersdata)
        elif not user:
            return "<h4>Login failed</h4>"

    return render_template('login.html')

@app.route('/registeralogin', methods=['GET', 'POST'])
def registeralogin():
    if request.method == "POST":
        accesscodeData = request.form['accesscode']
        emaiiladdressData = request.form['emailaddress']

        newLogin = Login(access_code=accesscodeData, email_address=emaiiladdressData)
        db.session.add(newLogin)
        db.session.commit()

        return "<h4>Login created successfully</h4>"

    return render_template('register_login.html')

@app.route('/edit', methods=['POST', 'GET'])
def edit():
    # trying to mimic the MS page load and page post back events.
    if request.method == "GET":
        userid = request.args.get('ID')
        userdata = db.session.execute(db.select(Users).filter_by(id=userid)).scalar_one()
        return render_template('edit.html', userdata=userdata)
        #return '<h1>' + userdata.first_name + '</h1>'
    elif request.method == "POST":
        userid = request.args.get('ID')
        userdatatochange = db.session.execute(db.select(Users).filter_by(id=userid)).scalar_one()
       
        updatedhomeaddressofuser = request.form['homeaddress']
        updatedfirstnameofuser = request.form['firstname']
        updatedemailaddressofuser = request.form['emailaddress']

        userdatatochange.home_address = updatedhomeaddressofuser
        userdatatochange.first_name = updatedfirstnameofuser
        userdatatochange.email_address = updatedemailaddressofuser
        db.session.commit()
        # update the database.
        return '<h1>' + userdatatochange.email_address + '</h1>'
        #return index()

@app.route('/deletecheck', methods=['POST', 'GET'])
def deletecheck():
    
    if request.method == "GET":
        #get the user data from the DB.
        userid = request.args.get('ID')
        userdata = db.session.execute(db.select(Users).filter_by(id=userid)).scalar_one()
        #send to the page
        return render_template('delete_check.html', userdata=userdata)
    return "<h4>User delete page</h4>"    

@app.route('/deleteproceed', methods=['GET', 'POST'])
def deleteproceed():

    if request.method == "GET":
        #get the user data from the DB.
        userid = request.args.get('ID')
        userdata = db.session.execute(db.select(Users).filter_by(id=userid)).scalar_one()
        
        print(userdata.id)
        print(userdata.first_name)
        # delete the record
        db.session.delete(userdata)
        db.session.commit()

        # rerun the users page
        usersdata = db.session.execute(db.select(Users).order_by(Users.id)).scalars()
        return render_template('users.html', usersdata=usersdata)
        
    return "<h4>User delete page</h4>" 

# Run the Flask app if this script is the main entry point
if __name__ == '__main__':
    #with app.app_context():
        #db.create_all() # <--- create db object.
    app.run(debug=True)