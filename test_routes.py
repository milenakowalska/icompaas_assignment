import unittest, json, requests
from unittest.mock import patch
from project import app

class TestCheckInput(unittest.TestCase):
    def test_check_input(self):
        input_data = {"payload":"correct input"}
        response = requests.post("http://127.0.0.1:5000/v1/sanitized/input",
                                json = input_data)
        self.assertEqual(json.loads(response.text),
                        {"result" : "sanitized"})

        input_data = {"payload":"105 \" or 1=1"}
        response = requests.post("http://127.0.0.1:5000/v1/sanitized/input",
                                json = input_data)
        self.assertEqual(json.loads(response.text),
                        {"result" : "unsanitized"})

        input_data = {"payload":"105; DROP TABLE"}
        response = requests.post("http://127.0.0.1:5000/v1/sanitized/input",
                                json = input_data)
        self.assertEqual(json.loads(response.text),
                        {"result" : "unsanitized"})

        input_data = {"payload":"username '' or \"=\""}
        response = requests.post("http://127.0.0.1:5000/v1/sanitized/input",
                                json = input_data)
        self.assertEqual(json.loads(response.text),
                        {"result" : "unsanitized"})

        input_data = {"payload":"username + \"some string\""}
        response = requests.post("http://127.0.0.1:5000/v1/sanitized/input",
                                json = input_data)
        self.assertEqual(json.loads(response.text),
                        {"result" : "unsanitized"})

if __name__ == '__main__':
    unittest.main()