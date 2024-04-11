import unittest

from tests.generated.test_request import TestRequest


class TestSerialize(unittest.TestCase):
    def test_serialize(self):
        json = '{"int": 1337, "float": 13.37, "string": "foobar", "bool": true, "arrayScalar": ["foo", "bar"], "arrayObject": [{"id": 1, "name": "foo"}, {"id": 1, "name": "bar"}], "mapScalar": {"bar": "foo", "foo": "bar"}, "mapObject": {"bar": {"id": 1, "name": "bar"}, "foo": {"id": 1, "name": "foo"}}, "object": {"id": 1, "name": "foo"}}'

        response = TestRequest.model_validate_json(json_data=json)

        self.assertEqual(1337, response.int_)
        self.assertEqual(13.37, response.float_)
        self.assertEqual("foobar", response.string)
        self.assertEqual(True, response.bool_)
        self.assertEqual(["foo", "bar"], response.array_scalar)


if __name__ == '__main__':
    unittest.main()
