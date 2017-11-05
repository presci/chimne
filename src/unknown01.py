
    import oauth2 as oauth
    import json
    import urllib
    import urllib2
    from collections import namedtuple
    import time
    from hashlib import sha1
    import hmac
    import uuid
    import base64


    AUTHENTICATION="https://api.twitter.com/oauth2/token"
    REQUEST_TOKEN="https://api.twitter.com/oauth/request_token"
    AUTHORIZE_URL="https://api.twitter.com/oauth/authorize"
    ACCESS_TOKEN_URL="https://api.twitter.com/oauth/access_token"


    CONSUMER_KEY="dpFi3ScEXuv2JxPQE66rjAus9"
    CONSUMER_SECRET="XiIpnyChvPzQhYlR8MEzDXUOn3PvrToTJT0cNiz9avOw4ks9H3"
    ACCESS_KEY="100065890-Y3BaXEMGobxIwEqatv4W6JbjtIVtVVsdGZzti9cW"
    ACCESS_SECRET="1KtaNTrKI1eGjrZfDHzDQParujsRKV5zJXkBd8kBjCHQm"

    OAuth_Basic=namedtuple("OAuth_Basic", "oauth_consumer_key oauth_signature_method  oauth_version")
    baseString=namedtuple("baseString", "timeStamp string nonce status")
    SendRequest=namedtuple("SendRequest", "method url timestamp upload")



    def basestring(oauth, access_key, body=None):
        timestamp = str(int(time.time()))
        nonce= base64.b64encode(str(uuid.uuid4().hex))
        basestring=percentencode("oauth_consumer_key") + "=" + percentencode(oauth.oauth_consumer_key) + "&"
        basestring+=percentencode("oauth_nonce") + "=" + percentencode(nonce) + "&"
        basestring+=percentencode("oauth_signature_method") + "=" + percentencode(oauth.oauth_signature_method) + "&"
        basestring+=percentencode("oauth_timestamp") + "=" + percentencode(timestamp) + "&"
        basestring+=percentencode("oauth_token") + "=" + percentencode(access_key) + "&"
        basestring+=percentencode("oauth_version") + "=" + percentencode(oauth.oauth_version)
        if body:
            basestring+="&" + percentencode("status") + "=" + percentencode(body)
        return baseString(timeStamp=timestamp, string=basestring, nonce=nonce, status=body)

    def sign_request(signature, consumer_secret, access_secret):
        key = consumer_secret + "&" + access_secret
        hashed = hmac.new(key, signature, sha1)
        return hashed.digest().encode("base64").rstrip('\n')
        

    def signaturebasestring(request, basestr, upload=False):
        if not upload:
            return percentencode(request.method) + "&" + percentencode(request.url) + "&" + percentencode(basestr)
        return percentencode(request.url) + "&" + percentencode(basestr)


    def sendrequest(s_oauth, s_basestring, s_request, s_signature):
        oauth_header="OAuth oauth_consumer_key=\""+s_oauth.oauth_consumer_key+"\", oauth_nonce=\""+s_basestring.nonce+"\", oauth_signature=\""+percentencode(s_signature)+"\", oauth_signature_method=\""+s_oauth.oauth_signature_method+"\", oauth_timestamp=\""+s_request.timestamp+"\", oauth_token=\""+ACCESS_KEY+"\", oauth_version=\""+s_oauth.oauth_version+"\"" 
        headers = {"Authorization": oauth_header, "Content-type": "application/x-www-form-urlencoded", "Host":"api.twitter.com", "User-Agent":"OAuth gem v0.4.4", "oauth_consumer_key":s_oauth.oauth_consumer_key}
        status = {"status":s_basestring.status}
        encoded_args = urllib.urlencode(status)
        req = urllib2.Request(s_request.url, encoded_args, headers)
        resp = None
        try:
            resp = urllib2.urlopen(req)
            
        except urllib2.HTTPError, e:
            print "httperror :" + str(e.code) 
            print e.reason
            print resp.read()
        except urllib2.URLError, e:
            print "urlerror :" + str(e.code) 
            print e.reason
        except httplib.HTTPException, e:
            print "httpexception :" + str(e.code) 
            print e.reason
        

    def percentencode(val):
        return val.replace(" ", "%20").replace("!", "%21").replace("&", "%26").replace("/", "%2F").replace("=", "%3D").replace("+", "%2B").replace(",", "%2C").replace("-", "%2D").replace(".", "%2E")

    p_oauth=OAuth_Basic(oauth_consumer_key=CONSUMER_KEY, oauth_signature_method="HMAC-SHA1", oauth_version="1.0")
    p_basestring=basestring(p_oauth, ACCESS_KEY, "hello world")
    p_request = SendRequest(method="POST", url="https://api.twitter.com/1.1/statuses/update.json", timestamp=p_basestring.timeStamp,  upload=False)
    signature=sign_request(signaturebasestring(p_request, p_basestring.string, False), CONSUMER_SECRET, ACCESS_SECRET)
    sendrequest(p_oauth, p_basestring, p_request, signature)
