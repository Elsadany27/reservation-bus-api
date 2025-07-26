from django.urls import path
from reservationbus.view import (
    RegisterView, CustomLoginView, UserCountView,
    TripListCreateView, TripDetailView,
    TicketCreateView,
    ReserveTicketCreateView, UserReserveTicketsView,AvailableSeatsView,AllReservedTicketsView,FilterAllReservedTicketsView
)

urlpatterns = [

    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('user-count/', UserCountView.as_view(), name='user-count'),

    path('trips/', TripListCreateView.as_view(), name='trip-list-create'),
    path('trips/<int:pk>/', TripDetailView.as_view(), name='trip-detail'),

    path('tickets/', TicketCreateView.as_view(), name='ticket-create'),

    path('reserve-ticket/', ReserveTicketCreateView.as_view(), name='reserve-ticket'),
    path('my-tickets/', UserReserveTicketsView.as_view(), name='my-reserve-tickets'),
    # New endpoint for checking available seats on a trip
    path('trips/<int:trip_id>/available-seats/', AvailableSeatsView.as_view(), name='available-seats'),

    path('reserved-tickets/all/', AllReservedTicketsView.as_view(), name='all-reserved-tickets'),
    path('reserved-tickets/filter/', FilterAllReservedTicketsView.as_view(), name='filter-reserved-tickets'),

]
