#!/usr/bin/env python

import sys
import os
from sheet import Sheet
from utils import save_github_avatar

username = sys.argv[1]
output_dir = 'images'
source_image = os.path.join(output_dir, "{0}.png".format(username))
save_github_avatar(username, source_image)
Sheet(source_image).place_avatars().save_sheet()
os.unlink(source_image)

