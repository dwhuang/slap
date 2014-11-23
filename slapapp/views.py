from django.shortcuts import render

import httplib2
import urllib

from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
#from django.utils import simplejson as json
import simplejson as json

from profiles.models import Profile

def facebook(request):
    params = {
        'client_id': settings.FACEBOOK_APP_ID,
        'redirect_uri': 'http://localhost:8000/registration/facebook/',
        'client_secret': settings.FACEBOOK_SECRET_KEY,
        'code': request.GET['code']
    }

    http = httplib2.Http(timeout=15)
    response, content = http.request('https://graph.facebook.com/oauth/access_token?%s' % urllib.urlencode(params))
    
    # Find access token and expire (this is really gross)
    params = content.split('&')
    ACCESS_TOKEN = params[0].split('=')[1]
    EXPIRE = params[1].split('=')[1]
    
    # Get basic information about the person
    response, content = http.request('https://graph.facebook.com/me?access_token=%s' % ACCESS_TOKEN)
    data = json.loads(content)
    
    # Try to find existing profile, create a new user if one doesn't exist
    try:
        profile = Profile.objects.get(facebook_uid=data['id'])
    except Profile.DoesNotExist:
        user = User.objects.create_user(data['username'], data['email'], data['id'])
        profile = user.get_profile()
        profile.facebook_uid = data['id']
    
    # Update token and expire fields on profile
    profile.facebook_access_token = ACCESS_TOKEN
    profile.facebook_access_token_expires = EXPIRE
    profile.save()
    
    # Authenticate and log user in
    user = authenticate(username=profile.user.username, password=profile.facebook_uid)
    login(request, user)
    
    return HttpResponseRedirect('/')

def f(request):
    return HttpResponse("""<a class="ui-button" href="https://www.facebook.com/dialog/oauth?client_id=1529719137268268&redirect_uri=http://localhost:8000/facebook/">Log In with Facebook</a>""")
