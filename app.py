from flask import Flask ,render_template,redirect ,url_for, make_response,session,request
from flask import jsonify
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager ,UserMixin,login_user,login_required,logout_user,current_user 
import requests
import time
from database import  db_session 
from models import Products , Bucket
from models import Products as PD
from sqlalchemy.sql import exists
import smtplib
#import mysql.connector
from bs4 import BeautifulSoup ,NavigableString ,Comment

app = Flask(__name__)

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
					sendMail()
	
def sendMail():
	server = smtplib.SMTP('smtp.gmail.com',587)
	server.ehlo()
	server.starttls()
	server.ehlo()

	server.login('kigaye.ericpeter@gmail.com','tfxcwzmgcjwdgsro')
	subject  = 'Price fell down!'
	body = 'check out the link https://www.jumia.ug/computing/'
	msg = f"Subject:{subject}\n\n{body}"

	server.sendmail(
		'kigaye.ericpeter@gmail.com',
		'tobiusaolo21@gmail.com',
		msg
		)
	print('HEY EMAIL HAS BEEN SENT!')
	server.quit()

	# p1 = proddb.product_price
	# print(p1)
	# p2 = bucketdb.product_price

	# if p2 < p1:
	# 	print('buy now')
	# else:
	# 	print('its still high')

@app.route('/')
def index():
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
		#time.sleep(10)
		
		return render_template('index.html',df=df)

@app.route('/bucket',methods=['GET','POST'])
def bucket():
	if request.method == 'POST':
		product = request.form['product_name']
		price = request.form['product_price']
		desc=request.form['product_desc']
		image= request.form['image_name']
		item = Bucket(product_name=product,product_desc=desc,product_price=price,image=image)
		db_session.add(item)
		db_session.commit()
		

	bucket_items = Bucket.query.all()
	return render_template('bucket.html',bucket_items=bucket_items)



#if __name__ == "__main__":
 #   app.run(debug=True, host='127.0.0.1', port=5000)
