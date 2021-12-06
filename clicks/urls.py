from .import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . views import *

# Application Views

urlpatterns = [
    path('', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('signup/', views.user_signup, name='signup'),
    path('profile/',views.profile, name='profile'),
    path('homepage/',views.homepage, name='homepage'),
]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
