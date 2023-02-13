from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

app_name = 'account'


urlpatterns = [
    path('signup', views.signup, name='signup'),
    path('validate-username', csrf_exempt(views.validate_username), name='validate-username'),
    path('validate-email', csrf_exempt(views.validate_email), name='validate-email'),
    path('activate/<uid64>/<token>/', views.activate, name='activate'),
    path('login', views.signin, name='signin'),
]