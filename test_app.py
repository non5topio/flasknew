import unittest
from app import app

class AppTests(unittest.TestCase):

    def setUp(self):
        # Set up the test client
        self.app = app.test_client()
        self.app.testing = True

    def test_home(self):
        # Test the home route
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"message": "Welcome to the Flask App!"})

    def test_home_content_type(self):
        # Test the Content-Type header for the home route
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')


    def test_home_delete_not_allowed(self):
        # Test DELETE method on the home route
        response = self.app.delete('/')
        self.assertEqual(response.status_code, 405)
        self.assertIn('GET', response.headers.get('Allow', ''))


    def test_home_put_not_allowed(self):
        # Test PUT method on the home route
        response = self.app.put('/')
        self.assertEqual(response.status_code, 405)
        self.assertIn('GET', response.headers.get('Allow', ''))


    def test_home_post_not_allowed(self):
        # Test POST method on the home route
        response = self.app.post('/')
        self.assertEqual(response.status_code, 405)
        # Check that Allow header indicates GET is allowed (and potentially HEAD, OPTIONS)
        self.assertIn('GET', response.headers.get('Allow', ''))


    def test_home_with_query_params(self):
        # Test the home route with unexpected query parameters
        response = self.app.get('/?param1=value1&param2=value2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"message": "Welcome to the Flask App!"})


    def test_nonexistent_route(self):
        # Test accessing a non-existent route
        response = self.app.get('/nonexistent_route')
        self.assertEqual(response.status_code, 404)
        # Optionally, check for specific content in the 404 page if customized
        # self.assertIn(b"Not Found", response.data) # Flask's default 404 page contains this


if __name__ == '__main__':
    unittest.main()