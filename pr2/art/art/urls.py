"""
URL configuration for art project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from users import views as user_views
from gallery import views as gallery_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', gallery_views.general, name='general'),
    path('likes/', gallery_views.likes, name='likes'),
    path('korzina/', gallery_views.korzina, name='korzina'),
    path('contact/', gallery_views.contact, name='contact'),
    path('toggle-favorite/<int:artwork_id>/', gallery_views.toggle_favorite, name='toggle_favorite'),
    path('add-to-cart/<int:artwork_id>/', gallery_views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:cart_item_id>/', gallery_views.remove_from_cart, name='remove_from_cart'),
    path('', include('users.urls')),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)