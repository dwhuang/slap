import sys
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from authomatic import Authomatic
from authomatic.adapters import DjangoAdapter

from slapmaster.models import Post, Response, User
from slapmaster.config import AUTHOMATIC_CONFIG
authomatic = Authomatic(AUTHOMATIC_CONFIG, 'gadf48t7vhzv0-42djcajhdslapit')

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
    u = get_or_create_user(result.user.id, result.user.name)
    user = {'name': result.user.name, 
            'fb_id': result.user.id,
            'email': result.user.email,
            'link': result.user.link,
            'picture': "https://graph.facebook.com/%s/picture?type=square" 
                % result.user.id,
            'credentials': result.user.credentials.serialize(),
            'show_fb_link': u.fb_link,
            'nickname': u.nickname,
            'reputation': u.reputation,
           }
    request.session['user'] = user
    return HttpResponseRedirect(reverse('post_list'))

def logout(request):
    request.session.pop("user", None)
    return HttpResponseRedirect(reverse('post_list'))

def validate_user_credentials(session):
    """helper function
    """
    if not session.has_key('user'):
        return False
    if not session['user'].has_key('credentials'):
        return False
    credentials = authomatic.credentials(session['user']['credentials'])
    if not credentials.valid:
        session.pop("user", None)
        return False
    if credentials.expire_soon(60 * 60 * 24): # expiring in a day
        credentials.refresh()
        session['user']['credentials'] = credentials.serialize()
    return True

def get_or_create_user(fb_id, nickname):
    # check db
    u = User.objects.filter(fb_id=fb_id).first()
    if u is None:
        User.objects.create(fb_id=fb_id, nickname=nickname)
        u = User.objects.filter(fb_id=fb_id).first()
    return u

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

def user_prefs(request):
    if not validate_user_credentials(request.session):
        return HttpResponseRedirect(reverse('post_list'))
    u = get_or_create_user(request.session['user']['fb_id'], None)
    if u is None:
        return HttpResponseRedirect(reverse('post_list'))
    db_userinfo = {'fb_link': u.fb_link, 'nickname': u.nickname,
            'reputation': u.reputation}
    context = dict(request.session['user'].items() + db_userinfo.items())
    return render(request, 'slapmaster/user_prefs.html', context)

def user_prefs_save(request):
    show_fb_link = True if request.POST.has_key('fb_link') else False
    nickname = request.POST['nickname']
    u = get_or_create_user(request.session['user']['fb_id'], None)
    u.fb_link = show_fb_link
    u.nickname = nickname
    u.save()
    request.session['user']['show_fb_link'] = show_fb_link
    request.session['user']['nickname'] = nickname
    # refresh session dict
    request.session['refresh'] = 1
    request.session.pop('refresh', 1)
    
    return HttpResponseRedirect(reverse('post_list'))
