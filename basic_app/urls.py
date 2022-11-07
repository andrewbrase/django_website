from django.urls import path, include
from basic_app import views

# template urls app name variable
app_name = 'basic_app'

urlpatterns=[ 
    path('Home/',views.home, name='home'),
    path('Register/',views.register, name='register'),
]