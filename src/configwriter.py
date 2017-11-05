import ConfigParser


config=ConfigParser.RawConfigParser()
config.add_section("chimne")
config.set("chimne","AUTHENTICATION","https://api.twitter.com/oauth2/token")
config.set("chimne","REQUEST_TOKEN","https://api.twitter.com/oauth/request_token")
config.set("chimne","AUTHORIZE_URL","https://api.twitter.com/oauth/authorize")
config.set("chimne","ACCESS_TOKEN_URL","https://api.twitter.com/oauth/access_token")
config.set("chimne","CONSUMER_KEY","aaaaaaaaaaaaaaaaaaa")
config.set("chimne","CONSUMER_SECRET","aaaaaaaaaaaaaaaaaa")
config.set("chimne","ACCESS_KEY","aaaaaaaaaaaaaaa")
config.set("chimne","ACCESS_SECRET","aaaaaaaaaaaaa")
with open("chimne.cfg", "wb") as configfile:
    config.write(configfile)


