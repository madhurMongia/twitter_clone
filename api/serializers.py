from rest_framework import serializers
from .models import Tweet
from accounts.seralizers import TweetUserSerializer
class TweetSerializer(serializers.ModelSerializer):

    user = TweetUserSerializer(required = False)
    class Meta:
        model = Tweet
        fields = '__all__'
        read_only_fields = ['created_at','updated_at']
        extra_kwargs = {
        'user' : { 'required' : False}
    }