from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from user.models import User as UserModel
import re


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ["email", "password", "username"]
        extra_kwargs = {
            'password':{'write_only':True},
        }

    def validate(self, attrs):
        password = attrs['password']
        if not re.match(r"^(?=.*[a-zA-Z])(?=.*\d)(?=.*[#@$!%*?&])[A-Za-z\d#@$!%*?&]{8,}", password):
                raise ValidationError('8자 이상 문자와 숫자 및 특수문자를 조합하시오.')
        return super().validate(attrs)

    def create(self, validated_data):
        user = UserModel.objects.create(
            email=validated_data['email'],
            username=validated_data['username'],
        )

        user.set_password(validated_data['password'])
        user.save()

        return user
