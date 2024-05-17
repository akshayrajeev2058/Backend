from django.contrib.auth import authenticate
from django.shortcuts import render
from .models import *
from .serializer import (
    Usersignuperializer,
    Loginseralizer,
    Leavemangementserializer,
    Leaveserializer,Alluserserializer
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from django.core.mail import send_mail
from django.conf import settings




class Sgnupuser(APIView):
    def post(self, request):
        try:
            serializer = Usersignuperializer(data=request.data)
            if serializer.is_valid():
                print(serializer.data, ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

                user_data = serializer.validated_data
                user = UserManagement.objects.create(
                    email=user_data.get("email"),
                    username=user_data.get("username"),
                )

                user.set_password(user_data.get("password"))
                user.save()

                return Response(
                    {"messages": "Account created successfully."},
                    status=status.HTTP_201_CREATED,
                )
            else:
                print(serializer.errors)
        except Exception as e:
            print(e)
            return Response(
                {"messages": "error."}, status=status.HTTP_501_NOT_IMPLEMENTED
            )


class Userlogin(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = Loginseralizer(data=data)
            if serializer.is_valid():
                print(serializer.data)
                email = serializer.data.get("email")
                password = serializer.data.get("password")

                user = authenticate(email=email, password=password)
                if user is not None:
                    return Response(
                        {
                            "message": "Login successful.",
                            "user_id": user.id,
                        },
                        status=status.HTTP_200_OK,
                    )
                else:
                    return Response(
                        {"message": "Invalid email or password."},
                        status=status.HTTP_401_UNAUTHORIZED,
                    )
            else:
                # Serializer is not valid
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response(
                {"message": "An error occurred."},
                status=status.HTTP_501_NOT_IMPLEMENTED,
            )
class Leavemanagent(APIView):
    def post(self, request, *args, **kwargs):
        try:
            id = kwargs.get("id")
            user = UserManagement.objects.get(id=id)
            serializer = Leavemangementserializer(data=request.data, partial=True)
            if serializer.is_valid():
                validated_data = serializer.validated_data
                leave_obj = Leavemanagement.objects.create(
                    user=user,
                    reason=validated_data.get("reason"),
                    startdate=validated_data.get("startdate"),
                    enddate=validated_data.get("enddate"),
                )
                
                # Send email notification to admin
                admin_email = settings.ADMIN_EMAIL  
                subject = "Leave Application Received"
                message = f"Leave application received from {user.email}. Please review and take action."
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [admin_email])
                
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except UserManagement.DoesNotExist:
            return Response(
                {"message": "User not found."}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            print(e)
            return Response(
                {"message": "An error occurred."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


            

class Alllist(ListCreateAPIView):
    queryset = Leavemanagement.objects.all()
    print(queryset, "*****************")
    serializer_class = Leavemangementserializer


class SuperuserLoginView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(email=email, password=password)

        if user is None:
            return Response(
                {"error": "Invalid email or password"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not user.is_superuser:
            return Response(
                {"error": "Only superusers are allowed to log in"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response({"message": "Login successful"}, status=status.HTTP_200_OK)


class Alluser(ListCreateAPIView):
    queryset=UserManagement.objects.all()
    serializer_class=Alluserserializer


class UpdateStatus(APIView):
    def patch(self, request):
        try:
            data = request.data
            leave_id = data.get('id')
            new_choice = data.get('choice')
            
            leave = Leavemanagement.objects.get(id=leave_id)
            leave.choice = new_choice
            leave.save()
            
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
