from django.conf.urls import url
from blog import views

app_name = 'blog'

urlpatterns = [
    url(r'^createpost', views.createPost),
    url(r'^getuser', views.getUser),
    url(r'^deletepost', views.deletePost),
    url(r'^follow/', views.addFollower),
    url(r'^unfollow', views.deleteFollower),
    url(r'^comment/', views.addComment),
    url(r'^comments', views.getComments),
    url(r'^posts', views.getPosts),
    url(r'^view', views.view),
    url(r'^followers', views.getFolloers),
    url(r'^following', views.getFollowing),
]