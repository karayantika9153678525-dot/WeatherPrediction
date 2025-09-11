<<<<<<< HEAD
"""
URL configuration for weatherpredict project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path
from weatherpredict.views import home, about, contact, predict_api

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name="home"),
    path('home/', home, name="home"),
    path('about/', about, name="about"),
    path('contact/', contact, name="contact"),
    path('predict/', predict_api, name="predict_api"),
]


 
=======
"""
URL configuration for weatherpredict project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path
from .views import home, about, contact, predict_api

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name="home"),              # Home page at root URL
    path('home/', home, name="home"),         # Home page (optional, for /home/)
    path('about/', about, name="about"),      # About page
    path('contact/', contact, name="contact"),# Contact page
    path('predict/', predict_api, name="predict_api"),  # ✅ API endpoint
]

 
>>>>>>> 556c898955d2e86d6e2bb0b002c875bce26477a0
