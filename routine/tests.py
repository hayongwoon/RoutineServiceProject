import datetime
from django.urls import reverse
from django.test.client import encode_multipart, RequestFactory
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from routine_result.models import RoutineResult as RoutineResultModel

from user.models import User as UserModel
from routine.models import Routine as RoutineModel
from routine.models import RoutineDay as RoutineDayModel

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


### 조회 테스트 postman에서는 바디 안에 값을 넣어서 가능했지만, test code의 get의 경우 쿼리스트링으로 값을 전달해야한다.
### GET은 요청을 전송할 때 URL 주소 끝에 파라미터로 포함되어 전송되며, 이 부분을 쿼리 스트링(QueryString)
### 참고 블로그 : https://velog.io/@songyouhyun/Get%EA%B3%BC-Post%EC%9D%98-%EC%B0%A8%EC%9D%B4%EB%A5%BC-%EC%95%84%EC%8B%9C%EB%82%98%EC%9A%94

### 때문에 테스트 코드의 구조나 구성이 어떤 식으로 해야 맞는 건지 조사해보자.
### 만약 바디로 받는게 아니라면 view에서 id = request.dat 가 아닌, reqest.GET('key')로 구조 바꿔야한다.

# class ReadSingleRoutineAPIViewTestCase(APITestCase):
#     def setUp(self):
#         self.data = {'email': 'test@test.com', 'password': 'test1234!!'}
#         self.user = UserModel.objects.create_user(**self.data)
#         self.client.force_login(self.user)

#         url = reverse('routines')
#         routine_data = {
#             "title": "problem solving",
#             "category": "HOMEWORK",
#             "goal": "Increase your problem-solving skills",
#             "is_alarm": True,
#             "get_days_list": ["MON", "WED", "FRI"]
#         }

#         self.client.post(url, routine_data)

#     def test_single_routine_read_case(self):
#         url = 'http://127.0.0.1:8000/routines?routine_id=1'

#         response = self.client.get(url)

#         print(response.status_code)


# class ReadRoutineListAPIViewTestCase(APITestCase):
#     def setUp(self):
#         self.data = {'email': 'test@test.com', 'password': 'test1234!!'}
#         self.user = UserModel.objects.create_user(**self.data)
#         self.client.force_login(self.user)

#         url = reverse('routines')
#         for i in range(10):
#             routine_data = {
#                 "title": f"{i}problem solving",
#                 "category": "HOMEWORK",
#                 "goal": "Increase your problem-solving skills",
#                 "is_alarm": True,
#                 "get_days_list": ["MON", "WED", "FRI"]
#             }

#             self.client.post(url, routine_data)

#     def test_read_today_todo_list_in_creating_routine_day_case(self):
#         url = 'http://127.0.0.1:8000/routines/todo-list?account_id=1&today=2022-07-31'
#         # print(datetime.today().strftime("%Y-%m-%d")
#         routines = RoutineModel.objects.filter(account=1)
#         print(routines)
#         response = self.client.get(url, format='json')
#         print(response.data)

