from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import newUser
from django.conf import settings
from django.utils import timezone
from rest_framework.authtoken.models import Token
from .seralizers import UserSerializer,newTokenSerializer
class RegistionView(APIView):

    def post(self, request):
        serilizer = UserSerializer(data= request.data)
        if serilizer.is_valid():
            account = serilizer.save()
            user_name = serilizer.validated_data['user_name']
            token = Token.objects.create(user = account)
            return Response({'msg': "user with username " + user_name + " created " , 'key' : token.key}, status=status.HTTP_201_CREATED)
        return Response(serilizer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):

    def post(self,request):
        serializer = newTokenSerializer(data = request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']
            token = get_object_or_404(
                Token, user=serializer.validated_data['user'])
            user.last_login = timezone.now()
            user.save()
            return Response({'key' : token.key},status = status.HTTP_200_OK)
        return Response(serializer.errors,status =status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profile(request):
        profile = get_object_or_404(newUser,user_name = request.query_params.get('profile'))
        return Response(UserSerializer(profile, isPass2 = False).data)


class ActionView(APIView):
    def get(self,request):
        if request.query_params.get('action') == 'follow':
            return self.follow(request)
        elif request.query_params.get('action') == 'unfollow':
            return self.unfollow(request)
        else:
            return Response({'msg':'invalid action'},status = status.HTTP_400_BAD_REQUEST)

    def follow(self,request):
        follower =  request.user
        followee = get_object_or_404(newUser,user_name = request.query_params.get('followee'))
        
        followee.followers.add(follower)
        return Response({'msg':'followed'},status = status.HTTP_200_OK)

    def unfollow(self,request):
        follower = request.user
        followee = get_object_or_404(newUser,pk = request.query_params.get('followee'))
        followee.followers.remove(follower)
        return Response({'msg':'unfollowed'},status = status.HTTP_200_OK)

