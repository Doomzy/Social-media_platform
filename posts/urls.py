from posts.models import Post
from django.urls import path
from .views import *

app_name= 'Posts'

urlpatterns = [
    path('', PostView.as_view(), name= "post"),
    path('ajax-ctrls/', PostCtrlsView.as_view(), name= "postCtrls"),
]
