import unittest
import jwt
from collector.fetch import create_token, make_authorized_request
import responses


class FetchTests(unittest.TestCase):

    def test_create_token(self):
        secret = "Whabadubaduppdupp"
        token = create_token(secret)
        print("Token: %s" % token)
        decoded_token = jwt.decode(token, secret, algorithms=['HS256'])
        print("Token: %s" % decoded_token)
        self.assertEqual(decoded_token.get("iss"), 'local')

    @responses.activate
    def test_secure_request(self):
        responses.add(**{
            'method': responses.POST,
            'url': 'http://amplitude-proxy.example.com/ingresses',
            'body': 'success',
            'status': 200,
            'content_type': 'application/json',
            'adding_headers': {'X-Foo': 'Bar'}
        })
        data = [
            {"some": "data"},
            {"some": "other-data"},
        ]
        response = make_authorized_request('http://amplitude-proxy.example.com/ingresses', data)
        print("Response: %s" % response)
        self.assertEqual(response, 'success')
