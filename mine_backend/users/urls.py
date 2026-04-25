from django.urls import path
from users.views import LoginView, RegisterView,EditView

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('register/', RegisterView.as_view()),
    path('edit/<int:pk>/',EditView.as_view())
]
