from django.contrib import admin
from django.urls import path
from auth.views import login, reg

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/reg/',reg)
]
