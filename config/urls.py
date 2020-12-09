"""HistMat URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include

from .settings import settings



from django.conf import settings

from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    path('admin_HistMat_zJ8pyWuQCm/', admin.site.urls),
    
]
urlpatterns += i18n_patterns(
    path('biblio/', include('apps.Biblio.urls', namespace='post')),
    path('user/', include('apps.Users.urls', namespace='users')),
    path('', include('apps.Layout.urls', namespace='layout')),
    path('', include('social_django.urls', namespace='social')),
    path('apuntes/', include('apps.Apuntes.urls', namespace='apuntes')),
    path('forum/', include('apps.Forum.urls', namespace='forum')),
    
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]