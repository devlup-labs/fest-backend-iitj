from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from rest_framework import routers

router = routers.DefaultRouter()


urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('coreteam/', include('coreteam.urls')),
    path('sponsors/', include('sponsors.urls')),
    path('events/', include('events.urls')),
    re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns = [path('__debug__/', include('debug_toolbar.urls')),] + urlpatterns
