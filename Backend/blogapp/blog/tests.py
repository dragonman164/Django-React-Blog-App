from rest_framework.test import APITestCase
from django.urls import reverse


class AuthenticationViewTests(APITestCase):
    def setUp(self) -> None:
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.user_data = {
            "email" : "abcd@gmail.com",
            "password" : "123",
            "name" : "Sanidhiya",
            "phoneno" : "911234567890",
            "gender" : "Male"
        }
        self.login_data = {
            "username" : "abcd@gmail.com",
            "password" : "123"
        }
        return super().setUp()


    def register_user(self):
        return self.client.post(path=self.register_url,data=self.user_data,format="json")

    def login_user(self):
        return self.client.post(self.login_url, self.login_data, format="json")

    def tearDown(self) -> None:
        return super().tearDown()
    
    def test_user_register_with_no_data(self):
        res = self.client.post(self.register_url)
        self.assertEqual(res.status_code, 400)

    def test_user_register_with_correct_data(self):
        res = self.register_user()
        self.assertEqual(res.status_code,201)
        self.assertEqual(res.data , {
            "name" : "Sanidhiya",
            "phoneno" : "911234567890",
            "address" : None, 
            "dob" : None,
            "profession" : None, 
            "gender" : "Male"
        })

    def test_user_login_with_no_data(self):
        res = self.client.post(self.login_url)  
        self.assertEqual(res.status_code, 400)

    def test_user_login_with_correct_data(self):
        self.register_user()
        res = self.login_user()
        self.assertEqual(res.status_code, 200)
        self.assertIn('token',res.data.keys())
    

class BlogUserViewTest(APITestCase):
    def register_user(self):
        return self.client.post(path=self.register_url,data=self.user_data,format="json")

    def login_user(self):
        return self.client.post(self.login_url, self.login_data, format="json")
    
    
    def setUp(self) -> None:
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.user_url = reverse('userview')
        self.user_data = {
            "email" : "abcd@gmail.com",
            "password" : "123",
            "name" : "Sanidhiya",
            "phoneno" : "911234567890",
            "gender" : "Male"
        }
        self.login_data = {
            "username" : "abcd@gmail.com",
            "password" : "123"
        }
        self.register_user()
        res = self.login_user()
        self.token = res.data['token']
        return super().setUp()

    def test_fetch_user_details(self):
        res = self.client.get(self.user_url,headers = {'Authorization' : f'Token {self.token}'})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data , {
            "name" : "Sanidhiya",
            "phoneno" : "911234567890",
            "address" : None, 
            "dob" : None,
            "profession" : None, 
            "gender" : "Male"
        })

    def test_update_user_details(self):
        pass
    
    def test_delete_user(self):
        res = self.client.delete(self.user_url,headers = {'Authorization' : f'Token {self.token}'})
        self.assertEqual(res.status_code,204)

    def tearDown(self) -> None:
        return super().tearDown()
    
class BlogViewTest(APITestCase):
    pass