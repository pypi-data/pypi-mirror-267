import unittest
from .generated.client import Client
from .generated.test_request import TestRequest
from .generated.test_object import TestObject


class TestIntegration(unittest.TestCase):
    def test_client_get_all(self):
        client = Client.build("my_token")

        response = client.product().get_all(8, 16, "foobar")

        self.assertEqual(response.headers["Authorization"], "Bearer my_token")
        self.assertEqual(response.headers["Accept"], "application/json")
        self.assertEqual(response.headers["User-Agent"], "SDKgen Client v1.0")
        self.assertEqual(response.method, "GET")
        self.assertEqual(response.args["startIndex"], "8")
        self.assertEqual(response.args["count"], "16")
        self.assertEqual(response.args["search"], "foobar")
        self.assertEqual(response.json, None)

    def test_client_create(self):
        client = Client.build("my_token")

        payload = self.new_payload()
        response = client.product().create(payload)

        self.assertEqual(response.headers["Authorization"], "Bearer my_token")
        self.assertEqual(response.headers["Accept"], "application/json")
        self.assertEqual(response.headers["User-Agent"], "SDKgen Client v1.0")
        self.assertEqual(response.method, "POST")
        self.assertEqual(response.json.model_dump_json(by_alias=True), '{"int":1337,"float":13.37,"string":"foobar","bool":true,"arrayScalar":["foo","bar"],"arrayObject":[{"id":1,"name":"foo"},{"id":1,"name":"bar"}],"mapScalar":{"bar":"foo","foo":"bar"},"mapObject":{"bar":{"id":1,"name":"bar"},"foo":{"id":1,"name":"foo"}},"object":{"id":1,"name":"foo"}}')

    def test_client_update(self):
        client = Client.build("my_token")

        payload = self.new_payload()
        response = client.product().update(1, payload)

        self.assertEqual(response.headers["Authorization"], "Bearer my_token")
        self.assertEqual(response.headers["Accept"], "application/json")
        self.assertEqual(response.headers["User-Agent"], "SDKgen Client v1.0")
        self.assertEqual(response.method, "PUT")
        self.assertEqual(response.json.model_dump_json(by_alias=True), '{"int":1337,"float":13.37,"string":"foobar","bool":true,"arrayScalar":["foo","bar"],"arrayObject":[{"id":1,"name":"foo"},{"id":1,"name":"bar"}],"mapScalar":{"bar":"foo","foo":"bar"},"mapObject":{"bar":{"id":1,"name":"bar"},"foo":{"id":1,"name":"foo"}},"object":{"id":1,"name":"foo"}}')

    def test_client_patch(self):
        client = Client.build("my_token")

        payload = self.new_payload()
        response = client.product().patch(1, payload)

        self.assertEqual(response.headers["Authorization"], "Bearer my_token")
        self.assertEqual(response.headers["Accept"], "application/json")
        self.assertEqual(response.headers["User-Agent"], "SDKgen Client v1.0")
        self.assertEqual(response.method, "PATCH")
        self.assertEqual(response.json.model_dump_json(by_alias=True), '{"int":1337,"float":13.37,"string":"foobar","bool":true,"arrayScalar":["foo","bar"],"arrayObject":[{"id":1,"name":"foo"},{"id":1,"name":"bar"}],"mapScalar":{"bar":"foo","foo":"bar"},"mapObject":{"bar":{"id":1,"name":"bar"},"foo":{"id":1,"name":"foo"}},"object":{"id":1,"name":"foo"}}')

    def test_client_delete(self):
        client = Client.build("my_token")

        response = client.product().delete(1)

        self.assertEqual(response.headers["Authorization"], "Bearer my_token")
        self.assertEqual(response.headers["Accept"], "application/json")
        self.assertEqual(response.headers["User-Agent"], "SDKgen Client v1.0")
        self.assertEqual(response.method, "DELETE")
        self.assertEqual(response.json, None)

    def new_payload(self) -> TestRequest:
        object_foo = TestObject()
        object_foo.id = 1
        object_foo.name = "foo"
        object_bar = TestObject()
        object_bar.id = 1
        object_bar.name = "bar"

        array_scalar = ["foo", "bar"]
        array_object = [object_foo, object_bar]

        map_scalar = {"foo": "bar", "bar": "foo"}
        map_object = {"foo": object_foo, "bar": object_bar}

        request = TestRequest()
        request.int_ = 1337
        request.float_ = 13.37
        request.string = "foobar"
        request.bool_ = True
        request.array_scalar = array_scalar
        request.array_object = array_object
        request.map_scalar = map_scalar
        request.map_object = map_object
        request.object = object_foo
        return request


if __name__ == '__main__':
    unittest.main()
