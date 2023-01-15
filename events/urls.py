from django.urls import path
from .views import AllEventsView, EventTypeView

urlpatterns = [
    path('', AllEventsView.as_view(), name="events"),
    path('<slug:reference_name>/', EventTypeView.as_view(), name="event"),
    # path('<slug:slug>/', EventView.as_view(), name="event"),
]
