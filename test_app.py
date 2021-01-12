from flask import Flask
#from flask_testing import TestCase
from app import app, session
from db.alembic_orm.add import Base, engine, Session
import unittest
import json
import base64




class BaseCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        session.commit()
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)


    def tearDown(self):
        #session.remove()
        session.close()
        session.commit()
        # Base.metadata.drop_all(bind=engine)
        pass

    def open_with_auth(self, url, method, username, password):
        return self.app.open(url,
                             method=method,
                             headers={
                                 'Authorization': 'Basic ' + base64.b64encode(username + ":" + password)
                             }
                             )


class User(BaseCase):
    def test_re(self):
        self.assertEqual(2, 2)

    def test_user_post(self):
       post_data = json.dumps(
            {
                "username": "hhh",
                "email": "eh@mail.com",
                "password": "1233"
            }
        )

       response = self.app.post('users', headers={"Content-Type": "application/json"}, data=post_data)
       self.assertEqual(201, response.status_code)


    def test_invaid_users(self):
       post_data = json.dumps(
            {
                "username": "hhh",
                "email": "ehmail.com",
                "password": "1233"
            }
        )

       response = self.app.post('users', headers={"Content-Type": "application/json"}, data=post_data)
       self.assertEqual(400, response.status_code)


    def test_same_user(self):
       post_data = json.dumps(
            {
                "username": "hhh",
                "email": "eh@mail.com",
                "password": "1233"
            }
        )

       self.app.post('users', headers={"Content-Type": "application/json"}, data=post_data)

       post_data = json.dumps(
           {
               "username": "hhh",
               "email": "eh@mail.com",
               "password": "1233"
           }
       )

       response = self.app.post('users', headers={"Content-Type": "application/json"}, data=post_data)
       self.assertEqual(400, response.status_code)


    def test_get_userbyId(self):
        post_data = json.dumps(
            {
                "username": "hhh",
                "email": "eh@mail.com",
                "password": "1233"
            }
        )

        self.app.post('users', headers={"Content-Type": "application/json"}, data=post_data)

        response = self.app.get('users/1')
        self.assertEqual(200, response.status_code)


    def test_get_userbyId_no_user(self):

        response = self.app.get('users/1')
        self.assertEqual(404, response.status_code)


    def test_get_userbyId_not_int(self):

        response = self.app.get('users/not_integer')
        self.assertEqual(400, response.status_code)


    def test_usersId_put(self):
       post_data = json.dumps(
            {
                "username": "hhh",
                "email": "eh@mail.com",
                "password": "1233"
            }
        )

       self.app.post('users', headers={"Content-Type": "application/json"}, data=post_data)

       alice_credentials = base64.b64encode(b'hhh:1233').decode('utf-8')
       put_data = json.dumps(
           {
               "username": "hhh",
               "email": "eh@mail.com",
               "password": "1233"
           }
       )
       response = self.app.put('users/1', content_type='application/json', headers={'Authorization': f'Basic {alice_credentials}'}, data=put_data)

       self.assertEqual(200, response.status_code)


    def test_usersId_put_no_user(self):
       post_data = json.dumps(
            {
                "username": "hhh",
                "email": "eh@mail.com",
                "password": "1233"
            }
        )

       self.app.post('users', headers={"Content-Type": "application/json"}, data=post_data)

       alice_credentials = base64.b64encode(b'hhh:1233').decode('utf-8')
       put_data = json.dumps(
           {
               "username": "hhh",
               "email": "eh@mail.com",
               "password": "1233"
           }
       )
       response = self.app.put('users/2', content_type='application/json', headers={'Authorization': f'Basic {alice_credentials}'}, data=put_data)

       self.assertEqual(400, response.status_code)


    def test_usersId_put_invalid(self):
       post_data = json.dumps(
            {
                "username": "hhh",
                "email": "eh@mail.com",
                "password": "1233"
            }
        )

       self.app.post('users', headers={"Content-Type": "application/json"}, data=post_data)

       alice_credentials = base64.b64encode(b'hhh:1233').decode('utf-8')
       put_data = json.dumps(
           {
               "username": "hhh",
               "email": "ehmail.com",
               "password": "1233"
           }
       )
       response = self.app.put('users/1', content_type='application/json', headers={'Authorization': f'Basic {alice_credentials}'}, data=put_data)

       self.assertEqual(400, response.status_code)


    def test_usersId_put_not_same_user(self):
       post_data = json.dumps(
            {
                "username": "hhh",
                "email": "eh@mail.com",
                "password": "1233"
            }
        )

       self.app.post('users', headers={"Content-Type": "application/json"}, data=post_data)

       post_data = json.dumps(
           {
               "username": "hhhj",
               "email": "ehlo@mail.com",
               "password": "1233"
           }
       )

       self.app.post('users', headers={"Content-Type": "application/json"}, data=post_data)

       alice_credentials = base64.b64encode(b'hhhj:1233').decode('utf-8')
       put_data = json.dumps(
           {
               "username": "hhh",
               "email": "eh@mail.com",
               "password": "1233"
           }
       )
       response = self.app.put('users/1', content_type='application/json', headers={'Authorization': f'Basic {alice_credentials}'}, data=put_data)

       self.assertEqual(403, response.status_code)


    def test_usersId_put_not_busy_username(self):
       post_data = json.dumps(
            {
                "username": "hhh",
                "email": "eh@mail.com",
                "password": "1233"
            }
        )

       self.app.post('users', headers={"Content-Type": "application/json"}, data=post_data)

       post_data = json.dumps(
           {
               "username": "hhhj",
               "email": "ehlo@mail.com",
               "password": "1233"
           }
       )

       self.app.post('users', headers={"Content-Type": "application/json"}, data=post_data)

       alice_credentials = base64.b64encode(b'hhhj:1233').decode('utf-8')
       put_data = json.dumps(
           {
               "username": "hhh",
               "email": "eh@mail.com",
               "password": "1233"
           }
       )
       response = self.app.put('users/2', content_type='application/json', headers={'Authorization': f'Basic {alice_credentials}'}, data=put_data)

       self.assertEqual(400, response.status_code)


    def test_delete_userbyId(self):
        post_data = json.dumps(
            {
                "username": "hhh",
                "email": "eh@mail.com",
                "password": "1233"
            }
        )
        alice_credentials = base64.b64encode(b'hhh:1233').decode('utf-8')

        self.app.post('users', headers={"Content-Type": "application/json"}, data=post_data)

        response = self.app.delete('users/1', headers={'Authorization': f'Basic {alice_credentials}'})
        self.assertEqual(200, response.status_code)


    def test_delete_userbyId_no_Id(self):
        post_data = json.dumps(
            {
                "username": "hhh",
                "email": "eh@mail.com",
                "password": "1233"
            }
        )
        alice_credentials = base64.b64encode(b'hhh:1233').decode('utf-8')

        self.app.post('users', headers={"Content-Type": "application/json"}, data=post_data)

        response = self.app.delete('users/2', headers={'Authorization': f'Basic {alice_credentials}'})
        self.assertEqual(400, response.status_code)


    def test_delete_userbyId_no_permisions(self):
        post_data = json.dumps(
            {
                "username": "user1",
                "email": "u1@mail.com",
                "password": "1233"
            }
        )

        self.app.post('users', headers={"Content-Type": "application/json"}, data=post_data)

        post_data = json.dumps(
            {
                "username": "user2",
                "email": "u2@mail.com",
                "password": "1233"
            }
        )
        alice_credentials = base64.b64encode(b'user1:1233').decode('utf-8')

        self.app.post('users', headers={"Content-Type": "application/json"}, data=post_data)

        response = self.app.delete('users/2',  headers={'Authorization': f'Basic {alice_credentials}'})
        self.assertEqual(403, response.status_code)


class Medications(BaseCase):

    def test_post_med_just_user(self):
        # user = self.test_usersId()
        # res = self.open_with_auth('/medications', 'POST', )
        post_data = json.dumps(
            {
                "username": "hhh",
                "email": "eh@mail.com",
                "password": "1233",
                'role': 'user'
            }
        )

        self.app.post('users', headers={"Content-Type": "application/json"}, data=post_data)

        med = json.dumps(
            {
                'id': 1,
                'name': 'name1',
                'description': 'description1',
                'cost': 12,
                'quantity': 10,
                'inStock': True
            }
        )
        # method='POST',
        alice_credentials = base64.b64encode(b'hhh:1233').decode('utf-8')
        res = self.app.post('/medications',
                            content_type='application/json',

                            headers={'Authorization': f'Basic {alice_credentials}'},
                            data=med
                             )
        self.assertEqual(403, res.status_code)


    def test_post_med_provisor(self):
        # user = self.test_usersId()
        # res = self.open_with_auth('/medications', 'POST', )
        post_data = json.dumps(
            {
                "username": "hhh",
                "email": "eh@mail.com",
                "password": "1233",
                'role': 'provisor'
            }
        )

        self.app.post('users', headers={"Content-Type": "application/json"}, data=post_data)

        med = json.dumps(
            {
                'id': 1,
                'name': 'name1',
                'description': 'description1',
                'cost': 12,
                'quantity': 10,
                'inStock': True
            }
        )
        # method='POST',
        alice_credentials = base64.b64encode(b'hhh:1233').decode('utf-8')
        res = self.app.post('/medications',
                            content_type='application/json',

                            headers={'Authorization': f'Basic {alice_credentials}'},
                            data=med
                            )
        self.assertEqual(200, res.status_code)


    def test_post_med_provisor_invalid(self):
        # user = self.test_usersId()
        # res = self.open_with_auth('/medications', 'POST', )
        post_data = json.dumps(
            {
                "username": "hhh",
                "email": "eh@mail.com",
                "password": "1233",
                'role': 'provisor'
            }
        )

        self.app.post('users', headers={"Content-Type": "application/json"}, data=post_data)

        med = json.dumps(
            {
                'id':1,
                'name': 'name1',
                'description': 'description1',
                'cost': 'erroe_not_integer',
                'quantity': 10,
                'inStock': True
            }
        )
        # method='POST',
        alice_credentials = base64.b64encode(b'hhh:1233').decode('utf-8')
        res = self.app.post('/medications',
                            content_type='application/json',

                            headers={'Authorization': f'Basic {alice_credentials}'},
                            data=med
                             )
        self.assertEqual(400, res.status_code)


    def test_get_med_by_Id(self):
        self.test_post_med_provisor()
        response = self.app.get('/medications/1')
        self.assertEqual(200, response.status_code)


    def test_get_med_by_non_Id(self):
        response = self.app.get('/medications/1')
        self.assertEqual(404, response.status_code)


    def test_get_med_by_invalid_Id(self):
        response = self.app.get('/medications/invalid_Id')
        self.assertEqual(400, response.status_code)

    def test_post_order(self):
        post_data = json.dumps(
            {
                "username": "hhh",
                "email": "eh@mail.com",
                "password": "1233",
                'role': 'provisor'
            }
        )

        self.app.post('users', headers={"Content-Type": "application/json"}, data=post_data)

        med = json.dumps(
            {
                'id': 1,
                'name': 'name1',
                'description': 'description1',
                'cost': 12,
                'quantity': 10,
                'inStock': True
            }
        )
        # method='POST',
        alice_credentials = base64.b64encode(b'hhh:1233').decode('utf-8')
        res = self.app.post('/medications',
                            content_type='application/json',

                            headers={'Authorization': f'Basic {alice_credentials}'},
                            data=med
                            )

        post_data = json.dumps(
            {
                "username": "hhhf",
                "email": "ehos@mail.com",
                "password": "12334",
                'role': 'user'
            }
        )

        self.app.post('users', headers={"Content-Type": "application/json"}, data=post_data)

        # method='POST',
        alice_credentials = base64.b64encode(b'hhhf:12334').decode('utf-8')

        order_data = json.dumps(
            {
            # 'user_id': data['userId'],
            'medicationId': '1',
            'amount': 1
            }
        )

        order = self.app.post('/store/orders',
                      content_type='application/json',

                      headers={'Authorization': f'Basic {alice_credentials}'},
                      data=order_data
                      )
        self.assertEqual(200, order.status_code)


    def test_post_order_invalid_data(self):
        post_data = json.dumps(
            {
                "username": "hhh",
                "email": "eh@mail.com",
                "password": "1233",
                'role': 'provisor'
            }
        )

        self.app.post('users', headers={"Content-Type": "application/json"}, data=post_data)

        med = json.dumps(
            {
                'id': 1,
                'name': 'name1',
                'description': 'description1',
                'cost': 12,
                'quantity': 10,
                'inStock': True
            }
        )
        # method='POST',
        alice_credentials = base64.b64encode(b'hhh:1233').decode('utf-8')
        res = self.app.post('/medications',
                            content_type='application/json',

                            headers={'Authorization': f'Basic {alice_credentials}'},
                            data=med
                            )

        post_data = json.dumps(
            {
                "username": "hhhf",
                "email": "ehos@mail.com",
                "password": "12334",
                'role': 'user'
            }
        )

        self.app.post('users', headers={"Content-Type": "application/json"}, data=post_data)

        # method='POST',
        alice_credentials = base64.b64encode(b'hhhf:12334').decode('utf-8')

        order_data = json.dumps(
            {
            # 'user_id': data['userId'],
            'medicationId': '1',
            'amount': 'invalid_not_integer'
            }
        )

        order = self.app.post('/store/orders',
                      content_type='application/json',

                      headers={'Authorization': f'Basic {alice_credentials}'},
                      data=order_data
                      )
        self.assertEqual(400, order.status_code)


    def test_post_order_no_med(self):
        post_data = json.dumps(
            {
                "username": "hhh",
                "email": "eh@mail.com",
                "password": "1233",
                'role': 'provisor'
            }
        )

        self.app.post('users', headers={"Content-Type": "application/json"}, data=post_data)

        post_data = json.dumps(
            {
                "username": "hhhf",
                "email": "ehos@mail.com",
                "password": "12334",
                'role': 'user'
            }
        )

        self.app.post('users', headers={"Content-Type": "application/json"}, data=post_data)

        # method='POST',
        alice_credentials = base64.b64encode(b'hhhf:12334').decode('utf-8')

        order_data = json.dumps(
            {
            # 'user_id': data['userId'],
            'medicationId': '1',
            'amount': 'invalid_not_integer'
            }
        )

        order = self.app.post('/store/orders',
                      content_type='application/json',

                      headers={'Authorization': f'Basic {alice_credentials}'},
                      data=order_data
                      )
        self.assertEqual(400, order.status_code)


    def test_put_med(self):
        self.test_post_med_provisor()
        put_med = json.dumps(
            {
                'id': 1,
                'name': 'new_name',
                'description': 'description1',
                'cost': 12,
                'quantity': 10,
                'inStock': True
            }
        )
        # method='POST',
        alice_credentials = base64.b64encode(b'hhh:1233').decode('utf-8')
        res = self.app.put('/medications/1',
                            content_type='application/json',

                            headers={'Authorization': f'Basic {alice_credentials}'},
                            data=put_med
                            )
        self.assertEqual(200, res.status_code)


    def test_put_med(self):
        self.test_post_med_provisor()
        put_med = json.dumps(
            {
                'id': 1,
                'name': 'new_name',
                'description': 'description1',
                'cost': 12,
                'quantity': 10,
                'inStock': True
            }
        )
        # method='POST',
        alice_credentials = base64.b64encode(b'hhh:1233').decode('utf-8')
        res = self.app.put('/medications/1',
                            content_type='application/json',

                            headers={'Authorization': f'Basic {alice_credentials}'},
                            data=put_med
                            )
        self.assertEqual(200, res.status_code)


    def test_put_invalid_med(self):
        self.test_post_med_provisor()
        put_med = json.dumps(
            {
                'id': 1,
                'name': 'new_name',
                'description': 'description1',
                'cost': 'invalid',
                'quantity': 10,
                'inStock': True
            }
        )
        # method='POST',
        alice_credentials = base64.b64encode(b'hhh:1233').decode('utf-8')
        res = self.app.put('/medications/1',
                            content_type='application/json',

                            headers={'Authorization': f'Basic {alice_credentials}'},
                            data=put_med
                            )
        self.assertEqual(400, res.status_code)


    def test_put_non_med(self):
        self.test_post_med_provisor()
        put_med = json.dumps(
            {
                'id': 1,
                'name': 'new_name',
                'description': 'description1',
                'cost': 12,
                'quantity': 10,
                'inStock': True
            }
        )
        # method='POST',
        alice_credentials = base64.b64encode(b'hhh:1233').decode('utf-8')
        res = self.app.put('/medications/2',
                            content_type='application/json',

                            headers={'Authorization': f'Basic {alice_credentials}'},
                            data=put_med
                            )
        self.assertEqual(404, res.status_code)


    def test_put_invalid_medId(self):
        self.test_post_med_provisor()
        put_med = json.dumps(
            {
                'id': 1,
                'name': 'new_name',
                'description': 'description1',
                'cost': 12,
                'quantity': 10,
                'inStock': True
            }
        )
        # method='POST',
        alice_credentials = base64.b64encode(b'hhh:1233').decode('utf-8')
        res = self.app.put('/medications/invalid',
                            content_type='application/json',

                            headers={'Authorization': f'Basic {alice_credentials}'},
                            data=put_med
                            )
        self.assertEqual(400, res.status_code)


    def test_delete_med(self):
        self.test_post_med_provisor()
        alice_credentials = base64.b64encode(b'hhh:1233').decode('utf-8')
        res = self.app.delete('/medications/1',
                              headers={'Authorization': f'Basic {alice_credentials}'},
                              )
        self.assertEqual(200, res.status_code)


    def test_delete_invalid_medId(self):
        self.test_post_med_provisor()
        alice_credentials = base64.b64encode(b'hhh:1233').decode('utf-8')
        res = self.app.delete('/medications/invalid_Id',
                           headers={'Authorization': f'Basic {alice_credentials}'},
                           )
        self.assertEqual(400, res.status_code)


    def test_get_order(self):
        post_data = json.dumps(
            {
                "username": "hhh",
                "email": "eh@mail.com",
                "password": "1233",
                'role': 'provisor'
            }
        )

        self.app.post('users', headers={"Content-Type": "application/json"}, data=post_data)

        med = json.dumps(
            {
                'id': 1,
                'name': 'name1',
                'description': 'description1',
                'cost': 12,
                'quantity': 10,
                'inStock': True
            }
        )
        # method='POST',
        alice_credentials = base64.b64encode(b'hhh:1233').decode('utf-8')
        res = self.app.post('/medications',
                            content_type='application/json',

                            headers={'Authorization': f'Basic {alice_credentials}'},
                            data=med
                            )

        post_data = json.dumps(
            {
                "username": "hhhf",
                "email": "ehos@mail.com",
                "password": "12334",
                'role': 'user'
            }
        )

        self.app.post('users', headers={"Content-Type": "application/json"}, data=post_data)

        # method='POST',
        alice_credentials = base64.b64encode(b'hhhf:12334').decode('utf-8')

        order_data = json.dumps(
            {
                # 'user_id': data['userId'],
                'medicationId': '1',
                'amount': 1
            }
        )

        self.app.post('/store/orders',
                              content_type='application/json',

                              headers={'Authorization': f'Basic {alice_credentials}'},
                              data=order_data
                              )
        response = self.app.get('/store/orders/1', headers={'Authorization': f'Basic {alice_credentials}'})
        self.assertEqual(200, response.status_code)


    def test_get_no_order(self):

        post_data = json.dumps(
            {
                "username": "hhhf",
                "email": "ehos@mail.com",
                "password": "12334",
                'role': 'user'
            }
        )

        self.app.post('users', headers={"Content-Type": "application/json"}, data=post_data)

        # method='POST',
        alice_credentials = base64.b64encode(b'hhhf:12334').decode('utf-8')

        response = self.app.get('/store/orders/1', headers={'Authorization': f'Basic {alice_credentials}'})
        self.assertEqual(404, response.status_code)


    def test_get_order_no_permisions(self):
        post_data = json.dumps(
            {
                "username": "hhh",
                "email": "eh@mail.com",
                "password": "1233",
                'role': 'provisor'
            }
        )

        self.app.post('users', headers={"Content-Type": "application/json"}, data=post_data)

        med = json.dumps(
            {
                'id': 1,
                'name': 'name1',
                'description': 'description1',
                'cost': 12,
                'quantity': 10,
                'inStock': True
            }
        )
        # method='POST',
        alice_credentials = base64.b64encode(b'hhh:1233').decode('utf-8')
        res = self.app.post('/medications',
                            content_type='application/json',

                            headers={'Authorization': f'Basic {alice_credentials}'},
                            data=med
                            )

        post_data = json.dumps(
            {
                "username": "hhhf",
                "email": "ehos@mail.com",
                "password": "12334",
                'role': 'user'
            }
        )

        self.app.post('users', headers={"Content-Type": "application/json"}, data=post_data)

        # method='POST',
        alice_credentials = base64.b64encode(b'hhhf:12334').decode('utf-8')

        order_data = json.dumps(
            {
                # 'user_id': data['userId'],
                'medicationId': '1',
                'amount': 1
            }
        )

        self.app.post('/store/orders',
                              content_type='application/json',

                              headers={'Authorization': f'Basic {alice_credentials}'},
                              data=order_data
                              )
        post_data = json.dumps(
            {
                "username": "user3",
                "email": "u3@mail.com",
                "password": "12334",
                'role': 'user'
            }
        )

        self.app.post('users', headers={"Content-Type": "application/json"}, data=post_data)

        # method='POST',
        alice_credentials = base64.b64encode(b'user3:12334').decode('utf-8')

        response = self.app.get('/store/orders/1', headers={'Authorization': f'Basic {alice_credentials}'})
        self.assertEqual(403, response.status_code)


class FirstLab(BaseCase):

    def test_variant(self):
        request = self.app.get('/api/v1/hello-world-15')
        self.assertEqual(200, request.status_code)


if __name__ == '__main__':

    unittest.main()
