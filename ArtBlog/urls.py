from django.contrib import admin
from django.urls import path, include
from auth.views import login, reg, checker

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/blog/', include('blog.urls', namespace='blog')),
    path('api/reg/',reg),
    path('api/login/',login),
    path('api/checkusername/',checker)
]
