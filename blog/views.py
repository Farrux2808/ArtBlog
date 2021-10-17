from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from blog.models import Photos, Posts, Followers, Comments, User


def public(request):
    return HttpResponse("You don't need to be authenticated to see this")


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

@api_view(['post'])
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
            comments = Comments.objects.filters(user = user, post_id = request.GET['post_id']).values()
            return Response({"status": 'success', "commets": comments})
        except:
            return Response({"status": "error", "massage": "bad request"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"status": 'error', "massage": 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

def checkToken(token):
    try:
        user = User.objects.get(token=token)
        return user
    except User.DoesNotExist:
        return False