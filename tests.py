import unittest, json
from project import app


class TestCheckInput(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
        self.api_path = "http://127.0.0.1:5000/v1/sanitized/input"

    def get_response(self, payload):
        return self.app.post(self.api_path, 
                            json = {"payload": payload})

    def test_check_input(self):
        response = self.get_response("correct input")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)['result'],"sanitized")
    
        response = self.get_response("105 \" or 1=1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)['result'],"unsanitized")

        response = self.get_response("105; DROP TABLE")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)['result'],"unsanitized")

        response = self.get_response("username + \"some string\"")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)['result'],"unsanitized")
        
        with self.assertRaises(ValueError):
            response = self.app.post(self.api_path, 
                                json = {"another key":"username + \"some string\""})
        
        with self.assertRaises(ValueError):
            response = self.app.post(self.api_path, 
                                json = {"payload":"username + \"some string\"",
                                        "additional_key": "value"})        
        
if __name__ == '__main__':
    unittest.main()
