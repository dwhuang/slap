from django.db import models

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    news_url = models.URLField(max_length=1024)
    reason = models.CharField(max_length=1024)
    vote = models.PositiveIntegerField(default=0)
    views = models.PositiveIntegerField(default=0)
    time = models.DateTimeField(auto_now_add=True)
    
class Response(models.Model):
    id = models.AutoField(primary_key=True)
    original_post = models.ForeignKey('Post')
    response_text = models.TextField()
    upvote = models.PositiveIntegerField(default=0)
    downvote = models.PositiveIntegerField(default=0)
    time = models.DateTimeField(auto_now_add=True)

