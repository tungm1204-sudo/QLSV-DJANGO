from rest_framework import serializers
from accounts.serializers import UserSerializer
from .models import Department, TeacherProfile


class DepartmentSerializer(serializers.ModelSerializer):
    """Serializer đơn giản cho Khoa / Bộ môn."""
    class Meta:
        model = Department
        fields = "__all__"


class TeacherProfileSerializer(serializers.ModelSerializer):
    """
    Serializer dùng để đọc thông tin giảng viên đầy đủ.
    - `user` trả về nested object để frontend có đủ thông tin cá nhân.
    - `department_detail` cung cấp tên/mã khoa thay vì chỉ trả về FK id.
    - `full_name` là trường tổng hợp tiện lợi cho UI hiển thị dropdown.
    """
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
        """
        Chức năng: Lấy tên đầy đủ của giảng viên.
        Output: (str) Họ và tên đầy đủ từ User model.
        """
        return obj.user.get_full_name()


class TeacherCreateSerializer(serializers.ModelSerializer):
    """
    Serializer để tạo giảng viên mới kèm tạo tài khoản User.
    Business logic:
    - Tương tự StudentCreateSerializer, tách các trường User thành write_only
      và tự động tạo User trong method create().
    - Username tự động lấy từ MGV để giảng viên login bằng mã số giảng viên của mình.
    """
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
        """
        Chức năng: Tạo User với role TEACHER và TeacherProfile trong cùng một transaction.
        Input: validated_data - dữ liệu đã validate.
        Output: (TeacherProfile) Profile vừa tạo.
        Lưu ý: Lazy import User để tránh circular import.
        """
        from accounts.models import User
        first_name = validated_data.pop("first_name")
        last_name = validated_data.pop("last_name")
        email = validated_data.pop("email")
        password = validated_data.pop("password")

        # MGV được dùng làm username để đồng nhất với hệ thống định danh nhân sự
        user = User.objects.create_user(
            username=validated_data["mgv"],
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            role=User.Role.TEACHER,
        )
        return TeacherProfile.objects.create(user=user, **validated_data)
