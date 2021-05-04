import re
#import logging
import time
import os
from random import randint
from flask import *
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import *

app=Flask(__name__,instance_relative_config=True)




app.config.from_mapping(SECRET_KEY='dev',DATABASE=os.path.join(app.instance_path,'F:/Program Files/Microsoft SQL Server/MSSQL15.MSSQLSERVER/MSSQL'))

app.config['SQLALCHEMY_ECHO'] = True

app.config['SQLALCHEMY_DATABASE_URI']="mssql+pyodbc://DESKTOP-URHHJQ5/atm6?driver=SQL+Server?trusted_connection=yes"


app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)


class customer_details(db.Model) :
	id = db.Column( db.Integer,primary_key=True)
	pin = db.Column(db.Integer,unique=True)
	account_num=db.Column(db.Integer)


	def __init__(self,pin,account_num=None):


	   
	   self.pin = pin
	   if account_num:
	   	self.account_num=account_num
	  


class Transactions(db.Model):
	Transaction_idn = db.Column(db.Integer,primary_key=True)
	deposit_amt=db.Column(db.Float)

	withdraw_amt=db.Column(db.Float)
	balance= db.Column(db.Integer)
	cus_id= db.Column(db.Integer, db.ForeignKey('customer_details.id'),nullable=False)
	crt_dt = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)


	def __init__(self,cus_id,balance=0,deposit_amt=None,withdraw_amt=None):
		self.cus_id=cus_id
		if deposit_amt:
			self.deposit_amt=deposit_amt
		elif withdraw_amt:
			self.withdraw_amt=withdraw_amt
	
		self.balance=balance
		




@app.route('/error')
def error():
	
	return render_template('atm11.html')

@app.route('/')
def index():
	return render_template('atm2.html')
class ATM:
	'''welcome to the ATM'''
	
	def __init__(self,pin=None,balance=0):
		'''credentials of account.'''
		
		self.balance = balance
		if pin:
			self.pin=pin

		
	
	def login(self,pin):
		
		'''Logi credentials for ATM'''
		self.pin = pin
		

		pin_regex = re.compile(r'^[1-3]+\d{3}$')
		
		searcher_output = pin_regex.search(pin)
		
		return searcher_output
		
	   
		

	def validate_acc(self,account_num):
		"validate account"
		self.account_num=account_num
		acc_regex=re.compile(r'^[1-4]+\d{7}$')
		searcher_output=acc_regex.search(account_num)
		return searcher_output

	def getBalance(self):

		"accessing for amount"

		return self.balance

	def getPin(self):

		"waiting for user response"
		
		return self.pin
		
	def withdraw(self,amount,bal):

		"aceesing the amount to customer"

		self.balance = bal-amount
		
		return self.balance

	def deposit(self,amount,bal=0):

		"Deposits are accepted"

		self.balance = bal+amount
		return self.balance

	def display(self):

		"providing the final results"
		
		return self.balance



acc = ATM()



@app.route('/login',methods=['POST','GET'])
def log_in():
	''' accessing the credentials'''
	return render_template('atm.html')

@app.route('/menu',methods=['POST','GET'])
def menu():
	if request.method=='GET':
		return render_template('atm3.html')

@app.route('/deposit',methods=['POST','GET'])
def deposit():
	#bal=0
	if request.method=='GET':

		#bal=amount
		res=make_response(render_template('atm4.html'))
		#res.set_cookie('bal',bal)
		return res

@app.route('/withdrawl',methods=['POST','GET'])
def withdrawl():
	
	if request.method=='GET':

		res=make_response(render_template('atm5.html'))
		
		return res
@app.route('/registration_form',methods=['GET','POST'])
def registration():
	
	return render_template('atm7.html')
@app.route('/verify1',methods=['POST','GET'])
def verify1():
	import pdb
	pdb.set_trace()
	if request.method=="POST":
		match=''
		acc_num=request.form['account_number']
		pin=request.form['pin']
		mo1=acc.login(pin)
		mo2=acc.validate_acc(acc_num)

	try:
		match=mo1.group(0),mo2.group(0)
		#match=mo2.group(0)
	except:
		
		return render_template('atm8.html')

	if match:
		
		c1=customer_details(pin=pin,account_num=acc_num)

		db.session.add(c1)
		db.session.commit()
		c2=customer_details.query.filter_by(pin=pin).first()
		id1=c2.id
		c3=Transactions(cus_id=id1)
		db.session.add(c3)
		db.session.commit()
		return redirect(url_for('index'))
	
@app.route('/verify',methods=['POST','GET'])
def verify():
	for i in range(1,3):
		if request.method=='POST':
			match = ''
			session['pin'] = request.form['pin']
			
			pin=session['pin']
			mo = acc.login(pin)
			try:
				match = mo.group(0)
				time.sleep(0.2)
				
		
			except AttributeError:
				print("retry once ")
				
			except TypeError:
				print ("Type Error")
				
			except: 
				print("please enter the correct pin.")
				return redirect(url_for('error'))
			if match:
				credentials=customer_details(pin=pin)
				credentials1=customer_details.query.filter_by(pin=pin).first()
				#credentials1=customer_details.query.all()
				#for x in credentials1:
				if credentials1:
					return redirect(url_for('menu'))
				else:
					return render_template('atm7.html')

@app.route('/balance/<option>',methods=['POST','GET'])
def balance(option):
	if request.method=='POST':
		
			
		if option == 'deposit':
			#"For deposit"
			
			amt=int(request.form['amount'])
			
			z1=acc.getPin()
		
			y=customer_details.query.filter_by(pin=z1).first()
			#bal=y.balance
			y1=y.id
			c2=Transactions(cus_id=y1)
			c3=Transactions.query.filter_by(cus_id=y1).first()
			if c3:
				y2=Transactions.query.filter_by(cus_id=y1).order_by(Transactions.Transaction_idn.desc()).limit(1).first()
				bal=y2.balance

				if bal:
					bal1 = acc.deposit(amt,bal)
					c1=Transactions(deposit_amt=amt,cus_id=y1,balance=bal1)
					db.session.add(c1)
					db.session.commit()

					return render_template('atm6.html',x=bal1)

				else:
					bal3 = acc.deposit(amt)
					c1=Transactions(deposit_amt=amt,cus_id=y1,balance=bal3)
					db.session.add(c1)
					db.session.commit()

					db.session.commit()
					return render_template('atm6.html',x=bal3)

	
				
			
		elif option == 'withdrawl':
			#"reading withdraw"
   
			amt=int(request.form['amount'])
			
			z2=acc.getPin()
			
			y2=customer_details.query.filter_by(pin=z2).first()
			y1=y2.id
			y3=Transactions.query.filter_by(cus_id=y1).order_by(Transactions.Transaction_idn.desc()).limit(1).first()
			bal=y3.balance
			bal1=int(bal)
			if amt<bal1:
				amount=amt

				bal2=acc.withdraw(amount,bal1)
				
				c2=Transactions(withdraw_amt=amount,cus_id=y1,balance=bal2)
				#c2=customer_details(balance=x)
				#yz=Transactions.query.order_by(Transactions.Transaction_idn.desc()).limit(1).first()
				#yz.balance=bal2
				#db.session.add(c1)
				db.session.add(c2)
				db.session.commit()

				return render_template('atm6.html',x=bal2)
			elif bal==0:
				return render_template('atm10.html')
				#return '<html><body><h>choose correct amount</h1></body></html>'

			else:
				return render_template('atm9.html')
			#break
					
		elif option == 'balance':
			"for balance enquiry"
			#x=acc.display()
			y4=acc.getPin()
			y=customer_details.query.filter_by(pin=y4).first()
			y2=y.id
			y3=Transactions.query.filter_by(cus_id=y2).order_by(Transactions.Transaction_idn.desc()).limit(1).first()
			x=y3.balance
			return render_template('atm6.html',x=x)
			#break
		else:
			exit()
	

	else:
		print("sorry we are unable to process this transaction")

#else:
	#print("you entered wrong pin.")

@app.route('/logout',methods=['POST','GET'])      
def logout():
	if request.method=="POST":
		session.pop('pin',None)
		return redirect(url_for('index'))



if __name__=='__main__':
	db.create_all()
	app.run(debug=True)


				
			 
			 
		
