from django.shortcuts import render
from django.http import HttpResponse

from slapmaster.models import Post, Response

def post(request):
    return HttpResponse("lalala")

def allposts(request):
    all_posts = Post.objects.all()
    context = { 'all_posts': all_posts }
    return render(request, 'slapmaster/allposts.html', context)
