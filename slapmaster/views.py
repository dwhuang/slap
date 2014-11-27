import sys
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from authomatic import Authomatic
from authomatic.adapters import DjangoAdapter

from slapmaster.models import Post, Response
from slapmaster.config import AUTHOMATIC_CONFIG
authomatic = Authomatic(AUTHOMATIC_CONFIG, 'gadf48t7vhzv0-42djcajhdslapit')

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

def fb_login(request):
    response = HttpResponse()
    result = authomatic.login(DjangoAdapter(request, response), 'fb')
    if not result:
        response.write("cannot get login result")
        return response
    if result.error:
        response.write(result.error.message)
        return response
    if not result.user:
        response.write("login result does not contain user info")
        return response

    if not (result.user.name and result.user.id):
        result.user.update()
    request.session['credentials'] = result.user.credentials.serialize()
    request.session['username'] = result.user.name
    request.session['userid'] = result.user.id
    request.session['useremail'] = result.user.email
    return HttpResponseRedirect(reverse('post_list'))

def logout(request):
    request.session.pop("credentials", None)
    request.session.pop("username", None)
    request.session.pop("userid", None)
    request.session.pop("useremail", None)
    return HttpResponseRedirect(reverse('post_list'))

def validate_user_credentials(session):
    if not session.has_key('credentials'):
        return False
    credentials = authomatic.credentials(session['credentials'])
    if not credentials.valid:
        session.pop("credentials", None)
        session.pop("username", None)
        session.pop("userid", None)
        session.pop("useremail", None)
        return False
    if credentials.expire_soon(60 * 60 * 24): # expiring in a day
        credentials.refresh()
        session['credentials'] = credentials.serialize()
    return True

class IndexView(generic.ListView):
    model = Post
    context_object_name = 'post_list'
    template_name = 'slapmaster/post_list.html'

    def get_context_data(self, **kwargs):
        validate_user_credentials(self.request.session)
        context = super(IndexView, self).get_context_data(**kwargs)
        return context

class DetailView(generic.DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'slapmaster/post_detail.html'

    def get_context_data(self, **kwargs):
        validate_user_credentials(self.request.session)
        context = super(DetailView, self).get_context_data(**kwargs)
        # add this post's responses to the context
        context['response_list'] = context['post'].response_set.all()
        return context
