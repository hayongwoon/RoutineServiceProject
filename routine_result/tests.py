from django.urls import reverse
from rest_framework.test import APITestCase
from routine_result.models import RoutineResult as RoutineResultModel

from user.models import User as UserModel
from routine.models import Routine as RoutineModel


class CreateRoutineResultAPIViewTestCase(APITestCase):
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

    def test_update_routine_result_case(self):
        url = reverse('routine_result')
        routine_result_data = {
            "routine_id": 1,
            "result": "DONE"
        }

        response = self.client.put(url, routine_result_data)
        routine_result = RoutineResultModel.objects.get(routine=routine_result_data["routine_id"])

        self.assertEqual(response.status_code, 200)
        self.assertEqual(routine_result.result, 'DONE')

    def test_anouther_user_update_my_routine_result_case(self):
        self.data = {'email': 'anotheruser@anotheruser.com', 'password': 'test1234!!'}
        self.user = UserModel.objects.create_user(**self.data)
        self.client.force_login(self.user)

        url = reverse('routine_result')
        routine_result_data = {
            "routine_id": 1,
            "result": "DONE"
        }

        response = self.client.put(url, routine_result_data)
        
        self.assertEqual(response.status_code, 403)
