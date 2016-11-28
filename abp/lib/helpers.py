import urllib


def url_decode(s):
    return urllib.unquote(s).decode('utf8')
