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


    def test_path_traversal_vulnerability(self):
        # Test various path traversal attempts
        traversal_paths = [
            '/../../../etc/passwd',
            '/..%2f..%2f..%2fetc%2fpasswd',  # URL encoded
            '/%2e%2e/%2e%2e/%2e%2e/etc/passwd',  # Double URL encoded
            '/static/../../../../etc/passwd',
            '/.%2e/.%2e/.%2e/.%2e/etc/passwd',  # Mixed encoding
        ]
        
        for path in traversal_paths:
            response = self.app.get(path)
            
            # Should return 404 Not Found without exposing sensitive information
            self.assertIn(response.status_code, [404, 400])
            
            # Ensure no sensitive content is leaked
            if response.data:
                self.assertNotIn(b'/etc/passwd', response.data)
                self.assertNotIn(b'root:', response.data)


    def test_home_with_extremely_long_query_params(self):
        # Create an extremely long query parameter (10,000+ characters)
        long_value = 'a' * 10000
        url = f'/?param={long_value}'
        
        # Test the home route with the long query parameter
        response = self.app.get(url)
        
        # Application should handle it normally
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"message": "Welcome to the Flask App!"})


    def test_home_patch_not_allowed(self):
        # Test PATCH method on the home route
        response = self.app.patch('/')
        self.assertEqual(response.status_code, 405)
        # Check that Allow header indicates GET is allowed
        self.assertIn('GET', response.headers.get('Allow', ''))


    def test_home_head_method(self):
        # Test HEAD method on the home route
        head_response = self.app.head('/')
        get_response = self.app.get('/')
        
        # Status code should be 200
        self.assertEqual(head_response.status_code, 200)
        
        # HEAD should have same headers as GET
        self.assertEqual(head_response.content_type, get_response.content_type)
        
        # HEAD should have no body content
        self.assertEqual(head_response.data, b'')


    def test_home_options_method(self):
        # Test OPTIONS method on the home route
        response = self.app.options('/')
        self.assertEqual(response.status_code, 200)
        # Check that Allow header indicates GET is allowed
        self.assertIn('GET', response.headers.get('Allow', ''))
        # Verify other common methods in the Allow header
        self.assertIn('HEAD', response.headers.get('Allow', ''))
        self.assertIn('OPTIONS', response.headers.get('Allow', ''))


if __name__ == '__main__':
    unittest.main()