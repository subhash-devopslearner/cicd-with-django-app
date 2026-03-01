from django.test import TestCase, Client

# Create your tests here.
class SiteTests(TestCase):
    def test_homepage_works(self):
        # This replaces your 'curl http://localhost:8000'
        client = Client()
        response = client.get('/')
        self.assertEqual(response.status_code, 200)
