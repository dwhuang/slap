import sys
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

from slapmaster.models import Post, Response

def allposts(request):
    all_posts = Post.objects.all()
    context = { 'all_posts': all_posts }
    return render(request, 'slapmaster/allposts.html', context)

def post(request, post_id):
    post = Post.objects.get(id=post_id)
    response_list = Response.objects.filter(original_post=post_id)
    context = { 'post': post, 'response_list': response_list }
    return render(request, 'slapmaster/post.html', context)

def addpost(request):
    try:
        news_url = request.POST['news_url']
        reason = request.POST['reason']
        p = Post(news_url=news_url, reason=reason)
        p.save()
        return HttpResponseRedirect(reverse('allposts'))
    except:
        return HttpResponse(sys.exc_info()[0])

def addresponse(request):
    try:
        post_id = request.POST['post_id']
        response_text = request.POST['response_text']
        r = Post.objects.get(id=post_id).response_set.create(
                response_text=response_text)
        r.save()
        return HttpResponseRedirect(reverse('post', args=(post_id,)))
    except:
        return HttpResponse(sys.exc_info()[0])

