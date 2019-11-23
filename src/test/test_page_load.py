from app import app
import unittest2


class FlaskTestCase(unittest.TestCase):

    # Ensure that Flask login page was set up correctly
    def test_login_page(self):
        tester = app.test_client(self)
        response = tester.get('login/login.html.j2', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    # Ensure that the login page loads correctly
    def test_login_page_loads(self):
        tester = app.test_client(self)
        response = tester.get('login/login.html.j2')
        self.assertIn(b'Username', response.data)

    # Ensure that Flask password reset page was set up correctly
    def test_password_reset_page(self):
        tester = app.test_client(self)
        response = tester.get('login/password-reset.html.j2', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    # Ensure that the password reset page loads correctly
    def test_password_reset_page_loads(self):
        tester = app.test_client(self)
        response = tester.get('login/password-reset.html.j2')
        self.assertIn(b'Reset your password', response.data)
		
	# Ensure that Flask register page was set up correctly
    def test_register_page(self):
        tester = app.test_client(self)
        response = tester.get('login/register.html.j2', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    # Ensure that the register page loads correctly
    def test_register_page_loads(self):
        tester = app.test_client(self)
        response = tester.get('login/register.html.j2')
        self.assertIn(b'Register', response.data)
		
	# Ensure that Flask purchase page was set up correctly
    def test_purchase_page(self):
        tester = app.test_client(self)
        response = tester.get('stocks/purchase.html.j2', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    # Ensure that the purchase page loads correctly
    def test_purchase_page_loads(self):
        tester = app.test_client(self)
        response = tester.get('stocks/purchase.html.j2')
        self.assertIn(b'Purchase Stock', response.data)
		
	# Ensure that Flask sell page was set up correctly
    def test_sell_page(self):
        tester = app.test_client(self)
        response = tester.get('stocks/sell.html.j2', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    # Ensure that the sell page loads correctly
    def test_sell_page_loads(self):
        tester = app.test_client(self)
        response = tester.get('stocks/sell.html.j2')
        self.assertIn(b'Purchase Stock', response.data)


if __name__ == '__main__':
    unittest.main()