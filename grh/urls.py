"""
URL configuration for grh project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin # type: ignore
from django.urls import path, include # type: ignore
from django.conf import settings
from django.conf.urls.static import static
from notifications import notifications_views
from employer.views import index

urlpatterns = [
    path('', index, name='home'),
    path('admin/', admin.site.urls),
    path('employe/', include('employer.urls')),
    path('accounts/', include('accounts.urls')),
    path('inbox/notifications/', include('notifications.urls', namespace='notifications')),
    path('notifications/page/', notifications_views.notifications_page, name='notifications_page'),
    path('notifications/mark-as-read/<int:notification_id>/', notifications_views.mark_as_read, name='mark_as_read'),
    path('notifications/mark-all-as-read/', notifications_views.mark_all_as_read, name='mark_all_as_read'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
