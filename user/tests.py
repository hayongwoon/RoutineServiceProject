from django.urls import reverse
from rest_framework.test import APITestCase

from user.models import User as UserModel


class UserRegisterationAPIViewTestCase(APITestCase):
    def test_correct_registeration_case(self):
        url = reverse("signup")
        user_data = {
            "email": "test@test.com",
            "password": "test1234!!",
            "username": "hayongwoon"
        }
        response = self.client.post(url, user_data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['email'], "test@test.com")
        self.assertEqual(response.data['username'], "hayongwoon")
    
    
    def test_password_length_is_less_than_eight_charaters_case(self):
        url = reverse("signup")
        user_data = {
            "email": "test@test.com",
            "password": "test1!!",
            "username": "hayongwoon"
        }
        response = self.client.post(url, user_data)

        self.assertEqual(response.status_code, 400)


    def test_special_character_is_not_in_password_case(self):
        url = reverse("signup")
        user_data = {
            "email": "test@test.com",
            "password": "test12345",
            "username": "hayongwoon"
        }
        response = self.client.post(url, user_data)

        self.assertEqual(response.status_code, 400)


    def test_numbers_is_not_in_password_case(self):
        url = reverse("signup")
        user_data = {
            "email": "test@test.com",
            "password": "test!!@@",
            "username": "hayongwoon"
        }
        response = self.client.post(url, user_data)

        self.assertEqual(response.status_code, 400)

    
    def test_alpha_is_not_in_password_case(self):
        url = reverse("signup")
        user_data = {
            "email": "test@test.com",
            "password": "1234!!@@",
            "username": "hayongwoon"
        }
        response = self.client.post(url, user_data)

        self.assertEqual(response.status_code, 400)

    
    def test_not_email_in_email_field_case(self):
        url = reverse("signup")
        user_data = {
            "email": "test",
            "password": "test1234!!",
            "username": "hayongwoon"
        }
        response = self.client.post(url, user_data)

        self.assertEqual(response.status_code, 400)
       
   
    def test_blank_in_username_field_case(self):
        url = reverse("signup")
        user_data = {
            "email": "test@test.com",
            "password": "test1234!!",
        }
        response = self.client.post(url, user_data)

        self.assertEqual(response.status_code, 400)

    
    def test_user_with_this_email_already_exists_case(self):
        self.data = {'email': 'test@test.com', 'password': 'test1234!!'}
        self.user = UserModel.objects.create_user(**self.data)

        url = reverse("signup")
        user_data = {
            "email": "test@test.com",
            "password": "test1234!!",
        }
        response = self.client.post(url, user_data)

        self.assertEqual(response.status_code, 400)
       

class UserLoginAPIViewTestCase(APITestCase):
    def setUp(self):
        self.data = {'email': 'test@test.com', 'password': 'test1234!!'}
        self.user = UserModel.objects.create_user(**self.data)


    def test_correct_login_case(self):
        url = reverse('login')
        user_data = {
            "email": "test@test.com",
            "password": "test1234!!"
        }

        response = self.client.post(url, user_data)

        self.assertEqual(response.status_code, 200)


    def test_input_incorrect_password_case(self):
        url = reverse('login')
        user_data = {
            "email": "test@test.com",
            "password": "rest1234!!"
        }

        response = self.client.post(url, user_data)

        self.assertEqual(response.status_code, 401)


    def test_input_incorrect_email_case(self):
        url = reverse('login')
        user_data = {
            "email": "rest@test.com",
            "password": "test1234!!"
        }

        response = self.client.post(url, user_data)

        self.assertEqual(response.status_code, 401)


class UserLogoutAPIViewTestCase(APITestCase):
    def setUp(self):
        self.data = {'email': 'test@test.com', 'password': 'test1234!!'}
        self.user = UserModel.objects.create_user(**self.data)


    def test_correction_logout_case(self):
        url = reverse('logout')

        self.client.force_login(self.user)
        response = self.client.post(url)

        self.assertEqual(response.status_code, 202)
        
