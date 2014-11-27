from authomatic.providers import oauth2, oauth1, openid

AUTHOMATIC_CONFIG = {
    'fb': {
        'id': 5566,
        'class_': oauth2.Facebook,
        
        # Facebook is an AuthorizationProvider too.
        'consumer_key': '1507946739477315',
        'consumer_secret': '2ae7ab56208209dce836dea7386ac3a9',
        
        # But it is also an OAuth 2.0 provider and it needs scope.
        'scope': ['public_profile', 'email'],
    },
}
