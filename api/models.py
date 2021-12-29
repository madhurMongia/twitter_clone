from django.db import models
from django.conf import settings
from django.utils import timezone
User = settings.AUTH_USER_MODEL

class TweetLikes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet = models.ForeignKey('Tweet', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)

class Tweet(models.Model):
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User,related_name='tweets', on_delete=models.CASCADE)
    content = models.TextField(max_length=140)
    likes = models.ManyToManyField(User, blank=True, related_name='tweet_likes', through=TweetLikes)
    created_at = models.DateTimeField(blank = True)
    updated_at = models.DateTimeField(blank = True)

    def is_retweet(self):
        return self.parent != None
    def save(self ,*args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(Tweet,self).save(*args, **kwargs)

