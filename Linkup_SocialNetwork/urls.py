from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', include('homePage.urls')),
    path('account/', include('accounts.urls')),
    path('u/', include('userProfile.urls')),
    path('posts/', include('posts.urls')),
    path('admin/', admin.site.urls),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
