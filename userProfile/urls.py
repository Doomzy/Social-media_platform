from django.urls import path
from .views import *

app_name= 'userProfile'

urlpatterns = [
    path('<slug:user>', Profile.as_view(), name= "Profile"),
    path('friends/<slug:user>', FriendsCTRL.as_view(), name= "FriendsCTRL"),
]
