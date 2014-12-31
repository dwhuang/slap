import sys
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.views import generic
from authomatic import Authomatic
from authomatic.adapters import DjangoAdapter

from slapmaster.models import Post, Response, User, PostVote
from slapmaster.user_session import UserSession

def addpost(request):
    try:
        news_url = request.POST['news_url']
        reason = request.POST['reason']
        p = Post(news_url=news_url, reason=reason)
        p.save()
        return HttpResponseRedirect(reverse('post_list'))
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

def fb_login(request):
    user_session = UserSession(request)
    return user_session.login()

def logout(request):
    user_session = UserSession(request)
    return user_session.logout()

class IndexView(generic.ListView):
    model = Post
    context_object_name = 'post_list'
    template_name = 'slapmaster/post_list.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['user_session'] = UserSession(self.request)
        return context

class DetailView(generic.DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'slapmaster/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context['user_session'] = UserSession(self.request)
        # add this post's responses to the context
        context['response_list'] = context['post'].response_set.all()
        return context

class UserPrefsView(generic.TemplateView):
    template_name = 'slapmaster/user_prefs.html'

    def dispatch(self, request, *args, **kwargs):
        self.user_session = UserSession(request)
        if not self.user_session.validate():
            return redirect('post_list')
        return super(UserPrefsView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UserPrefsView, self).get_context_data(**kwargs)
        context['user_session'] = self.user_session
        return context

def user_prefs_save(request):
    show_fb_url = True if request.POST.has_key('show_fb_url') else False
    nickname = request.POST['nickname']

    user_session = UserSession(request)
    user_session.show_fb_url = show_fb_url
    user_session.nickname = nickname
    return HttpResponseRedirect(reverse('post_list'))

def votepost(request, pk, vote):
    post = Post.objects.get(pk=pk)
    user = UserSession(request).user
    if not user:
        # user is not logged in
        return HttpResponseRedirect(reverse('post_list'))
    # check that the user has not already voted the post
    if user.voted_post.filter(id=pk).count() > 0:
        # user has already voted for this post
        return HttpResponseRedirect(reverse('post_list'))
    power = 0
    if vote == 'up':
        power = 1
        post.upvote += 1 
        post.save(update_fields=['upvote'])
    elif vote == 'down':
        power = -1
        post.downvote += 1
        post.save(update_fields=['downvote'])
    if power == 0:
        # neither voted up nor down 
        # (should not happen if urls.py is configured properly)
        raise Http404

    PostVote.objects.create(post=post, user=user, power=power)
    return HttpResponseRedirect(reverse('post_list'))

