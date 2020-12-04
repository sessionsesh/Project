from django.urls import path
from schedule import views as sviews
from . import views

app_name = 'schedule'
urlpatterns = [
   path('freetime', sviews.add_free_time, name="add_free_time"),
   path('calendar', sviews.calendar_view, name="calendar_view"),
]
