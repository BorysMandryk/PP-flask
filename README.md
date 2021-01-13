# PP-flask
1. Клонувати репозиторій.
2. Створити й активувати віртуальне середовище.
3. Встановити залежності.
4. Запустити WSGI-сервер.


C:\Users\Andri\AppData\Local\Programs\Python\Python37\python.exe -m pip install
set 

{
    "username": "user",
    "email": "e@mail.com",
    "password": "1233"
}
C:\Users\Andri\AppData\Local\pypoetry\Cache\virtualenvs\pp-flask-1o64LXyr-py3.7\Scripts\activate
python -m unittest -v
coverage run -m unittest -v
coverage report -m




python -m unittest test_app
coverage run -m unittest test_app
coverage report -m


 headers={
                                 # 'Authorization': 'Basic ' + base64.b64encode(user['username'] + ":" + user['password']),
                                 # 'Authorization': 'Basic ' + base64.b64encode(bytes(user['username'] + ":" + user['password'], 'ascii')).decode('ascii'),
                                 
                             },
                             
                             
                       
    def test_users_post(self):
        post_data = json.dumps(
            {
                "username": "hhh",
                "email": "eh@mail.com",
                "password": "1233"
            }
        )

        response = self.app.post('users', headers={"Content-Type": "application/json"}, data=post_data)
        self.assertEqual(201, response.status_code)


    def test_re(self):
        self.assertEqual(2, 2)