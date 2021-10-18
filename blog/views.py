from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from blog.models import Photos, Posts, Followers, Comments, User


@api_view(['POST'])
def createPost(request):
    user = checkToken(request.COOKIES.get('token'))
    if user:
        data = request.data
        p = Posts(title = data['title'], info = data['info'], user = user)
        p.save()
        for photo in data['photos']:
            Photos(post = p, photo = photo).save()
        return Response({"status": 'success', "massage": ''})
    else:
        return Response({"status": 'error', "massage": 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['DELETE'])
def deletePost(request):
    user = checkToken(request.COOKIES.get('token'))
    if user:
        try:
            p = Posts.objects.filter(id=request.GET['id']).delete()
            return Response({"status": 'success', "massage": 'succesful deleted'})
        except:
            return Response({"status": "error", "massage": "bad request"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"status": 'error', "massage": 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['get'])
def addFollower(request):
    user = checkToken(request.COOKIES.get('token'))
    if user:
        try:
            Followers(user = user, follower_id = request.GET['id'], status = 'active').save()
            return Response({"status": 'success', "massage": 'following'})
        except:
            return Response({"status": "error", "massage": "bad request"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"status": 'error', "massage": 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['DELETE'])
def deleteFollower(request):
    user = checkToken(request.COOKIES.get('token'))
    if user:
        try:
            Followers.objects.filter(user=user, follower = request.GET['id']).delete()
            return Response({"status": 'success', "massage": 'unfollowing'})
        except:
            return Response({"status": "error", "massage": "bad request"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"status": 'error', "massage": 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def addComment(request):
    user = checkToken(request.COOKIES.get('token'))
    if user:
        try:
            Comments(user = user, post_id = request.data['post_id'], comment = request.data['comment']).save()
            return Response({"status": 'success', "massage": 'added'})
        except:
            return Response({"status": "error", "massage": "bad request"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"status": 'error', "massage": 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def getComments(request):
    user = checkToken(request.COOKIES.get('token'))
    if user:
        try:
            comments = Comments.objects.filter(user = user, post_id = request.GET['post_id']).values()
            newComments = []
            for c in comments:
                u = User.objects.get(id = c["user_id"])
                newComments.append({
                    "comment": c['comment'],
                    "user_id": c["user_id"],
                    "user_name": u.user_name
                })
            return Response({"status": 'success', "commets": newComments})
        except:
            return Response({"status": "error", "massage": "bad request"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"status": 'error', "massage": 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def getPosts(request):
    user = checkToken(request.COOKIES.get('token'))
    if user:
        try:
            posts = Posts.objects.filter(user_id = request.GET['user_id']).values()
            return Response({"status": 'success', "posts": posts})
        except:
            return Response({"status": "error", "massage": "bad request"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"status": 'error', "massage": 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def view(request):
    user = checkToken(request.COOKIES.get('token'))
    if user:
        try:
            post = Posts.objects.get(user_id = user, id = request.GET['post_id'])
            post.views = post.views + 1
            post.save()
            return Response({"status": 'success', "massage": ""})
        except:
            return Response({"status": "error", "massage": "bad request"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"status": 'error', "massage": 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def getUser(request):
    user = checkToken(request.COOKIES.get('token'))
    if user:
        try:
            user = User.objects.get(id = request.GET['user_id'])
            u = {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "user_name": user.user_name,
                "email": user.email,
                "image": user.image
            }
            return Response({"status": 'success', "user": u})
        except:
            u = {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "user_name": user.user_name,
                "email": user.email,
                "image": user.image
            }
            return Response({"status": 'success', "user": u})
    else:
        return Response({"status": 'error', "massage": 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def getFolloers(request):
    user = checkToken(request.COOKIES.get('token'))
    if user:
        try:
            followers = Followers.objects.filter(user_id = request.GET['user_id']).select_related()
            f = []
            for follower in followers:
                f.append({
                    "id": follower.id,
                    "first_name": follower.follower.first_name,
                    "last_name": follower.follower.last_name,
                    "user_name": follower.follower.user_name,
                    "email": follower.follower.email,
                    "image": follower.follower.image
                })
            return Response({"status": "success", "followers": f})
        except User.DoesNotExist:
            return Response({"status": "error", "massage": ""})
    else:
        return Response({"status": 'error', "massage": 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def getFollowing(request):
    user = checkToken(request.COOKIES.get('token'))
    if user:
        try:
            followers = Followers.objects.filter(follower_id = request.GET['user_id']).select_related()
            f = []
            for follower in followers:
                f.append({
                    "id": follower.id,
                    "first_name": follower.user.first_name,
                    "last_name": follower.user.last_name,
                    "user_name": follower.user.user_name,
                    "email": follower.user.email,
                    "image": follower.user.image
                })
            return Response({"status": "success", "followers": f})
        except User.DoesNotExist:
            return Response({"status": "error", "massage": ""})
    else:
        return Response({"status": 'error', "massage": 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)


def checkToken(token):
    try:
        user = User.objects.get(token=token)
        return user
    except User.DoesNotExist:
        return False