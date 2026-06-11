from rest_framework import serializers
from .models import Parent, StudentProfile
from accounts.serializers import UserSerializer


class ParentSerializer(serializers.ModelSerializer):
    """Serializer đơn giản cho Phụ huynh — trả về tất cả trường."""
    class Meta:
        model = Parent
        fields = "__all__"


class StudentProfileSerializer(serializers.ModelSerializer):
    """
    Serializer dùng để đọc thông tin sinh viên đầy đủ.
    - `user` trả về object đầy đủ thay vì chỉ ID.
    - `parent_detail` là nested read để frontend hiển thị thông tin phụ huynh không cần gọi thêm API.
    - `full_name` là trường tổng hợp từ `user.get_full_name()`.
    """
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
        """
        Chức năng: Lấy tên đầy đủ của sinh viên.
        Output: (str) Họ và tên đầy đủ từ User model.
        """
        return obj.user.get_full_name()


class StudentCreateSerializer(serializers.ModelSerializer):
    """
    Serializer để tạo sinh viên mới kèm theo tạo tài khoản User.
    Business logic:
    - Tách các trường của User (first_name, last_name, email, password) thành write_only
      để nhận qua cùng 1 request, sau đó tự động tạo User và StudentProfile trong method create().
    - Username tự động lấy từ MSSV để đảm bảo tính nhất quán (sinh viên login bằng MSSV).
    """
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
        """
        Chức năng: Tạo User và StudentProfile trong một transaction.
        Input: validated_data - dict đã được validate chứa thông tin user + profile.
        Output: (StudentProfile) Profile vừa được tạo.
        Lưu ý: Import User ở đây (lazy import) để tránh circular import giữa accounts và students.
        """
        from accounts.models import User
        first_name = validated_data.pop("first_name")
        last_name = validated_data.pop("last_name")
        email = validated_data.pop("email")
        password = validated_data.pop("password")

        # Dùng MSSV làm username để sinh viên đăng nhập bằng mã số của mình
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
