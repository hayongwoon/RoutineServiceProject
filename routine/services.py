from django.utils import timezone
from routine.models import RoutineDay as RoutineDayModel


def convert_today_to_datetime_and_day_of_week(today):
    year, month, day = map(int, today.split("-"))
    days_of_week = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]

    this_day_of_week = days_of_week[timezone.datetime(year, month, day).weekday()]
    today_datetime = timezone.make_aware(timezone.datetime(year, month, day))

    return this_day_of_week, today_datetime


def routine_queryset_for_this_date(request):
    today = request.GET.get('today', None)
    account_id = request.GET.get('account_id', None)

    this_day_of_week, today_datetime = convert_today_to_datetime_and_day_of_week(today)

    days_queryset = RoutineDayModel.objects.filter(
            created_at__gte=today_datetime - timezone.timedelta(days=6),
            created_at__lt=today_datetime + timezone.timedelta(days=1),
            day=this_day_of_week
            )

    days_queryset_list = list(days_queryset)
    day_object_list = [day.routine for day in days_queryset_list if day.routine.account.id == int(account_id)]
    
    return day_object_list