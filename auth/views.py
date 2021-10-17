from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.contrib.auth.hashers import make_password, check_password
from blog.models import User
import secrets, hashlib

@api_view(['POST'])
def login(request):
    data = request.data
    try:
        user = User.objects.get(user_name=data.get('user_name',''))
        if check_password(data.get('password',''), user.password):
            salt = secrets.token_hex(8) + data.get('user_name')
            token = hashlib.sha256(salt.encode('utf-8')).hexdigest()
            user.token = token
            user.save()
            response = Response({'token': token})
            response.set_cookie('token', token)
            return response
        else:
            return Response({
                "status": "error",
                "massage": 'Invalid username or password'}, 
                status=status.HTTP_401_UNAUTHORIZED)
    except User.DoesNotExist:
        return Response({
            "status": "error",
            "massage": 'Invalid username or password'}, 
            status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def reg(request):
    data = request.data
    if data.get('first_name',False) and data.get('last_name',False) and data.get('user_name',False) and data.get('email',False) and data.get('password',False):
        try:
            User(
                first_name = data['first_name'],
                last_name = data['last_name'],
                user_name = data['user_name'],
                password = make_password(data['password']),
                email = data['email'],
                image = data.get('image', None),
            ).save()
            return Response({"status": "success", "massage": ""})

        except:
            return Response({
                "status": "error",
                "massage": "data is repeated"
            }, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({
            "status": "error",
            "massage": "data is incomplete"
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def checker(request):
    user_name = request.data.get('user_name', '')
    try:
        user = User.objects.get(user_name = user_name)
        return Response({"status": True})
    except User.DoesNotExist:
        return Response({"status": False})