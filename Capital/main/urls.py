from django.urls import path
from .import views

urlpatterns = [
    path('signup/',views.SignUp.as_view(),name='signup'),
    path('about/',views.About.as_view(),name='about'),
    path('history/',views.History.as_view(),name='history'),
    path('team/',views.Ourteam.as_view(),name='team'),
    #path('profile/',login_required(views.Profile.as_view()),name='profile'),
] 