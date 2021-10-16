from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.hashers import make_password, check_password

@api_view(['POST'])
def login(request):
    data = {"status": "ok"}
    return data

@api_view(['POST'])
def reg(request):
    data = {"status": "ok"}
    return Response(request.data)


