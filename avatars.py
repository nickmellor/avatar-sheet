#!/usr/bin/env python

import requests
import json
import sys
import os
from sheet import Sheet
from utils import save_github_avatar_with_token

organisation_id = sys.argv[1]
output_dir = 'images'
try:
    access_token = os.environ['COMMON_CODE_GITHUB_TOKEN']
except KeyError:
    raise Exception('No access key available. Please set up COMMON_CODE_GITHUB_TOKEN with your GitHub API token')

url = 'https://api.github.com/orgs/{org}/members?access_token={token}'.format(org=sys.argv[1], token=access_token)
request = requests.get(url)
if request.ok:
    usernames = [member['login'] for member in json.loads(request.text or request.content)]
    for username in usernames:
        source_image = os.path.join(output_dir, "{0}.png".format(username))
        save_github_avatar_with_token(username, source_image, access_token)
        Sheet(source_image).place_avatars().save_sheet()
        os.unlink(source_image)

