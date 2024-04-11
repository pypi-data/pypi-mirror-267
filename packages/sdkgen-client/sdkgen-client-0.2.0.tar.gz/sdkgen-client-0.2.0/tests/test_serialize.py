import unittest

from tests.generated.test_response import TestResponse


class TestSerialize(unittest.TestCase):
    def test_serialize(self):
        json = '{"method": "POST"}'

        response = TestResponse.model_validate_json(json_data=json)

        self.assertEqual("POST", response.method)

