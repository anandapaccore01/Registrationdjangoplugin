"""
URL configuration for signupandlogin1 project.

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
from django.urls import path,include
from signup_login import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homeview, name= 'homepage'),
    path('register', views.Registerview, name= 'register'),
    path('captcha/', include('captcha.urls')),
    path('emailactivate/<token>',views.emailactivate, name='emailactivate'),
    path('login', views.loginview, name= 'login'),
    path('profile/<int:id>', views.Profileview, name='profile'),
    path('logout', views.logoutview, name='logout'),
    path('changeemail', views.changeemail, name='changeemail'),
    path('resetpasswordview', views.resetpasswordView, name='resetpasswordview'),
    path('resetpassword', views.resetpassword, name='resetpassword'),
    path('sendotp',views.send_otp, name='send_otp'),
    path('verify_otp',views.verify_otp, name='verify_otp'),
    path('<path:path>',views.handle_not_found),
]
