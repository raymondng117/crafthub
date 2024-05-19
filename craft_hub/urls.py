"""
URL configuration for craft_hub project.

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
from django.contrib import admin
    #In the root app's urls.py (craft_hub), the root URL is configured to include the URL patterns from the user app using an empty path ''.
from django.urls import include, path

urlpatterns = [
    path('', include('index.urls')),

    # The user app's URLs are included with the prefix 'user/', so all URLs defined in the user app's urls.py will be accessible under this prefix (domain/user/).
    path('user/', include('user.urls')),
    path('products/', include('core.urls')),
    path('admin/', admin.site.urls),
]
