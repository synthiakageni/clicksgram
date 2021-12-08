from .import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . views import *

# Application Views

urlpatterns = [
    path('', views.user_login, name='login'),
    path('homepage/', views.homepage, name='homepage'),
    path('logout/', views.user_logout, name='logout'),
    path('signup/', views.user_signup, name='signup'),
    path('profile', profile, name='profile'),
    path('homepage', homepage, name='homepage'),
    path('search_images/',views.search_images, name='search_images'),
    path('like_image/',views.like_image, name='like_image'),
    path('upload/add/', views.save_image, name='save.image'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('picture/<int:id>/', views.image_comments, name='single_image'),
]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
