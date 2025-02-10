from flask import Flask,render_template,url_for,request,flash,redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin,login_user,LoginManager,current_user,login_required
from flask_bcrypt import Bcrypt


app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///user.db'
app.config['SECRET_KEY']="this is my key"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db=SQLAlchemy(app)
bcrypt=Bcrypt(app)
login_manager=LoginManager(app)
login_manager.login_view='login'

@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))

class User(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50),nullable=False)
    email=db.Column(db.String(80),nullable=False,unique=True)
    password=db.Column(db.String(80),nullable=False)

@app.route("/",methods=['GET','POST'])
def home():
    if request.method=='POST':
        name=request.form['name']
        email=request.form['email']
        password=request.form['password']
        hashed_password=bcrypt.generate_password_hash(password)
        if(User.query.filter_by(email=email).first()):
            flash("Email already exist")
            return redirect(url_for('register'))
        else: 
             user=User(name=name,email=email,password=hashed_password)
             db.session.add(user)
             db.session.commit()
             return redirect(url_for('login'))
    return render_template('register.html')


@app.route("/login",methods=['GET','POST'])
def login():
    if request.method=='POST':
        email=request.form['email']
        password=request.form['password']
        user=User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password,password):
            login_user(user)
            return redirect(url_for('dash'))
        else:
            flash("Invalid login")
            return redirect(url_for('login'))
    return  render_template('login.html')


@app.route("/dash")
def dash():
    return render_template('dash.html')

if __name__=='__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)