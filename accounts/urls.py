from accounts.views import LoginAPI,RegisterAPI, UserAPI
from django.conf.urls import url

urlpatterns = [
    url("login/", LoginAPI.as_view()),
    url("register/", RegisterAPI.as_view()),
    url("user/", UserAPI.as_view())

]
