from django.urls import path
from apps.views import *

urlpatterns = [
    path('', login_view, name="login"),
    path('register', register_view, name="register"),
    path('home', home_view, name="home"),
    path('logout', logout_view, name="logout"),
    path('profile/', profile_view, name="profile"),
    path('todo/delete/<int:id>', delete_view, name="delete"),
    path('todo/edit/<int:id>', edit_view, name="edit"),
    path('user/setting/', setting_view, name="setting"),
]
