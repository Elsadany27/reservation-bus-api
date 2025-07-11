from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import User, Trip, Ticket, ReserveTicket
from .serializer import RegisterSerializer, TripSerializer, TicketSerializer, ReserveTicketSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.views import APIView
from django.db import IntegrityError
from rest_framework.exceptions import AuthenticationFailed
from django_filters.rest_framework import DjangoFilterBackend


# Registration View
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"message": "تم انشاء الحساب"}, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response({"error": "البريد الإلكتروني مستخدم بالفعل"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({"error": "حدث خطأ غير متوقع"}, status=status.HTTP_400_BAD_REQUEST)


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


class UserCountView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_count = User.objects.count()
        return Response({"total_users": user_count})


# Trip Views
class TripListCreateView(generics.ListCreateAPIView):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['from_area', 'to_area', 'date']


class TripDetailView(generics.RetrieveAPIView):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    permission_classes = [IsAuthenticated]


# Ticket
class TicketCreateView(generics.CreateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [AllowAny]


# ✅ Reserve Ticket (Create)
class ReserveTicketCreateView(generics.CreateAPIView):
    queryset = ReserveTicket.objects.all()
    serializer_class = ReserveTicketSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# ✅ Return All Tickets of Logged-in User
class UserReserveTicketsView(generics.ListAPIView):
    serializer_class = ReserveTicketSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ReserveTicket.objects.filter(user=self.request.user)
