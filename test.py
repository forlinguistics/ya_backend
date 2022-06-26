import os
from app import app as shop, db as shop_db
import unittest
import json
from unit_test import print_diff, deep_sort_children

fake_id = '069cb8d7-bbdd-47d3-ad8f-82ef4c269df2'
root_id = "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1"
simple_post = {
    "items": [
        {
            "type": "CATEGORY",
            "name": "Товары",
            "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
            "parentId": None
        }
    ],
    "updateDate": "2022-02-01T12:00:00.000Z"
}

import_tree = [
    {
        "items": [
            {
                "type": "CATEGORY",
                "name": "Товары",
                "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
                "parentId": None
            }
        ],
        "updateDate": "2022-02-01T12:00:00.000Z"
    },
    {
        "items": [
            {
                "type": "CATEGORY",
                "name": "Смартфоны",
                "id": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
                "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1"
            },
            {
                "type": "OFFER",
                "name": "jPhone 13",
                "id": "863e1a7a-1304-42ae-943b-179184c077e3",
                "parentId": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
                "price": 79999
            },
            {
                "type": "OFFER",
                "name": "Xomiа Readme 10",
                "id": "b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4",
                "parentId": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
                "price": 59999
            }
        ],
        "updateDate": "2022-02-02T12:00:00.000Z"
    },
    {
        "items": [
            {
                "type": "CATEGORY",
                "name": "Телевизоры",
                "id": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1"
            },
            {
                "type": "OFFER",
                "name": "Samson 70\" LED UHD Smart",
                "id": "98883e8f-0507-482f-bce2-2fb306cf6483",
                "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                "price": 32999
            },
            {
                "type": "OFFER",
                "name": "Phyllis 50\" LED UHD Smarter",
                "id": "74b81fda-9cdc-4b63-8927-c978afed5cf4",
                "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                "price": 49999
            }
        ],
        "updateDate": "2022-02-03T12:00:00.000Z"
    },
    {
        "items": [
            {
                "type": "OFFER",
                "name": "Goldstar 65\" LED UHD LOL Very Smart",
                "id": "73bc3b36-02d1-4245-ab35-3106c9ee1c65",
                "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                "price": 69999
            }
        ],
        "updateDate": "2022-02-03T15:00:00.000Z"
    }
]
tree = {
    "type": "CATEGORY",
    "name": "Товары",
    "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
    "price": 58599,
    "parentId": None,
    "date": "2022-02-03T15:00:00.000Z",
    "children": [
        {
            "type": "CATEGORY",
            "name": "Телевизоры",
            "id": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
            "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
            "price": 50999,
            "date": "2022-02-03T15:00:00.000Z",
            "children": [
                {
                    "type": "OFFER",
                    "name": "Samson 70\" LED UHD Smart",
                    "id": "98883e8f-0507-482f-bce2-2fb306cf6483",
                    "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                    "price": 32999,
                    "date": "2022-02-03T12:00:00.000Z",
                    "children": None,
                },
                {
                    "type": "OFFER",
                    "name": "Phyllis 50\" LED UHD Smarter",
                    "id": "74b81fda-9cdc-4b63-8927-c978afed5cf4",
                    "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                    "price": 49999,
                    "date": "2022-02-03T12:00:00.000Z",
                    "children": None
                },
                {
                    "type": "OFFER",
                    "name": "Goldstar 65\" LED UHD LOL Very Smart",
                    "id": "73bc3b36-02d1-4245-ab35-3106c9ee1c65",
                    "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                    "price": 69999,
                    "date": "2022-02-03T15:00:00.000Z",
                    "children": None
                }
            ]
        },
        {
            "type": "CATEGORY",
            "name": "Смартфоны",
            "id": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
            "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
            "price": 69999,
            "date": "2022-02-02T12:00:00.000Z",
            "children": [
                {
                    "type": "OFFER",
                    "name": "jPhone 13",
                    "id": "863e1a7a-1304-42ae-943b-179184c077e3",
                    "parentId": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
                    "price": 79999,
                    "date": "2022-02-02T12:00:00.000Z",
                    "children": None
                },
                {
                    "type": "OFFER",
                    "name": "Xomiа Readme 10",
                    "id": "b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4",
                    "parentId": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
                    "price": 59999,
                    "date": "2022-02-02T12:00:00.000Z",
                    "children": None
                }
            ]
        },
    ]
}

tree_with_rebase = {
    "type": "CATEGORY",
    "name": "Товары",
    "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
    "price": 58599,
    "parentId": None,
    "date": "2022-02-03T16:00:00.000Z",
    "children": [

        {
            "type": "CATEGORY",
            "name": "Смартфоны",
            "id": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
            "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
            "price": 58599,
            "date": "2022-02-03T16:00:00.000Z",
            "children": [
                {
                    "type": "OFFER",
                    "name": "jPhone 13",
                    "id": "863e1a7a-1304-42ae-943b-179184c077e3",
                    "parentId": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
                    "price": 79999,
                    "date": "2022-02-02T12:00:00.000Z",
                    "children": None
                },
                {
                    "type": "OFFER",
                    "name": "Xomiа Readme 10",
                    "id": "b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4",
                    "parentId": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
                    "price": 59999,
                    "date": "2022-02-02T12:00:00.000Z",
                    "children": None
                },
                {
                    "type": "CATEGORY",
                    "name": "Телевизоры",
                    "id": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                    "parentId": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
                    "price": 50999,
                    "date": "2022-02-03T16:00:00.000Z",
                    "children": [
                        {
                            "type": "OFFER",
                            "name": "Samson 70\" LED UHD Smart",
                            "id": "98883e8f-0507-482f-bce2-2fb306cf6483",
                            "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                            "price": 32999,
                            "date": "2022-02-03T12:00:00.000Z",
                            "children": None,
                        },
                        {
                            "type": "OFFER",
                            "name": "Phyllis 50\" LED UHD Smarter",
                            "id": "74b81fda-9cdc-4b63-8927-c978afed5cf4",
                            "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                            "price": 49999,
                            "date": "2022-02-03T12:00:00.000Z",
                            "children": None
                        },
                        {
                            "type": "OFFER",
                            "name": "Goldstar 65\" LED UHD LOL Very Smart",
                            "id": "73bc3b36-02d1-4245-ab35-3106c9ee1c65",
                            "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                            "price": 69999,
                            "date": "2022-02-03T15:00:00.000Z",
                            "children": None
                        }
                    ]
                }
            ]
        },
    ]
}


class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        shop.config['TESTING'] = True
        self.app = shop.test_client()
        self.app.application.config[
            'SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Mynameismike99@localhost/test_products'
        shop_db.init_app(self.app.application)
        shop_db.create_all(app=self.app.application)

    def tearDown(self):
        shop_db.session.remove()
        shop_db.drop_all(app=self.app.application)
        shop_db.get_engine(self.app.application).dispose()

    def test_simple_import(self):
        post_json = json.dumps(simple_post)
        # test parent not in db
        error_dict = json.loads(post_json)
        error_dict['items'][0]['parentId'] = fake_id
        status = self.app.post('/imports', json=error_dict)
        assert status.status_code == 400
        # test category price not null
        error_dict = json.loads(post_json)
        error_dict['items'][0]['price'] = 23
        status = self.app.post('/imports', json=error_dict)
        assert status.status_code == 400
        # test element name not null
        error_dict = json.loads(post_json)
        error_dict['items'][0]['name'] = None
        status = self.app.post('/imports', json=error_dict)
        assert status.status_code == 400
        # test two elements with the same id in one import
        error_dict = json.loads(post_json)
        error_dict['items'].append(error_dict['items'][0])
        status = self.app.post('/imports', json=error_dict)
        assert status.status_code == 400
        # test simple correct json
        status = self.app.post('/imports', json=simple_post)
        assert status.status_code == 200

    def test_simple_get_node(self):
        status = self.app.post('/imports', json=simple_post)
        assert status.status_code == 200
        expected_json = simple_post['items'][0].copy()
        expected_json['children'] = None
        expected_json['date'] = simple_post['updateDate']
        expected_json['price'] = None
        node_id = simple_post['items'][0]['id']
        status = self.app.get('/nodes/' + node_id)
        assert status.get_json() == expected_json

    def test_delete(self):
        status = self.app.post('/imports', json=simple_post)
        assert status.status_code == 200
        node_id = simple_post['items'][0]['id']
        status = self.app.delete('/delete/' + node_id)
        assert status.status_code == 200
        status = self.app.get('/nodes/' + node_id)
        assert status.status_code == 404
        status = self.app.delete('/delete/' + fake_id)
        assert status.status_code == 404

    def test_tree_import(self):
        for batch in import_tree:
            status = self.app.post('/imports', json=batch)
            assert status.status_code == 200
        status = self.app.get('/nodes/' + root_id)
        resp_tree = status.get_json()
        deep_sort_children(resp_tree)
        deep_sort_children(tree)
        assert resp_tree == tree

    def test_node_rebase(self):
        for batch in import_tree:
            status = self.app.post('/imports', json=batch)
            assert status.status_code == 200
        rebase_dict = {
            "items": [
                {
                    "type": "CATEGORY",
                    "name": "Телевизоры",
                    "id": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                    "parentId": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
                    "price": None
                }
            ],
            "updateDate": "2022-02-03T16:00:00.000Z"
        }
        status = self.app.post('/imports', json=rebase_dict)
        assert status.status_code == 200
        status = self.app.get('/nodes/' + root_id)
        resp_tree = status.get_json()
        deep_sort_children(resp_tree)
        deep_sort_children(tree_with_rebase)
        assert resp_tree == tree_with_rebase


if __name__ == '__main__':
    unittest.main()
