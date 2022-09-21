from django.urls import path
from . import views

urlpatterns = [

    # Authentication
    path('login', views.loginPage, name='login'),
    path('logout', views.logoutUser, name='logout'),
    path('register', views.regiaterUser, name='register'),

    
    # Profile 
    path('', views.profiles, name='profiles'),
    path('profile/<str:pk>/', views.userProfile, name='user-profile'),

    # Account 
    path('account/', views.userAccount, name='account'),
    path('edit-account/', views.editAccount, name='edit-account'),

    # Skills
    path('add-skill', views.addSkills, name='add-skill'),
    path('edit-skill/<str:pk>/', views.editSkills, name='edit-skill'),
    path('delete-skill/<str:pk>/', views.deleteSkills, name='delete-skill'),

    # Message
    path('inbox/', views.inbox, name='inbox'),
    path('message/<str:pk>/', views.viewMessage, name='message'),
    path('send-message/<str:pk>/', views.sendMessage, name='send-message'),
]
