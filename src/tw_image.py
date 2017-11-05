from ConfigParser import SafeConfigParser
from collections import namedtuple

import tw_util
from hashlib import sha1
import hmac
import uuid 
import time
import urllib
import urllib2
import requests



basickey=namedtuple('basicprekey', 'method url oauth_consumer_key oauth_token postBody')
with_nonce_ts=namedtuple('with_nonce_ts', 'nonce timestamp basestr')

def createBasicKeyObj(parser,method="POST", url="", body=""):
    return basickey(method=method, \
            url=url, \
            oauth_consumer_key=parser.get("chimne", "consumer_key"), \
            oauth_token=parser.get('chimne', "access_key"), \
            postBody=body)

def createbasestring(_basickey):
    nonce=uuid.uuid4().hex
    timestamp=str(int(time.time()))
    basestring = ""
    basestring += tw_util.percentencode('oauth_consumer_key') + '=' + tw_util.percentencode(_basickey.oauth_consumer_key)
    basestring += '&' + tw_util.percentencode('oauth_nonce') + '=' + tw_util.percentencode(nonce)
    basestring += '&' + tw_util.percentencode('oauth_signature_method') + '=' + tw_util.percentencode('HMAC-SHA1')
    basestring += '&' + tw_util.percentencode('oauth_timestamp') + '=' + tw_util.percentencode(timestamp)
    basestring += '&' + tw_util.percentencode('oauth_token') + '=' + tw_util.percentencode(_basickey.oauth_token) 
    basestring += '&' + tw_util.percentencode('oauth_version') + '=' + tw_util.percentencode("1.0") 
    if  _basickey.postBody is not None: 
        basestring += '&' + tw_util.percentencode('status') + '=' + tw_util.percentencode(_basickey.postBody) 
    return with_nonce_ts(nonce=nonce, timestamp=timestamp, basestr=basestring)

def createsignaturebasestr(_basickey, nonce_ts_str):
    basestring=""
    if _basickey.method is not None:
        basestring += _basickey.method.upper() + '&'
    basestring += tw_util.percentencode(_basickey.url) + '&'
    basestring += tw_util.percentencode(nonce_ts_str.basestr)
    return basestring

def createsignature(parser, basestring):
    key= parser.get("chimne", "consumer_secret") + "&" + parser.get("chimne", "access_secret")
    raw = basestring
    hashed = hmac.new(key, raw, sha1)
    return hashed.digest().encode('base64').rstrip('\n')

def createOAuthHeader(_basickey, nonce_ts_str, signature):
    basestring = "OAuth "
    basestring += tw_util.percentencode('oauth_consumer_key') + '="' + tw_util.percentencode(_basickey.oauth_consumer_key) + '", '
    basestring += tw_util.percentencode('oauth_nonce') + '="' + tw_util.percentencode(nonce_ts_str.nonce) + '", '
    basestring += tw_util.percentencode('oauth_signature') + '="' + tw_util.percentencode(signature) + '", '
    basestring += tw_util.percentencode('oauth_signature_method') + '="' + tw_util.percentencode('HMAC-SHA1') + '", '
    basestring += tw_util.percentencode('oauth_timestamp') + '="' + tw_util.percentencode(nonce_ts_str.timestamp) + '", '
    basestring += tw_util.percentencode('oauth_token') + '="' + tw_util.percentencode(_basickey.oauth_token) + '", '
    basestring += tw_util.percentencode('oauth_version') + '="' + tw_util.percentencode("1.0") + '"'
    return basestring


def oauthheader(parser, o_method, o_url, o_body):
    _basickey=createBasicKeyObj(parser, method=o_method, url=o_url, body=o_body)
    _with_nonce_ts=createbasestring(_basickey)
    signatureready=createsignaturebasestr(_basickey, _with_nonce_ts)
    signature=createsignature(parser, signatureready)
    oauthheader=createOAuthHeader(_basickey, _with_nonce_ts, signature)
    header = {'Authorization': oauthheader, 'User-Agent': 'OAuth gem v0.4.4'}
    return header


def postmessage(parser, postbody):
    header = oauthheader(parser, "POST", "https://api.twitter.com/1.1/statuses/update.json", postbody)
    response = requests.post('https://api.twitter.com/1.1/statuses/update.json', data={'status':postbody}, headers=header)
    print response.content


def postimage(parser, imagepath):
    header = oauthheader(parser, None, "https://upload.twitter.com/1.1/media/upload.json", None)
    print header




parser = SafeConfigParser()
parser.read("chimne.cfg")
postmessage(parser, "hello big river")
#postimage(parser, "/helloworld.jpg")
    


    









#discover
#capitalone
#barclaycard