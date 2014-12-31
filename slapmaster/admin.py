from django.contrib import admin

from slapmaster.models import Post, Response, PostVote

admin.site.register(Post)
admin.site.register(Response)
admin.site.register(PostVote)
