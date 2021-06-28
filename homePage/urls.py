from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import HomePage

app_name= "homePage"

urlpatterns = [
    path('', login_required(HomePage.as_view()), name= "home"),
]
