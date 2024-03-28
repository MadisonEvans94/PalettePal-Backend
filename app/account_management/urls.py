from django.urls import path
from .views import login, signup, test_token

urlpatterns = [
    path('login/', login, name='login'),
    path('sign-up/', signup, name='signup'),
    path('test_token/', test_token, name='test_token'),
]
