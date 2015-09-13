from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from . import views

urlpatterns = [
    url(r'^sendQuestion', csrf_exempt(views.sendQuestion), name='sendQuestion'),
    url(r'^test', csrf_exempt(views.test), name='test'),
]

