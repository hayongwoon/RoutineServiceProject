from django.urls import reverse
from rest_framework.test import APITestCase
from routine_result.models import RoutineResult as RoutineResultModel

from user.models import User as UserModel
from routine.models import Routine as RoutineModel


class CreateRoutineAPIViewTestCase(APITestCase):
    def setUp(self):
        self.data = {'email': 'test@test.com', 'password': 'test1234!!'}
        self.user = UserModel.objects.create_user(**self.data)
        self.client.force_login(self.user)

    def test_create_routine_case(self):
        url = reverse('routines')
        routine_data = {
            "title": "problem solving",
            "category": "HOMEWORK",
            "goal": "Increase your problem-solving skills",
            "is_alarm": True,
            "get_days_list": ["MON", "WED", "FRI"]
        }

        response = self.client.post(url, routine_data)

        routine = RoutineModel.objects.get(id=1)
        routine_result = RoutineResultModel.objects.get(routine=routine)
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(routine.account.email, 'test@test.com')
        self.assertEqual(routine_result.result, 'NOT')
        self.assertEqual(response.data['days'], ["MON", "WED", "FRI"])

    def test_input_category_is_not_in_category_choices_case(self):
        url = reverse('routines')
        routine_data = {
            "title": "problem solving",
            "category": "NOT HOMEWORK or MIRACLE",
            "goal": "Increase your problem-solving skills",
            "is_alarm": True,
            "get_days_list": ["MON", "WED", "FRI"]
        }

        response = self.client.post(url, routine_data)

        self.assertEqual(response.status_code, 400)

    def test_title_field_is_blank_case(self):
        url = reverse('routines')
        routine_data = {
            "title": "",
            "category": "MIRACLE",
            "goal": "Increase your problem-solving skills",
            "is_alarm": True,
            "get_days_list": ["MON", "WED", "FRI"]
        }

        response = self.client.post(url, routine_data)

        self.assertEqual(response.status_code, 400)

    def test_goal_field_is_blank_case(self):
        url = reverse('routines')
        routine_data = {
            "title": "problem solving",
            "category": "MIRACLE",
            "goal": "",
            "is_alarm": True,
            "get_days_list": ["MON", "WED", "FRI"]
        }

        response = self.client.post(url, routine_data)

        self.assertEqual(response.status_code, 400)

    
class UpdateRoutineAPIViewTestCase(APITestCase):
    def setUp(self):
        self.data = {'email': 'test@test.com', 'password': 'test1234!!'}
        self.user = UserModel.objects.create_user(**self.data)
        self.client.force_login(self.user)

        url = reverse('routines')
        routine_data = {
            "title": "problem solving",
            "category": "HOMEWORK",
            "goal": "Increase your problem-solving skills",
            "is_alarm": True,
            "get_days_list": ["MON", "WED", "FRI"]
        }

        self.client.post(url, routine_data)

    def test_update_my_routine_title_and_goal_case(self):
        url = reverse('routines')
        routine_data = {
            "routine_id" : 1,
            "title": "put test title",
            "category": "HOMEWORK",
            "goal": "put test goal",
            "is_alarm": True,
            "get_days_list": ["MON", "WED", "FRI"]
        }

        response = self.client.put(url, routine_data)

        self.assertEqual(response.status_code, 202)
        self.assertEqual(response.data["title"], "put test title")
        self.assertEqual(response.data["goal"], "put test goal")

    def test_update_my_routine_days_case(self):
        url = reverse('routines')
        routine_data = {
            "routine_id" : 1,
            "title": "problem solving",
            "category": "HOMEWORK",
            "goal": "Increase your problem-solving skills",
            "is_alarm": True,
            "get_days_list": ["SUN", "SAT"]
        }

        response = self.client.put(url, routine_data)

        self.assertEqual(response.status_code, 202)
        self.assertEqual(response.data["days"], ["SUN", "SAT"])

    def test_update_my_routine_category_case(self):
        url = reverse('routines')
        routine_data = {
            "routine_id" : 1,
            "title": "problem solving",
            "category": "MIRACLE",
            "goal": "Increase your problem-solving skills",
            "is_alarm": True,
            "get_days_list": ["SUN", "SAT"]
        }

        response = self.client.put(url, routine_data)

        self.assertEqual(response.status_code, 202)
        self.assertEqual(response.data["category"], "MIRACLE")

    def test_another_user_try_my_routine_case(self):
        self.data = {'email': 'anotheruser@anotheruser.com', 'password': 'test1234!!'}
        self.user = UserModel.objects.create_user(**self.data)
        self.client.force_login(self.user)

        url = reverse('routines')
        routine_data = {
            "routine_id" : 1,
            "title": "problem solving",
            "category": "HOMEWORK",
            "goal": "Increase your problem-solving skills",
            "is_alarm": True,
            "get_days_list": ["MON", "WED", "FRI"]
        }

        response = self.client.put(url, routine_data)

        self.assertEqual(response.status_code, 403)


class DeleteRoutineAPIViewTestCase(APITestCase):
    def setUp(self):
        self.data = {'email': 'test@test.com', 'password': 'test1234!!'}
        self.user = UserModel.objects.create_user(**self.data)
        self.client.force_login(self.user)

        url = reverse('routines')
        routine_data = {
            "title": "problem solving",
            "category": "HOMEWORK",
            "goal": "Increase your problem-solving skills",
            "is_alarm": True,
            "get_days_list": ["MON", "WED", "FRI"]
        }

        self.client.post(url, routine_data)

    def test_delete_my_routine_case(self):
        url = reverse('routines')
        request_data = {
            "account_id" : 1,
            "routine_id" : 1
        }

        response = self.client.delete(url, request_data)
        routine = RoutineModel.objects.get(id=request_data["routine_id"])
        routine_result = RoutineResultModel.objects.get(routine=routine)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(routine.is_deleted, True)
        self.assertEqual(routine_result.is_deleted, True)
        self.assertEqual(response.data["message"], "삭제 완료!!")

    def test_cancle_delete_my_routine_case(self):
        url = reverse('routines')
        request_data = {
            "account_id" : 1,
            "routine_id" : 1
        }

        self.client.delete(url, request_data)
        response = self.client.delete(url, request_data)

        routine = RoutineModel.objects.get(id=request_data["routine_id"])
        routine_result = RoutineResultModel.objects.get(routine=routine)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(routine.is_deleted, False)
        self.assertEqual(routine_result.is_deleted, False)
        self.assertEqual(response.data["message"], "삭제 취소!!")

    def test_another_user_delete_my_routine_case(self):
        self.data = {'email': 'anotheruser@anotheruser.com', 'password': 'test1234!!'}
        self.user = UserModel.objects.create_user(**self.data)
        self.client.force_login(self.user)

        url = reverse('routines')
        request_data = {
            "account_id" : 1,
            "routine_id" : 1
        }

        response = self.client.delete(url, request_data)
        
        self.assertEqual(response.status_code, 403)


