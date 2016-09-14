import urllib.request


def save_github_avatar(username, filename):
    avatar_url = 'https://github.com/{0}.png'.format(username)
    urllib.request.urlretrieve(avatar_url, filename)


def save_github_avatar_with_token(username, filename, token):
    avatar_url = 'https://github.com/{0}.png/?access_token={1}'.format(username, token)
    urllib.request.urlretrieve(avatar_url, filename)
