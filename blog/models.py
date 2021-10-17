from django.db import models

class User(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=127)
    last_name = models.CharField(max_length=127)
    user_name = models.CharField(max_length=100, unique=True)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    token = models.CharField(max_length=120, null=True)
    image = models.CharField(max_length=255, null=True)

class Followers(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    status = models.CharField(max_length=20, null=True)

class Posts(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    info = models.TextField(null=True)
    views = models.IntegerField(default=0)

class Photos(models.Model):
    id = models.AutoField(primary_key=True)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    photo = models.CharField(max_length=255)

class Comments(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    comment = models.TextField()