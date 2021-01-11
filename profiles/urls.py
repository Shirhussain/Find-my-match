from django.urls import path
from . import views 

app_name = 'profiles'
urlpatterns = [
    path('<str:username>/', views.profile, name='profile'),
]

