'''def testblance(option):
	 prev_bal = balance(balance))
	 new_bal = balance(deposit(4000))
	 assert(new_bal=prev_bal+4000)'''
from temp_project1 import *
import unittest
class Testclass01(unittest.TestCase):
	#def setUp(self):
		#self.acc=ATM()

	def test_deposit(self):
		result=acc.deposit(3,5)
		self.assertEqual(result,8)
		print("deposit")
	def test_withdraw(self):
		result=acc.withdraw(2,5)
		self.assertEqual(result,3)
	def test_balance(self):
		prev_bal=balance(acc.display())
		new_bal=balance(deposit(400))
		self.assertTrue(sum(new_bal=prev_bal+new_bal))
	def test_login(self):
		pin=acc.login('3434')
		self.assertRegex('3434',r'^[1-3]+\d{3}$')
	def test_validate_acc(self):
		#import pdb
		#pdb.set_trace()
		acc_num=acc.validate_acc('1123456')
		self.assertRegex('11234567',r'^[1-4]+\d{7}$')
if __name__ == '__main__':
	unittest.main()






