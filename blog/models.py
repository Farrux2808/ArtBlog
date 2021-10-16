from django.db import models

class User(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=127)
    last_name = models.CharField(max_length=127)
    user_name = models.CharField(max_length=100, unique=True)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    token = models.CharField(max_length=120, null=True)
    image = models.CharField(max_length=255)

class Followers(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    follower_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    status = models.CharField(max_length=20, null=True)

class Photos(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    info = models.TextField()

class Comments(models.Model):
    id = models.AutoField(primary_key=True)
    photos_id = models.ForeignKey(Photos, on_delete=models.CASCADE)
    comment = models.TextField()