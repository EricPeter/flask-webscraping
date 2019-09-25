from flask import Flask ,render_template,redirect ,url_for, make_response,session,request,flash
from flask import jsonify
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager ,UserMixin,login_user,login_required,logout_user,current_user 
import requests
import time
import re
from database import  db_session 
from models import *
from models import Products as PD
from sqlalchemy.sql import exists
import smtplib
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError
#import mysql.connector
from passlib.hash import pbkdf2_sha256
import flask_login
from bs4 import BeautifulSoup ,NavigableString ,Comment

app = Flask(__name__)
app.secret_key='shutthefuckerup'
app.config['WTF_CSRF_SECRET_KEY'] = "b'f\xfa\x8b{X\x8b\x9eM\x83l\x19\xad\x84\x08\xaa"

# Initialize login manager
login = LoginManager(app)
login.init_app(app)

Bootstrap(app)

@login.user_loader
def load_user(id):
    return Login.query.get(int(id))

def RetrieveData():
	df = PD.query.all()
	return df
def compare():
	proddb=db_session.query(Products).all()
	bucketdb=Bucket.query.all()
	for x in bucketdb:
		for i in proddb:
			if x.image == i.image:
				current_price=float(i.product_price.replace(',',''))
				old_price=float(x.product_price.replace(',',''))
				# break
				if current_price < old_price:

					sendMail(x.image)
	
def sendMail(x):
	users=flask_login.current_user.Email
	server = smtplib.SMTP('smtp.gmail.com',587)
	server.ehlo()
	server.starttls()
	server.ehlo()

	server.login('kigaye.ericpeter@gmail.com','tfxcwzmgcjwdgsro')
	subject  = 'Price fell down!'
	body = x
	msg = f"Subject:{subject}\n\n{body}"

	server.sendmail(
		'kigaye.ericpeter@gmail.com',
		users,
		msg
		)

	server.quit()

	
@flask_login.login_required
@app.route('/home')
def home():
	while True:
		url = 'https://www.jumia.ug/computing/'
		response = requests.get(url)
		data = []
		soup = BeautifulSoup(response.content , 'html.parser')
		product_name = soup.find_all('span',{'class':'brand'})
		product_desc = soup.find_all('span',{'class':'name'}) 
		product_price = soup.find_all('span',{'class':'price-box ri'})
		images = soup.find_all('img',{'src':re.compile('.jpg')}) 
		product_discount = soup.find_all('div',{'class':'price-container clearfix'})
		first_child =soup.find_all('span',{'class':'price-box ri'} )
		#print(product_discount)
		children_data=[]
		for i in first_child:
			children = i.findChildren("span",recursive=True)[2]
			children_data.append(children)
		#print(children_data)
		for product in zip(images,product_name,product_desc,children_data,product_discount):
			images,name, desc ,price,discount= product
			products = {}
			products['Product_name']=name.text.strip()
			products['Product_desc']=desc.text.strip()
			products['Product_price']=price.text.strip()
			products['Image']=images['src']
			products['Product_discount'] = discount.text.strip()

			data.append(products)
			#print(products)
			#query =PD.query.all()replace('UGX', '')
			#for dt in query:
			if((db_session.query(exists().where(Products.product_name ==products['Product_name'])).scalar())&(db_session.query(exists().where(Products.product_desc ==products['Product_desc'])).scalar())):
				#print('Data already exists!')
				update_data = Products.query.filter_by(image=products['Image']).update(dict(product_price=products['Product_price']))
				db_session.commit()
				
				
			else:
				pd = Products(products['Product_name'],products['Product_desc'],products['Product_price'],products['Image'],products['Product_discount'])
				db_session.add(pd)
				db_session.commit()
		#print(data1)
		
		df=RetrieveData()
		compare()

		time.sleep(15)
		users=flask_login.current_user.Email
		return render_template('index.html',df=df,users=users)

@flask_login.login_required
@app.route('/phones')
def phones():
	while True:
		url = 'https://www.jumia.ug/phones-tablets/'
		response = requests.get(url)
		data = []
		soup = BeautifulSoup(response.content , 'html.parser')
		product_name = soup.find_all('span',{'class':'brand'})
		product_desc = soup.find_all('span',{'class':'name'}) 
		product_price = soup.find_all('span',{'class':'price-box ri'})
		images = soup.find_all('img',{'src':re.compile('.jpg')}) 
		product_discount = soup.find_all('div',{'class':'price-container clearfix'})
		first_child =soup.find_all('span',{'class':'price-box ri'} )
		#print(product_discount)
		children_data=[]
		for i in first_child:
			children = i.findChildren("span",recursive=True)[2]
			children_data.append(children)
		#print(children_data)
		for product in zip(images,product_name,product_desc,children_data,product_discount):
			images,name, desc ,price,discount= product
			products = {}
			products['Product_name']=name.text.strip()
			products['Product_desc']=desc.text.strip()
			products['Product_price']=price.text.strip()
			products['Image']=images['src']
			products['Product_discount'] = discount.text.strip()
			data.append(products)
			#print(products)
			#query =PD.query.all()replace('UGX', '')
			#for dt in query:
			if((db_session.query(exists().where(Products.product_name ==products['Product_name'])).scalar())&(db_session.query(exists().where(Products.product_desc ==products['Product_desc'])).scalar())):
				#print('Data already exists!')
				update_data = Phones.query.filter_by(image=products['Image']).update(dict(product_price=products['Product_price']))
				db_session.commit()
				
				
			else:
				pd = Phones(products['Product_name'],products['Product_desc'],products['Product_price'],products['Image'],products['Product_discount'])
				db_session.add(pd)
				db_session.commit()
		#print(data1)
		
		df = Phones.query.all()
		compare()
		time.sleep(10)
		users=flask_login.current_user.Email
		return render_template('phones.html',df=df,users=users)
@flask_login.login_required
@app.route('/fashion')
def fashion():
	while True:
		url = 'https://www.jumia.ug/video-games/'
		response = requests.get(url)
		data = []
		soup = BeautifulSoup(response.content , 'html.parser')
		product_name = soup.find_all('span',{'class':'brand'})
		product_desc = soup.find_all('span',{'class':'name'}) 
		product_price = soup.find_all('span',{'class':'price-box ri'})
		images = soup.find_all('img',{'src':re.compile('.jpg')}) 
		product_discount = soup.find_all('div',{'class':'price-container clearfix'})
		first_child =soup.find_all('span',{'class':'price-box ri'} )
		#print(product_discount)
		children_data=[]
		for i in first_child:
			children = i.findChildren("span",recursive=True)[2]
			children_data.append(children)
		#print(children_data)
		for product in zip(images,product_name,product_desc,children_data,product_discount):
			images,name, desc ,price,discount= product
			products = {}
			products['Product_name']=name.text.strip()
			products['Product_desc']=desc.text.strip()
			products['Product_price']=price.text.strip()
			products['Image']=images['src']
			products['Product_discount'] = discount.text.strip()
			print(products['Product_name'])
			data.append(products)
			#print(products)
			#query =PD.query.all()replace('UGX', '')
			#for dt in query:
			if((db_session.query(exists().where(Products.product_name ==products['Product_name'])).scalar())&(db_session.query(exists().where(Products.product_desc ==products['Product_desc'])).scalar())):
				#print('Data already exists!')
				update_data = Fashion.query.filter_by(image=products['Image']).update(dict(product_price=products['Product_price']))
				db_session.commit()
				
				
			else:
				pd = Fashion(products['Product_name'],products['Product_desc'],products['Product_price'],products['Image'],products['Product_discount'])
				db_session.add(pd)
				db_session.commit()
		#print(data1)
		
		df = Fashion.query.all()
		compare()

		time.sleep(10)
		users=flask_login.current_user.Email
		return render_template('Fashion.html',df=df,users=users)

@flask_login.login_required
@app.route('/bucket',methods=['GET','POST'])
def bucket():
	user=flask_login.current_user.Email
	if request.method == 'POST':
		product = request.form['product_name']
		price = request.form['product_price']
		desc=request.form['product_desc']
		image= request.form['image_name']

		if((db_session.query(exists().where(Bucket.product_name ==product)).scalar())&(db_session.query(exists().where(Bucket.username==user)).scalar())):
			 flash('Product already exists','error')
		else:
			item = Bucket(product_name=product,product_desc=desc,product_price=price,image=image,username=user)
			db_session.add(item)
			db_session.commit()
	bucket_items = Bucket.query.filter_by(username=user)
	counts= Bucket.query.filter_by(username=user).count()
	return render_template('bucket.html',bucket_items=bucket_items,users=user,counts=counts)
#deleting from the bucket
@flask_login.login_required
@app.route('/delete',methods=['GET','POST'])
def delete():
	user=flask_login.current_user.Email
	if request.method == 'POST':
		product = request.form['product_name']
		price = request.form['price']
		bucket_items = Bucket.query.filter_by(username=user,product_price=price,product_name=product).first()
		db_session.delete(bucket_items)
		db_session.commit()
	return redirect(url_for('bucket'))

##register and login
def invalid_credentials(form, field):
    """ Username and password checker """

    password = field.data
    email= form.email.data

    # Check username is invalid
    user_data = Login.query.filter_by(Email=email).first()
    if user_data is None:
        raise ValidationError("Email or password is incorrect")

    # Check password in invalid
    elif not pbkdf2_sha256.verify(password, user_data.Password):
        raise ValidationError("Email or password is incorrect")


class RegistrationForm(FlaskForm):
    """ Registration form"""

    email = StringField('email', validators=[InputRequired(message="Email required"), Length(min=4, max=100, message="Email must be between 4 and 25 characters")])
    password = PasswordField('password', validators=[InputRequired(message="Password required"), Length(min=4, max=25, message="Password must be between 4 and 25 characters")])
    confirm_pswd = PasswordField('confirm_pswd', validators=[InputRequired(message="Password required"), EqualTo('password', message="Passwords must match")])

    def validate_Email(self, email):
        user_object = Login.query.filter_by(email=email.data).first()
        if user_object:
            raise ValidationError("Email already exists. use a different email.")

class LoginForm(FlaskForm):
    """ Login form """

    email = StringField('email', validators=[InputRequired(message="Email required")])
    password = PasswordField('password', validators=[InputRequired(message="Password required"), invalid_credentials])


###Register
@app.route("/register", methods=['GET', 'POST'])
def register():

    reg_form = RegistrationForm()

    # Update database if validation success
    if reg_form.validate_on_submit():
        email = reg_form.email.data
        password = reg_form.password.data

        # Hash password
        hashed_pswd = pbkdf2_sha256.hash(password)

        # Add username & hashed password to DB
        user = Login(Email=email, Password=hashed_pswd)
        db_session.add(user)
        db_session.commit()

        flash('Registered successfully. Please login.', 'success')
        return redirect(url_for('login'))

    return render_template("register.html", form=reg_form)

# @app.route("/", methods=['GET', 'POST'])
# def login():
# 	login_form = LoginForm()
#     # Allow login if validation success
#     if login_form.validate_on_submit():
#     	user_object =Login.query.filter_by(Email=login_form.email.data).first()
#     	# print(login_form.email.data)
#     	login_user(user_object)
#     	session['logged_in'] =True
#         # login_user(user_object, remember=form.remember_me.data)
#         return redirect(url_for('home'))
#     return render_template("login.html", form=login_form)

@app.route("/",methods=['GET','POST'])
def login():
	login_form=LoginForm()
	if login_form.validate_on_submit():
		user_object=Login.query.filter_by(Email=login_form.email.data).first()
		login_user(user_object)
		session['logged_in']=True
		flask_login.login_user(user_object)
		return redirect(url_for('home'))
	return render_template("login.html",form=login_form)

	

@app.route("/logout", methods=['GET'])
def logout():

    # Logout user
    logout_user()
    flash('You have logged out successfully', 'success')
    return redirect(url_for('login'))


# if __name__ == "__main__":
#    app.run(debug=True, host='127.0.0.1', port=5000)
