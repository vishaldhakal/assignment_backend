from .serializers import*
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from .models import Agent
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
import re
from rest_framework import status
from rest_framework import generics


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)

            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {
                "token": token.key,
            }
        )


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_agent(request):
    idd = request.user.id
    usss = User.objects.get(id=idd)
    realtorr = Agent.objects.get(user=usss)
    realtorr_ser = AgentSerializer(realtorr)

    return Response(
        {
            "agent": realtorr_ser.data,
        }
    )


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def updateImageApi(request):
    if request.method == "POST":
        try:
            image = request.FILES["image_u"]
            if image != None:
                idd = request.user.id
                usss = User.objects.get(id=idd)
                realtorr = Agent.objects.get(user=usss)
                realtorr.image = image
                realtorr.save()
                realtorr_ser = AgentSerializer(realtorr)
            else:
                pass
        except:
            pass
        return Response({
            "agent": realtorr_ser.data,
        }, status=status.HTTP_200_OK)
    else:
        return Response("Method not allowed", status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def updateProfile(request):
    try:
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        realtor_ass = request.POST["agent_association"]
        idd = request.user.id
        usss = User.objects.get(id=idd)
        realtorr = Agent.objects.get(user=usss)
        usss.first_name = first_name
        usss.last_name = last_name
        usss.save()
        realtorr.agent_association = realtor_ass
        try:
            image = request.FILES["image_u"]
            if image != None:
                realtorr.image = image
        except:
            pass
        realtorr.save()
        realtorr_ser = AgentSerializer(realtorr)
        return Response({
            "agent": realtorr_ser.data,
        }, status=status.HTTP_200_OK)
    except:
        return Response({"status": "Invalid Response"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def register_agent(request):
    datas = JSONParser().parse(request)
    first = datas["first"]
    last = datas["last"]
    email = datas["email"]
    username = email.split('@')[0]
    password = datas["password"]
    password2 = datas["password2"]
    brokerage = datas["agent_association"]

    if not all([first, last, email, password, password2, brokerage]):
        return Response({"status": "Empty fields"}, status=status.HTTP_400_BAD_REQUEST)

    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return Response({"status": "Invalid email"}, status=status.HTTP_400_BAD_REQUEST)

    if password != password2:
        return Response({"status": "Passwords don't match"}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(email=email).exists():
        return Response({"status": "Email already exists"}, status=status.HTTP_409_CONFLICT)

    if User.objects.filter(username=username).exists():
        return Response({"status": "Username already exists"}, status=status.HTTP_409_CONFLICT)

    user = User.objects.create_user(
        username=username, password=password, email=email, first_name=first, last_name=last)
    realtor_profile = Agent.objects.create(
        user=user, agent_association=brokerage)
    realtor_profile.save()
    auth.login(request, user)
    return Response({"status": "Profile created successfully"}, status=status.HTTP_201_CREATED)
