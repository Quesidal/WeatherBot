from unsplash.api import Api
from unsplash.auth import Auth

from local_keys import UNSPLASH_CLIENT_ID, UNSPLASH_CLIENT_SECRET

client_id = UNSPLASH_CLIENT_ID
client_secret = UNSPLASH_CLIENT_SECRET
redirect_uri = "urn:ietf:wg:oauth:2.0:oob"
code = ""

auth = Auth(client_id, client_secret, redirect_uri, code=code)
wallpaper = Api(auth)


def rand_wallpaper():
    a = wallpaper.photo.random()[0]
    url = wallpaper.photo.download(a.id)['url']
    return url
