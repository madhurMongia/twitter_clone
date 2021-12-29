from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import BasePermission,SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics
from django.db.models import Q
from . import serializers

class TweetPagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'tweets'

class CustomPerm(BasePermission):
    def has_object_permission(self,request,view,tweet):
        user_tweets = request.user.tweets.all()
        return user_tweets.contains(tweet) or request.method in SAFE_METHODS

class TweetView(ModelViewSet):
    lookup_url_kwarg = 'tweet_id'
    permission_classes = [IsAuthenticated,CustomPerm]
    serializer_class =  serializers.TweetSerializer
    pagination_class = TweetPagination
    queryset = serializers.Tweet.objects.all()

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)
    def list(self,request):
        print(request.method)
        queryset = self.get_queryset().filter(Q(user=request.user))
        page = self.paginate_queryset(queryset)
        return self.get_paginated_response(self.get_serializer(page,many=True).data)

    @action(detail=True, methods=['post'])
    def toggle_like(self,request ,tweet_id):
        action = request.data.get('action')
        tweet = get_object_or_404(serializers.Tweet, id = tweet_id)
        tweet.likes.add(request.user) if action == 'like' else tweet.likes.remove(request.user)
        return Response({'message' : f'{action}d'},status =200)
    @action (detail=True,methods=['post'])
    def retweet(self,request,tweet_id):
        tweet = get_object_or_404(serializers.Tweet, id = tweet_id)
        data = {
            'parent' : tweet.id,
            'content' : request.data.get('content')
            }
        retweet = serializers.TweetSerializer(data = data)
        if retweet.is_valid():
            retweet.save(user=request.user)
            return Response(retweet.data ,status =200)
        return Response(retweet.errors ,status =400)

""" 
class ActionView(APIView):

    def post(self,request):
        action = request.data.get('action')
        if action == 'l  ike' or 'unlike':
            return self.toggle_like(request)
        elif action == 'retweet':
            return self.retweet(request)
        return Response({'error' : 'Invalid tweet action'},status = 400) """


class tweet_feed(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = TweetPagination               

    def list(self,request):
        following = request.user.following.values_list('id',flat = True) 
        feed_tweets = serializers.Tweet.objects.filter(Q(user_id__in = following) | Q(user_id=request.user.id) | Q(parent__user_id =request.user.id)).order_by('updated_at')
        page = self.paginate_queryset(feed_tweets)
        return self.get_paginated_response(serializers.TweetSerializer(page,many=True).data)