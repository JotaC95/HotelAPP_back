from django.urls import path
from .views import MyAssignmentsView

urlpatterns = [
    path("cleaner/my-assignments/", MyAssignmentsView.as_view(), name="my-assignments"),
]