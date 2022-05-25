from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from users_api import serializers
from users_api import models
from rest_framework.authentication import TokenAuthentication
from users_api import permissions
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
import jwt, datetime
from django.core import serializers as serializersv2
from django.http import HttpResponse, Http404

class RegisterView(APIView):
    """Register new user"""
    def post(self, request):
        serializer = serializers.UsersSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class LoginView(APIView):
    """Login user"""
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        user = models.UserModel.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationFailed('User not found!')
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')
        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }
        token = jwt.encode(payload, 'secret', algorithm='HS256').decode('utf-8')
        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }
        return response

class LogoutView(APIView):
    """Logout user"""
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success',
            'messageError':"false"
        }
        return response
class MessageView(APIView):
    """Check if user is authenticated"""
    def user_is_authenticated(self,request):
        token = request.COOKIES.get('jwt')
        if not token:
            return False
        try:
            payload = jwt.decode(token, 'secret', algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            return False
        return True
    def get_object(self, pk):
        """Get message object"""
        try:
            return models.MessageItem.objects.get(pk=pk)
        except models.MessageItem.DoesNotExist:
            raise Http404

    def create_message(self,request):
        """Create message object"""
        try:
            token = request.COOKIES.get('jwt')
            payload = jwt.decode(token, 'secret', algorithm=['HS256'])
            messageDict=request.data
            messageDict["sender_id"]=payload['id']
            serializer = serializers.MessageItemSerializer(data=messageDict )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return True
        except models.MessageItem.DoesNotExist:
            return False

    def post(self, request):
        if self.user_is_authenticated(request):
            if self.create_message(request):
                print("in if create_message")
                return Response({"message":"message created successfuly!","messageError":"false"})
        return Response({"message":"User is unauthenticated ","messageError":"true"})

    def update_message_read_flag(self,request):
        """Update message object"""
        try:
            dataObj=request
            dataObj["recipient_of_the_message_read_it"]=True
            print(dataObj)
            message_serializer = serializers.MessageItemSerializer(  data=dataObj, partial=True)
            message_serializer.is_valid(raise_exception=True)
            message_serializer.save()
            return True
        except:
            return False
 
    def delete(self, request, pk=None):
        """Delete message object"""
        message = self.get_object(request.data["id"])
        message.delete()
        return Response({"message":"deleted successfuly!","messageError":"false"})

    def get_all_messages_for_specific_user(self, request):
            """Get all messages from specipic user"""
            token = request.COOKIES.get('jwt')
            payload = jwt.decode(token, 'secret', algorithm=['HS256'])
            sender_messages = models.MessageItem.objects.filter(sender_id=payload['id'], recipient_id=request.data["recipient_id"] ).values()
            recipient_messages = models.MessageItem.objects.filter(sender_id=request.data["recipient_id"], recipient_id=payload['id'] ).values()
            # merge sender and recipient messages
            ans=recipient_messages| sender_messages
            # sort messages by date field
            ans.order_by('created_on') 
            return ans
            
    def get_last_messages_for_specific_user(self, request):
            """Get last message from specipic user"""
            token = request.COOKIES.get('jwt')
            payload = jwt.decode(token, 'secret', algorithm=['HS256'])
            sender_messages = models.MessageItem.objects.filter(sender_id=payload['id'],recipient_of_the_message_read_it=False, recipient_id=request.data["recipient_id"] ).values()
            recipient_messages = models.MessageItem.objects.filter(sender_id=request.data["recipient_id"],recipient_of_the_message_read_it=False, recipient_id=payload['id'] ).values()
            # merge sender and recipient messages
            ans=recipient_messages| sender_messages
            # sort messages by date field
            for message in ans:
                if message["recipient_of_the_message_read_it"] is False:
                    print(message["recipient_of_the_message_read_it"])
                    print(self.update_message_read_flag(message))
                    return  message
            return ans

    def get(self, request):
        if self.user_is_authenticated(request):
            if(request.data["type"]=="GetAllMessagesForSpecificUser"):
                ans=self.get_all_messages_for_specific_user(request)
                return Response({"message":ans,"messageError":"false"})
            if(request.data["type"]=="GetLastMessagesForSpecificUser"):
                ans=self.get_last_messages_for_specific_user(request)
                return Response({"message":ans,"messageError":"false"})
        return Response({"message":"User is unauthenticated ","messageError":"true"})

