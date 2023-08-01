from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('profile_list/', views.profile_list, name='profile_list'),
    path('profile/<int:pk>', views.profile, name='profile'),
    path('profile/followers/<int:pk>', views.followers, name='followers'),
    path('profile/follows/<int:pk>', views.follows, name='follows'),
    path('login/', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('update_user/', views.update_user, name='update_user'),
    path('deet_like/<int:pk>', views.deet_like, name="deet_like"),
    path('deet_show/<int:pk>', views.deet_show, name="deet_show"),
    path('unfollow/<int:pk>', views.unfollow, name="unfollow"),
    path('follow/<int:pk>', views.follow, name="follow"),
    path('delete_deet/<int:pk>', views.delete_deet, name="delete_deet"),
    path('edit_deet/<int:pk>', views.edit_deet, name="edit_deet"),
    path('search/', views.search, name='search'),
    path('search_user/', views.search_user, name='search_user'),
    path('<int:pk>/password/', views.change_password, name='change_password'),
    # path('*/password/', views.change_password, name='change_password'),
]