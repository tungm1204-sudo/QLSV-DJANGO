from rest_framework import serializers
from accounts.serializers import UserSerializer
from .models import Department, TeacherProfile


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"


class TeacherProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    department_detail = DepartmentSerializer(source="department", read_only=True)
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = TeacherProfile
        fields = [
            "id", "user", "mgv", "full_name", "dob", "gender",
            "department", "department_detail", "degree", "specialization", "status",
        ]

    def get_full_name(self, obj):
        return obj.user.get_full_name()


class TeacherCreateSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = TeacherProfile
        fields = [
            "first_name", "last_name", "email", "password",
            "mgv", "dob", "gender", "department", "degree", "specialization", "status",
        ]

    def create(self, validated_data):
        from accounts.models import User
        first_name = validated_data.pop("first_name")
        last_name = validated_data.pop("last_name")
        email = validated_data.pop("email")
        password = validated_data.pop("password")

        user = User.objects.create_user(
            username=validated_data["mgv"],
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            role=User.Role.TEACHER,
        )
        return TeacherProfile.objects.create(user=user, **validated_data)
