from django.urls import path

from .views import EventTypeView, EventView

urlpatterns = [
    path('', EventTypeView.as_view(), name="events"),
    path('<slug:slug>/', EventView.as_view(), name="event"),
]
