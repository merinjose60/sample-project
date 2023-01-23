from django.urls import path
from .views import *
urlpatterns=[
path('email/',regis),
path('emailsend/',email_send),
path('emailregister/',reg),
path('verify/<auth_token>',verify),
path('login/',login)
]