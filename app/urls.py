from django.contrib import admin
from django.conf.urls import url
from app import views as core_views
from django.urls import (
    path,
    include,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    url(r'^signup/$', core_views.signup, name='signup'),
    path('', include('bills.urls')),
]
