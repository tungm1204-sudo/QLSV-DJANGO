from rest_framework import serializers
from .models import Parent, StudentProfile
from accounts.serializers import UserSerializer


class ParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parent
        fields = "__all__"


class StudentProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    parent_detail = ParentSerializer(source="parent", read_only=True)
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = StudentProfile
        fields = [
            "id", "user", "mssv", "full_name", "dob", "gender",
            "address", "parent", "parent_detail", "date_of_join", "status",
        ]

    def get_full_name(self, obj):
        return obj.user.get_full_name()


class StudentCreateSerializer(serializers.ModelSerializer):
    """Serializer để tạo sinh viên mới (kèm tạo User)."""
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = StudentProfile
        fields = [
            "first_name", "last_name", "email", "password",
            "mssv", "dob", "gender", "address", "parent", "status",
        ]

    def create(self, validated_data):
        from accounts.models import User
        first_name = validated_data.pop("first_name")
        last_name = validated_data.pop("last_name")
        email = validated_data.pop("email")
        password = validated_data.pop("password")

        user = User.objects.create_user(
            username=validated_data["mssv"],
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            role=User.Role.STUDENT,
        )
        profile = StudentProfile.objects.create(user=user, **validated_data)
        return profile
