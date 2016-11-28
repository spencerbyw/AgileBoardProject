import urllib


def cln(s):
    return urllib.unquote(s).decode('utf8')
