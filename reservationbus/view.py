from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import exception_handler
from django.db import IntegrityError
from rest_framework.exceptions import AuthenticationFailed

from .models import User
from .serializer import RegisterSerializer

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated  

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"message": "تم انشاء الاكونت"}, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response({"error": "البريد الإلكتروني مستخدم بالفعل"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": "البريد الإلكتروني مستخدم بالفعل"}, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        try:
            data = super().validate(attrs)
            data['message'] = 'تم تسجيل الدخول بنجاح'
            return data
        except AuthenticationFailed:
            raise AuthenticationFailed("البريد الإلكتروني أو كلمة المرور غير صحيحة")


class CustomLoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [AllowAny]


#no of users


class UserCountView(APIView):
    permission_classes = [IsAuthenticated]  

    def get(self, request):
        user_count = User.objects.count()
        return Response({"total_users": user_count})
