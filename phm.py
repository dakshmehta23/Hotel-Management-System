from flask import Flask,render_template
from flask import Flask, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from wtforms import Form, BooleanField, StringField, IntegerField, validators
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


app = Flask(__name__)
app.config['SECRET_KEY']='HELLO WORLD'
app.config['FLASK_ADMIN_SWATCH'] = 'Cyborg'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONs'] = False
admin = Admin(app, name='PHM', template_mode='bootstrap3')
db=SQLAlchemy(app)


class User(db.Model):
	_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name=db.Column(db.String(20),nullable=False)
	email = db.Column(db.String(120), nullable=False)
	phone = db.Column(db.Integer(),nullable=False)
	checkin=db.Column(db.String(15),nullable=False)
	checkout=db.Column(db.String(15),nullable=False)
	rtypeA=db.Column(db.Boolean())
	rtypeB=db.Column(db.Boolean())
	rtypeC=db.Column(db.Boolean())
	rtypeD=db.Column(db.Boolean())
	

	def __init__(self, name, email, phone,checkin,checkout,rtypeA,rtypeB,rtypeC,rtypeD):
		self.name = name
		self.email = email
		self.phone = phone
		self.checkin=checkin
		self.checkout=checkout
		self.rtypeA = rtypeA
		self.rtypeB = rtypeB
		self.rtypeC = rtypeC
		self.rtypeD = rtypeD
		
	



admin.add_view(ModelView(User, db.session))

class RegistrationForm(Form):
	name= StringField('Name',[validators.DataRequired()])
	email = StringField('Email Address', [validators.Length(min=6, max=35),validators.Email(message="Invalid Email")])
	phone = IntegerField('Phone Number', [validators.NumberRange(min=1111111111,max=9999999999),validators.DataRequired()])
	checkin= StringField('CHECK-IN DATE',[validators.Length(min=8,max=10),validators.DataRequired()])
	checkout = StringField('CHECK_OUT DATE',[validators.Length(min=8,max=10),validators.DataRequired()])
	rtypeA = BooleanField('Suite ')
	rtypeB = BooleanField('Super Deluxe')
	rtypeC = BooleanField('Deluxe')
	rtypeD= BooleanField('Economy')






db.create_all()

@app.route('/')
@app.route("/home")
def home():
	return render_template('home.html')
@app.route("/contact")
def contact():
	return render_template('contact.html')





@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(form.name.data, form.email.data,
                    form.phone.data,form.checkin.data,form.checkout.data,form.rtypeA.data,form.rtypeB.data,form.rtypeC.data,form.rtypeD.data)
        db.session.add(user)
        db.session.commit()
        
        return redirect(url_for('home'))
    return render_template('register.html', form=form)


@app.route("/details")
def details():
	return render_template('details.html')

@app.route("/admin1",methods=['GET','POST'])
def admin1():
	error = None
	if request.method == 'POST':
		if request.form['username'] == 'admin' or request.form['password'] == 'admin':
			return redirect('/admin/user')
		
	return render_template('admin.html')




#TESTTTTTT

if __name__ == '__main__':
   app.run(debug = True)
