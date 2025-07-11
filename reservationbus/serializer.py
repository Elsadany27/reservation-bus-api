from rest_framework import serializers
from .models import User,ReserveTicket

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)  # ✅ Important!


#trips
from rest_framework import serializers
from .models import Trip, Ticket
from rest_framework import serializers
from .models import Trip, Ticket, ReserveTicket

class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = '__all__'
        read_only_fields = ['trip_number']

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'

class ReserveTicketSerializer(serializers.ModelSerializer):
    trip = TripSerializer(read_only=True)
    trip_id = serializers.PrimaryKeyRelatedField(queryset=Trip.objects.all(), write_only=True, source='trip')

    class Meta:
        model = ReserveTicket
        fields = ['id', 'reserver_name', 'trip', 'trip_id', 'seat_numbers']
