import unittest
import json 
import manage


class TestMethods(unittest.TestCase):
	"""docstring for TestMethods"""
	def setUp(self):
		manage.app.testing = True
		self.app = manage.app.test_client()
	
	def test_health(self):
		response=self.app.get('/v1/health',content_type='application/json')
		self.assertEqual(response.status_code,200)

if __name__ == '__main__':
	unittest.main()
