from rest_framework import serializers
from .models import newUser
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken.serializers import AuthTokenSerializer

class FollowField(serializers.RelatedField):
    def to_representation(self, value):
        return  {
            'username' : value.user_name,
            'id' : value.id,
        }
class UserSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        isPass2 =kwargs.pop('isPass2',True)
        super(UserSerializer, self).__init__(*args, **kwargs)
        if not isPass2:
            self.fields.pop('password2')
        allowed = kwargs.pop('fields',None)
        if allowed:
            for field in self.fields:
                if field not in allowed:
                    self.fields.pop(field)
    password2 = serializers.CharField()
    followers = FollowField(many=True , read_only=True)
    following = FollowField(many=True , read_only=True)
    class Meta:
        model = newUser
        fields = ('email',
        'user_name',
        'password',
        'password2',
        'bio',
        'followers',
        'following',
        )
        extra_kwargs = {
            'password' : {'write_only': True , 'style' : {'input_type':'password'}}
        }
    def create(self,validation_data):
        password = validation_data.pop('password')
        user = self.Meta.model(**validation_data)
        user.set_password(password)
        user.save()
        return user

    def validate(self,data):
        password = data.get('password')
        password2 = data.pop('password2')
        if(password2 != password):
           raise serializers.ValidationError(_('passwords do not match'))
        return data
        

class newTokenSerializer(AuthTokenSerializer):
    username = None
    email = serializers.CharField( write_only = True)

    def validate(self,attrs):
        if attrs.get('email') and attrs.get('password'):
            user = authenticate(**attrs)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "email" and "password".')
            raise serializers.ValidationError(msg, code='authorization')
        attrs['user'] = user
        return attrs

class TweetUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = newUser
        fields = ('user_name', 'id')