from django.urls import path
from . import views 

app_name = 'questions'
urlpatterns = [
    path('', views.home, name='home'),
    path('<int:id>/', views.single, name='single'),
]
