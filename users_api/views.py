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
from django.http import Http404

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
    def check_if_user_exist_by_id(self, userID):
        """Check if user id is exist"""
        user = models.UserModel.objects.filter(id=userID).first()
        if user is None:
            return False
        return True
    
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
    
    def get_user_id(self,request):
        token = request.COOKIES.get('jwt')
        payload = jwt.decode(token, 'secret', algorithm=['HS256'])
        userID=payload['id']
        return userID

class LogoutView(APIView):
    """Logout user"""
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'successfully logged out from the system',
            'messageError':"false"
        }
        return response


class CreateMessageView(APIView):
    def update_message_read_flag(self,messageID):
        """Update message object"""
        try:
            models.MessageItem.objects.filter(id=messageID).update(recipient_of_the_message_read_it=True)
            #Return updated object 
            return models.MessageItem.objects.filter(id=messageID ).values()
        except:
            return None
        
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
        if LoginView.check_if_user_exist_by_id(self,request.data["recipient_id"]) is False:
            return Response({"message":"Recipient ID didnt exist","messageError":"true"})
        if LoginView.user_is_authenticated(self,request):
            if self.create_message(request):
                print("in if create_message")
                return Response({"message":"message created successfuly!","messageError":"false"})
        return Response({"message":"User is unauthenticated ","messageError":"true"})

class DeleteMessageView(APIView):
    def get_object(self, pk):
        """Get message object"""
        try:
            return models.MessageItem.objects.get(pk=pk)
        except models.MessageItem.DoesNotExist:
            raise Http404
    def delete(self, request, pk=None):
        """Delete message object"""
        print("delete")
        if LoginView.user_is_authenticated(self,request):
            userID=str(LoginView.get_user_id(self,request))
            messageID=request.data["id"]
            message = self.get_object(messageID)
            recipient_id=message.get_recipient_id()
            sender_id=message.get_sender_id()
            # delete message in case its belong to sender or recipient
            if userID==recipient_id or userID==sender_id:
                message.delete()
                return Response({"message":"deleted successfuly!","messageError":"false"})   
            return Response({"message":"You are not authorized to delete this message","messageError":"true"})   
        return Response({"message":"User is unauthenticated","messageError":"false"})   
  
  
class GetMessageFromSpecificUserView(APIView):
    def get_message_from_specific_user(self, request,userID):
            """Get the last unread message"""
            res={}
            received_messages = models.MessageItem.objects.filter(sender_id=request.data["sender_id"],recipient_of_the_message_read_it=False, recipient_id=userID ).values()
            for message in received_messages:
                print(message)
                if message["recipient_of_the_message_read_it"] == False:
                    flag=CreateMessageView.update_message_read_flag(self,message["id"])
                    if flag:
                        res={"message":message,"messageError":"false"}
                        return res
            res={"message":"There are no new messages from this user","messageError":"false"}
            return res
        
    def get(self, request):
        userID=LoginView.get_user_id(self,request)
        if LoginView.user_is_authenticated(self,request):
                ans=self.get_message_from_specific_user(request,userID)
                return Response(ans)
        return Response({"message":"User is unauthenticated ","messageError":"true"})

class GetAllMessagesFromSpecificUser(APIView):
    def get_all_messages_for_specific_user(self, request,userID):
        """Get all messages from specipic user"""
        sent_messages = models.MessageItem.objects.filter(sender_id=userID, recipient_id=request.data["sender_id"] ).values()
        received_messages = models.MessageItem.objects.filter(sender_id=request.data["sender_id"], recipient_id=userID ).values()
        # merge sender and recipient messages
        ans=received_messages| sent_messages
        # sort messages by date field
        ans.order_by('created_on')    
        # Update message read flag for received messages
        for message in received_messages:
            if message["recipient_of_the_message_read_it"] == False:
                CreateMessageView.update_message_read_flag(self,message["id"])
        return ans
        
    def get(self, request):
        userID=LoginView.get_user_id(self,request)
        if LoginView.user_is_authenticated(self,request):
            ans=self.get_all_messages_for_specific_user(request,userID)
            return Response({"message":ans,"messageError":"false"})
        return Response({"message":"User is unauthenticated ","messageError":"true"})

class GetAllUnreadMessagesFromSpecificUser(APIView):
    def get_all_unread_messages_for_specific_user(self, request,userID):
            """Get the last unread message"""
            res={}
            received_messages = models.MessageItem.objects.filter(sender_id=request.data["sender_id"],recipient_of_the_message_read_it=False, recipient_id=userID ).values()
            for message in received_messages:
                print(message)
                if message["recipient_of_the_message_read_it"] == False:
                    CreateMessageView.update_message_read_flag(self,message["id"])
            if received_messages:
                res= {"message": received_messages,"messageError":"false"}
                return res
            res={"message":"All messages were read","messageError":"false"}
            return res
        
    def get(self, request):
        userID=LoginView.get_user_id(self,request)
        if LoginView.user_is_authenticated(self,request):
            ans=self.get_all_unread_messages_for_specific_user(request,userID)
            return Response({"message":ans,"messageError":"false"})
        return Response({"message":"User is unauthenticated ","messageError":"true"})      
    
    
    
