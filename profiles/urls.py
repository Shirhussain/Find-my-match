from django.urls import path
from . import views 

app_name = 'profiles'
urlpatterns = [
    path('<str:username>/', views.profile, name='profile'),
    path('jobs/add/', views.add_job, name="add_jobs"),
    path('jobs/update/', views.update_jobs, name="update_jobs"),
]

