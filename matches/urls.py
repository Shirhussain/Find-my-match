from django.urls import path
from . import views 

app_name = 'matches'
urlpatterns = [
    path('position/<slug:slug>/', views.position_match_view_url, name='PositionMatch_detail'),
    path('location/<slug:slug>/', views.location_match_view_url, name='LocationMatch_detail'),
    path('employer/<slug:slug>/', views.employer_match_view_url, name='EmployerMatch_detail'),
]

