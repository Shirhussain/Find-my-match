from django.urls import path
from . import views 

app_name = 'likes'
urlpatterns = [
    path('user/<int:id>/', views.user_like, name='like_user'),
]

