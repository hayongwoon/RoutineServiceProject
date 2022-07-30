from asyncore import write
from dataclasses import field
from wsgiref import validate
from rest_framework import serializers

from routine.models import Routine as RoutineModel
from routine.models import RoutineDay as RoutineDayModel
from user.models import User as UserModel
from routine_result.models import RoutineResult as RoutineResultModel


class AccountSerialzer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['email']


class RoutineSerialzer(serializers.ModelSerializer):
    account = AccountSerialzer()
    get_days_list = serializers.ListField(write_only=True)
    days = serializers.SerializerMethodField()
    result = serializers.SerializerMethodField()

    def get_days(self, obj):
        return [day["day"] for day in obj.routineday_set.all().values('day')]

    def get_result(self, obj):
        return obj.routineresult.result

    class Meta:
        model = RoutineModel
        fields = ['category', 'goal', 'account', 'result', 'title', 'days', 'is_alarm', 'get_days_list']


    def create(self, validated_data):
        get_days_list = validated_data.pop("get_days_list", [])

        routine = RoutineModel(**validated_data)
        routine.account = self.context["request"].user
        routine.save()

        for day in get_days_list:
            routin_day = RoutineDayModel(day=day, routine=routine)
            routin_day.save()
        
        routine_result = RoutineResultModel(result="NOT", routine=routine)
        routine_result.save()

        return routine

    def update(self, instance, validated_data):
        get_days_list = validated_data.pop("get_days_list", [])

        for k, v in validated_data.items():
            setattr(instance, k, v)
        instance.save()

        RoutineDayModel.objects.filter(routine=instance).delete()
        for day in get_days_list:
            routin_day = RoutineDayModel(day=day, routine=instance)
            routin_day.save()

        return instance


class GetTodayRoutineListSerializer(serializers.ModelSerializer):
    result = serializers.SerializerMethodField()

    def get_result(self, obj):
        return obj.routineresult.result

    class Meta:
        model = RoutineModel
        fields = ["goal", "account", "result", "title"]