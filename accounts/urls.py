from django.urls import path
from . import views

app_name= 'accounts'

urlpatterns = [
    path('login/', views.Login.as_view(), name= "login"),
    path('signup/', views.Signup.as_view(), name= "signup"),
    path('logout/', views.Logout.as_view(), name= "logout"),
    path('ajax-search/', views.UserSearch.as_view(), name= "userSearch"),
]
