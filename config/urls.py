from django.contrib import admin
from django.urls import path, include 
from django.conf import settings
from django.conf.urls.static import static


from news import views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('accounts/', include('registration.backends.default.urls')),
    path('questions/', include('questions.urls', namespace='questions')),
    path('profiles/', include('profiles.urls', namespace='profiles')),
]


if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)