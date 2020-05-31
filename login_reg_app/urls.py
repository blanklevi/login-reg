from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    path('success', views.success),
    path('success/login', views.success_log_in),
    path('registration', views.registration),
    path('loggedin', views.log_in),
    path('logout', views.log_out),
    path('wall', views.success_log_in),
    path('post_message', views.wall_page),
    path('post_comment', views.comment),

]
