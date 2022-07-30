from django.utils import timezone
from routine.models import RoutineDay as RoutineDayModel


def convert_today_to_datetime_and_day_of_week(today):
    y, m, d = map(int, today.split("-"))
    days_of_week = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]

    this_day_of_week = days_of_week[timezone.datetime(y, m, d).weekday()]
    today_datetime = timezone.make_aware(timezone.datetime(y, m, d))

    return this_day_of_week, today_datetime

def routine_queryset_for_this_date(request):
    today = request.data['today']
    this_day_of_week, today_datetime = convert_today_to_datetime_and_day_of_week(today)

    day_set = RoutineDayModel.objects.filter(
            created_at__gte=today_datetime - timezone.timedelta(days=6),
            created_at__lt=today_datetime + timezone.timedelta(days=1),
            day=this_day_of_week
            )
    day_set = list(day_set)
    day_object_list = [day.routine for day in day_set if day.routine.account.id == request.data['account_id']]

    return day_object_list