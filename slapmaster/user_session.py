from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from authomatic import Authomatic
from authomatic.adapters import DjangoAdapter

from slapmaster.models import User
from slapmaster.config import AUTHOMATIC_CONFIG

class UserSession(object):
    authomatic = Authomatic(AUTHOMATIC_CONFIG, 'gadf48t7vhzv0-42djcajhdslapit')
    SESSION_KEY = 'user_session'

    def __init__(self, request):
        self.request = request
        if not request.session.has_key(self.SESSION_KEY):
            request.session[self.SESSION_KEY] = {}
        self.session = request.session[self.SESSION_KEY]

    def __save_session(self):
        self.request.session.modified = True

    """
    Note: this function is run (at least) twice during the login process,
    as required by Authomatic.login(). The second-time request contains
    GET variables.
    """
    def login(self):
        # test browser cookie
        if len(self.request.GET) == 0:
            self.request.session.set_test_cookie()
        else:
            if self.request.session.test_cookie_worked():
                # cookie worked
                self.request.session.delete_test_cookie()
            else:
                return HttpResponse("please enable cookie and try again")

        # login using authomatic
        response = HttpResponse()
        result = self.authomatic.login(DjangoAdapter(self.request, response), 
                'fb')
        if not result:
            # pending login
            return response
        if result.error:
            response.write(result.error.message)
            return response
        if not result.user:
            response.write("login result does not contain user info")
            return response
        # if the basic profile is not already provided, get it
        if not result.user.name or not result.user.id:
            result.user.update()
        # check if the db contains this user. Create one if it doesn't.
        user = User.objects.filter(fb_id=result.user.id).first()
        if not user:
            user = User.objects.create(fb_id=result.user.id, 
                    nickname=result.user.name)
        # store session info
        self.session['fb_id'] = result.user.id
        self.session['credentials'] = result.user.credentials.serialize()
        self.__save_session()

        return HttpResponseRedirect(reverse('post_list'))

    def logout(self):
        self.session.pop('fb_id', None)
        self.session.pop('credentials', None)
        self.__save_session()
        return HttpResponseRedirect(reverse('post_list'))

    def validate(self):
        if not self.session.has_key('fb_id') \
                or not self.session.has_key('credentials'):
            return False
        credentials = self.authomatic.credentials(self.session['credentials'])
        if not credentials.valid:
            self.logout()
            return False
        if credentials.expire_soon(60 * 60 * 24): # expiring in a day
            credentials.refresh()
            self.session['credentials'] = credentials.serialize()
            self.__save_session()
        return True

    @property
    def fb_pic_url(self):
        user = User.objects.filter(fb_id=self.session['fb_id']).first()
        if user:
            return user.fb_pic_url
        return ''

    @property
    def fb_url(self):
        user = User.objects.filter(fb_id=self.session['fb_id']).first()
        if user:
            return user.fb_url
        return ''

    @property
    def show_fb_url(self):
        user = User.objects.filter(fb_id=self.session['fb_id']).first()
        if user:
            return user.show_fb_url
        return ''

    @show_fb_url.setter
    def show_fb_url(self, value):
        user = User.objects.filter(fb_id=self.session['fb_id']).first()
        if user:
            user.show_fb_url = value
            user.save(update_fields=['show_fb_url'])

    @property
    def nickname(self):
        user = User.objects.filter(fb_id=self.session['fb_id']).first()
        if user:
            return user.nickname
        return ''

    @nickname.setter
    def nickname(self, value):
        if not value:
            return
        user = User.objects.filter(fb_id=self.session['fb_id']).first()
        if user:
            user.nickname = value
            user.save(update_fields=['nickname'])

    @property
    def reputation(self):
        user = User.objects.filter(fb_id=self.session['fb_id']).first()
        if user:
            return user.reputation
        return ''

