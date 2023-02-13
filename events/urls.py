from django.urls import path

from .views import (AllEventsView, DeleteTeamAPIView, EventTypeView,
                    RegisterEventAPIView, RemoveMemberAPIView,
                    TeamDetailsAPIView, UpdateTeamAPIView, EventScheduleView)

urlpatterns = [
    path('list/<slug:reference_name>/', EventTypeView.as_view(), name="event"),
    path('register/', RegisterEventAPIView.as_view()),
    path('update-team/', UpdateTeamAPIView.as_view()),
    path('update-team/remove-member/', RemoveMemberAPIView.as_view()),
    path('delete-team/', DeleteTeamAPIView.as_view()),
    path('team-details/', TeamDetailsAPIView.as_view()),
    path('list/', AllEventsView.as_view(), name="events"),
    path('schedule/', EventScheduleView.as_view(), name="schedule"),
]
