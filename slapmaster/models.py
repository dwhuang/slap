from django.db import models

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    news_url = models.URLField(max_length=1024)
    reason = models.CharField(max_length=1024)
    vote = models.PositiveIntegerField(default=0)
    views = models.PositiveIntegerField(default=0)
    time = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey('User')
    
class Response(models.Model):
    id = models.AutoField(primary_key=True)
    original_post = models.ForeignKey('Post')
    response_text = models.TextField()
    upvote = models.PositiveIntegerField(default=0)
    downvote = models.PositiveIntegerField(default=0)
    time = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey('User')

class User(models.Model):
    id = models.AutoField(primary_key=True)
    fb_id = models.CharField(max_length=32)
    show_fb_url = models.BooleanField(default=True)
    nickname = models.CharField(max_length=32)
    reputation = models.IntegerField(default=0)

    @property
    def fb_url(self):
        return "https://www.facebook.com/app_scoped_user_id/%s/" % self.fb_id

    @property
    def fb_pic_url(self):
        return "https://graph.facebook.com/%s/picture?type=square" % self.fb_id
