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
        session.close()
        session.commit()

    user1 = json.dumps(
        {
            "username": "user1",
            "email": "u1@mail.com",
            "password": "1233",
            "role": "user"
        }
    )

    user2 = json.dumps(
        {
            "username": "user2",
            "email": "u2lo@mail.com",
            "password": "1233",
            "role": "user"
        }
    )

    provisor = json.dumps(
        {
            "username": "provizorro",
            "email": "eh@mail.com",
            "password": "1233",
            "role": "provisor"
        }
    )

    medication = json.dumps(
            {
                'id': 1,
                'name': 'name1',
                'description': 'description1',
                'cost': 12,
                'quantity': 10,
                'inStock': True
            }
        )

    order_data = json.dumps(
        {
            'medicationId': '1',
            'amount': 1
        }
    )

    order_data_large_amount = json.dumps(
        {
            'medicationId': '1',
            'amount': 100
        }
    )

    order_data_invalid = json.dumps(
        {
            'medicationId': 'invalid_id',
            'amount': 'invalid_not_integer'
        }
    )

    medication_invalid = json.dumps(
            {
                'id':1,
                'name': 'name1',
                'description': 'description1',
                'cost': 'error_not_integer',
                'quantity': 10,
                'inStock': True
            }
        )

    user1_invalid_email = json.dumps(
        {
            "username": "user1",
            "email": "u1mail.com",
            "password": "1233",
            "role": "user"
        }
    )


class User(BaseCase):

    def test_user_post(self):
       post_data = self.user1
       response = self.app.post('users', headers={"Content-Type": "application/json"}, data=post_data)

       self.assertEqual(201, response.status_code)

    def test_invaid_users(self):
       post_data = self.user1_invalid_email
       response = self.app.post('users', headers={"Content-Type": "application/json"}, data=post_data)

       self.assertEqual(400, response.status_code)

    def test_same_user(self):
       post_data = self.user1
       self.app.post('users', headers={"Content-Type": "application/json"}, data=post_data)
       response = self.app.post('users', headers={"Content-Type": "application/json"}, data=post_data)

       self.assertEqual(400, response.status_code)

    def test_get_user(self):
        post_data = self.user1
        self.app.post('users', headers={"Content-Type": "application/json"}, data=post_data)
        response = self.app.get('users/1')

        self.assertEqual(200, response.status_code)

    def test_get_no_user(self):
        response = self.app.get('users/1')

        self.assertEqual(404, response.status_code)

    def test_get_userby_not_int(self):
        response = self.app.get('users/not_integer')

        self.assertEqual(400, response.status_code)

    def test_put_user(self):
       post_data = self.user1
       self.app.post('users', headers={"Content-Type": "application/json"}, data=post_data)
       auth = base64.b64encode(b'user1:1233').decode('utf-8')
       put_data = self.user2
       response = self.app.put('users/1', content_type='application/json', headers={'Authorization': f'Basic {auth}'}, data=put_data)

       self.assertEqual(200, response.status_code)

    def test_put_no_user(self):
       post_data = self.user1
       self.app.post('users', headers={"Content-Type": "application/json"}, data=post_data)

       auth = base64.b64encode(b'user1:1233').decode('utf-8')
       put_data = self.user2
       response = self.app.put('users/2', content_type='application/json', headers={'Authorization': f'Basic {auth}'}, data=put_data)

       self.assertEqual(400, response.status_code)

    def test_put_invalid(self):
       post_data = self.user1
       self.app.post('users', headers={"Content-Type": "application/json"}, data=post_data)

       auth = base64.b64encode(b'user1:1233').decode('utf-8')
       put_data = self.user1_invalid_email
       response = self.app.put('users/1', content_type='application/json', headers={'Authorization': f'Basic {auth}'}, data=put_data)

       self.assertEqual(400, response.status_code)

    def test_put_not_same_user(self):
       post_data = self.user1
       self.app.post('users', headers={"Content-Type": "application/json"}, data=post_data)

       post_data = self.user2
       self.app.post('users', headers={"Content-Type": "application/json"}, data=post_data)

       put_data = self.user1
       auth = base64.b64encode(b'user2:1233').decode('utf-8')
       response = self.app.put('users/1', content_type='application/json', headers={'Authorization': f'Basic {auth}'}, data=put_data)

       self.assertEqual(403, response.status_code)

    def test_put_not_busy_username(self):
       post_data = self.user1
       self.app.post('users', headers={"Content-Type": "application/json"}, data=post_data)

       post_data = self.user2
       self.app.post('users', headers={"Content-Type": "application/json"}, data=post_data)

       auth = base64.b64encode(b'user2:1233').decode('utf-8')
       put_data = self.user1
       response = self.app.put('users/2', content_type='application/json', headers={'Authorization': f'Basic {auth}'}, data=put_data)

       self.assertEqual(400, response.status_code)

    def test_delete_user(self):
        post_data = self.user1
        self.app.post('users', headers={"Content-Type": "application/json"}, data=post_data)

        auth = base64.b64encode(b'user1:1233').decode('utf-8')
        response = self.app.delete('users/1', headers={'Authorization': f'Basic {auth}'})

        self.assertEqual(200, response.status_code)

    def test_delete_no_user(self):
        post_data = self.user1
        self.app.post('users', headers={"Content-Type": "application/json"}, data=post_data)

        auth = base64.b64encode(b'user1:1233').decode('utf-8')
        response = self.app.delete('users/2', headers={'Authorization': f'Basic {auth}'})

        self.assertEqual(400, response.status_code)

    def test_delete_no_permisions(self):
        post_data = self.user1
        self.app.post('users', headers={"Content-Type": "application/json"}, data=post_data)

        post_data = self.user2
        self.app.post('users', headers={"Content-Type": "application/json"}, data=post_data)

        auth = base64.b64encode(b'user1:1233').decode('utf-8')
        response = self.app.delete('users/2',  headers={'Authorization': f'Basic {auth}'})

        self.assertEqual(403, response.status_code)


class Medications(BaseCase):

    def test_post_med_user(self):
        post_data = self.user1
        self.app.post('users', headers={"Content-Type": "application/json"}, data=post_data)

        med = self.medication
        auth = base64.b64encode(b'user1:1233').decode('utf-8')
        response = self.app.post('/medications',
                            content_type='application/json',
                            headers={'Authorization': f'Basic {auth}'},
                            data=med
                            )

        self.assertEqual(403, response.status_code)

    def test_post_med_provisor(self):
        post_data = self.provisor
        self.app.post('users', headers={"Content-Type": "application/json"}, data=post_data)

        med = self.medication
        auth = base64.b64encode(b'provizorro:1233').decode('utf-8')
        response = self.app.post('/medications',
                            content_type='application/json',
                            headers={'Authorization': f'Basic {auth}'},
                            data=med
                            )

        self.assertEqual(200, response.status_code)

    def test_post_med_provisor_invalid(self):
        post_data = self.provisor
        self.app.post('users', headers={"Content-Type": "application/json"}, data=post_data)

        med = self.medication_invalid
        auth = base64.b64encode(b'provizorro:1233').decode('utf-8')
        response = self.app.post('/medications',
                            content_type='application/json',
                            headers={'Authorization': f'Basic {auth}'},
                            data=med
                             )

        self.assertEqual(400, response.status_code)

    def test_get_medication(self):
        post_data = self.provisor
        self.app.post('users', headers={"Content-Type": "application/json"}, data=post_data)

        med = self.medication
        auth = base64.b64encode(b'provizorro:1233').decode('utf-8')
        self.app.post('/medications',
                                 content_type='application/json',
                                 headers={'Authorization': f'Basic {auth}'},
                                 data=med
                                 )
        response = self.app.get('/medications/1')

        self.assertEqual(200, response.status_code)

    def test_get_no_medication(self):
        response = self.app.get('/medications/1')

        self.assertEqual(404, response.status_code)

    def test_get_medication_invalid(self):
        response = self.app.get('/medications/invalid_Id')

        self.assertEqual(400, response.status_code)

    def test_post_order(self):
        provisor_data = self.provisor
        self.app.post('users', headers={"Content-Type": "application/json"}, data=provisor_data)

        med = self.medication
        auth = base64.b64encode(b'provizorro:1233').decode('utf-8')
        self.app.post('/medications',
                                 content_type='application/json',
                                 headers={'Authorization': f'Basic {auth}'},
                                 data=med
                                 )

        user_data = self.user1
        self.app.post('users', headers={"Content-Type": "application/json"}, data=user_data)

        order_data = self.order_data
        auth = base64.b64encode(b'user1:1233').decode('utf-8')
        order = self.app.post('/store/orders',
                      content_type='application/json',
                      headers={'Authorization': f'Basic {auth}'},
                      data=order_data
                      )

        self.assertEqual(200, order.status_code)

    def test_post_order_invalid(self):
        provisor_data = self.provisor
        self.app.post('users', headers={"Content-Type": "application/json"}, data=provisor_data)

        med = self.medication
        auth = base64.b64encode(b'provizorro:1233').decode('utf-8')
        self.app.post('/medications',
                      content_type='application/json',
                      headers={'Authorization': f'Basic {auth}'},
                      data=med
                      )

        user_data = self.user1
        self.app.post('users', headers={"Content-Type": "application/json"}, data=user_data)

        order_data = self.order_data_invalid
        auth = base64.b64encode(b'user1:1233').decode('utf-8')
        order = self.app.post('/store/orders',
                              content_type='application/json',
                              headers={'Authorization': f'Basic {auth}'},
                              data=order_data
                              )

        self.assertEqual(400, order.status_code)

    def test_post_order_no_med(self):
        user_data = self.user1
        self.app.post('users', headers={"Content-Type": "application/json"}, data=user_data)

        order_data = self.order_data
        auth = base64.b64encode(b'user1:1233').decode('utf-8')
        order = self.app.post('/store/orders',
                              content_type='application/json',
                              headers={'Authorization': f'Basic {auth}'},
                              data=order_data
                              )

        self.assertEqual(404, order.status_code)

    def test_put_med(self):
        post_data = self.provisor
        self.app.post('users', headers={"Content-Type": "application/json"}, data=post_data)

        med = self.medication
        auth = base64.b64encode(b'provizorro:1233').decode('utf-8')
        self.app.post('/medications',
                                 content_type='application/json',
                                 headers={'Authorization': f'Basic {auth}'},
                                 data=med
                                 )

        put_med = self.medication
        auth = base64.b64encode(b'provizorro:1233').decode('utf-8')
        response = self.app.put('/medications/1',
                            content_type='application/json',

                            headers={'Authorization': f'Basic {auth}'},
                            data=put_med
                            )

        self.assertEqual(200, response.status_code)

    def test_put_invalid_med(self):
        post_data = self.provisor
        self.app.post('users', headers={"Content-Type": "application/json"}, data=post_data)

        med = self.medication
        auth = base64.b64encode(b'provizorro:1233').decode('utf-8')
        self.app.post('/medications',
                         content_type='application/json',
                         headers={'Authorization': f'Basic {auth}'},
                         data=med
                         )

        put_med = self.medication_invalid
        auth = base64.b64encode(b'provizorro:1233').decode('utf-8')
        response = self.app.put('/medications/1',
                            content_type='application/json',

                            headers={'Authorization': f'Basic {auth}'},
                            data=put_med
                            )

        self.assertEqual(400, response.status_code)

    def test_put_non_med(self):
        post_data = self.provisor
        self.app.post('users', headers={"Content-Type": "application/json"}, data=post_data)

        put_med = self.medication
        auth = base64.b64encode(b'provizorro:1233').decode('utf-8')
        response = self.app.put('/medications/2',
                            content_type='application/json',

                            headers={'Authorization': f'Basic {auth}'},
                            data=put_med
                            )

        self.assertEqual(404, response.status_code)

    def test_put_invalid_medId(self):
        post_data = self.provisor
        self.app.post('users', headers={"Content-Type": "application/json"}, data=post_data)

        med = self.medication
        auth = base64.b64encode(b'provizorro:1233').decode('utf-8')
        self.app.post('/medications',
                      content_type='application/json',
                      headers={'Authorization': f'Basic {auth}'},
                      data=med
                      )

        put_med = self.medication

        auth = base64.b64encode(b'provizorro:1233').decode('utf-8')
        res = self.app.put('/medications/invalid',
                            content_type='application/json',

                            headers={'Authorization': f'Basic {auth}'},
                            data=put_med
                            )

        self.assertEqual(400, res.status_code)

    def test_delete_med(self):
        post_data = self.provisor
        self.app.post('users', headers={"Content-Type": "application/json"}, data=post_data)

        med = self.medication
        auth = base64.b64encode(b'provizorro:1233').decode('utf-8')
        self.app.post('/medications',
                      content_type='application/json',
                      headers={'Authorization': f'Basic {auth}'},
                      data=med
                      )

        auth = base64.b64encode(b'provizorro:1233').decode('utf-8')
        res = self.app.delete('/medications/1',
                              headers={'Authorization': f'Basic {auth}'},
                              )

        self.assertEqual(200, res.status_code)

    def test_delete_invalid_medId(self):
        post_data = self.provisor
        self.app.post('users', headers={"Content-Type": "application/json"}, data=post_data)

        med = self.medication
        auth = base64.b64encode(b'provizorro:1233').decode('utf-8')
        self.app.post('/medications',
                      content_type='application/json',
                      headers={'Authorization': f'Basic {auth}'},
                      data=med
                      )

        auth = base64.b64encode(b'provizorro:1233').decode('utf-8')
        res = self.app.delete('/medications/invalid_Id',
                           headers={'Authorization': f'Basic {auth}'},
                           )

        self.assertEqual(400, res.status_code)

    def test_get_order(self):
        provisor_data = self.provisor
        self.app.post('users', headers={"Content-Type": "application/json"}, data=provisor_data)

        med = self.medication
        auth = base64.b64encode(b'provizorro:1233').decode('utf-8')
        self.app.post('/medications',
                      content_type='application/json',
                      headers={'Authorization': f'Basic {auth}'},
                      data=med
                      )

        user_data = self.user1
        self.app.post('users', headers={"Content-Type": "application/json"}, data=user_data)

        order_data = self.order_data
        auth = base64.b64encode(b'user1:1233').decode('utf-8')
        self.app.post('/store/orders',
                              content_type='application/json',
                              headers={'Authorization': f'Basic {auth}'},
                              data=order_data
                              )

        response = self.app.get('/store/orders/1', headers={'Authorization': f'Basic {auth}'})

        self.assertEqual(200, response.status_code)

    def test_get_order_invalid(self):
        provisor_data = self.provisor
        self.app.post('users', headers={"Content-Type": "application/json"}, data=provisor_data)

        med = self.medication
        auth = base64.b64encode(b'provizorro:1233').decode('utf-8')
        self.app.post('/medications',
                      content_type='application/json',
                      headers={'Authorization': f'Basic {auth}'},
                      data=med
                      )

        user_data = self.user1
        self.app.post('users', headers={"Content-Type": "application/json"}, data=user_data)

        order_data = self.order_data
        auth = base64.b64encode(b'user1:1233').decode('utf-8')
        self.app.post('/store/orders',
                              content_type='application/json',
                              headers={'Authorization': f'Basic {auth}'},
                              data=order_data
                              )

        response = self.app.get('/store/orders/1', headers={'Authorization': f'Basic {auth}'})

        self.assertEqual(200, response.status_code)

    def test_get_no_order(self):

        post_data = self.user1
        self.app.post('users', headers={"Content-Type": "application/json"}, data=post_data)

        auth = base64.b64encode(b'user1:1233').decode('utf-8')
        response = self.app.get('/store/orders/1', headers={'Authorization': f'Basic {auth}'})

        self.assertEqual(404, response.status_code)

    def test_get_order_no_permisions(self):
        provisor_data = self.provisor
        self.app.post('users', headers={"Content-Type": "application/json"}, data=provisor_data)

        med = self.medication
        auth = base64.b64encode(b'provizorro:1233').decode('utf-8')
        self.app.post('/medications',
                      content_type='application/json',
                      headers={'Authorization': f'Basic {auth}'},
                      data=med
                      )

        user_data = self.user1
        self.app.post('users', headers={"Content-Type": "application/json"}, data=user_data)

        order_data = self.order_data
        auth = base64.b64encode(b'user1:1233').decode('utf-8')
        self.app.post('/store/orders',
                      content_type='application/json',
                      headers={'Authorization': f'Basic {auth}'},
                      data=order_data
                      )

        post_data = self.user2
        self.app.post('users', headers={"Content-Type": "application/json"}, data=post_data)

        auth = base64.b64encode(b'user2:1233').decode('utf-8')
        response = self.app.get('/store/orders/1', headers={'Authorization': f'Basic {auth}'})

        self.assertEqual(403, response.status_code)

    def test_post_order_large_amount(self):
        """Demand creating"""
        provisor_data = self.provisor
        self.app.post('users', headers={"Content-Type": "application/json"}, data=provisor_data)

        med = self.medication
        auth = base64.b64encode(b'provizorro:1233').decode('utf-8')
        self.app.post('/medications',
                      content_type='application/json',
                      headers={'Authorization': f'Basic {auth}'},
                      data=med
                      )

        user_data = self.user1
        self.app.post('users', headers={"Content-Type": "application/json"}, data=user_data)

        order_data = self.order_data_large_amount
        auth = base64.b64encode(b'user1:1233').decode('utf-8')
        order = self.app.post('/store/orders',
                              content_type='application/json',
                              headers={'Authorization': f'Basic {auth}'},
                              data=order_data
                              )

        self.assertEqual(201, order.status_code)


class FirstLab(BaseCase):

    def test_variant(self):
        request = self.app.get('/api/v1/hello-world-15')
        self.assertEqual(200, request.status_code)


if __name__ == '__main__':
    unittest.main()
