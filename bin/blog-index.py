#!/usr/bin/env python
"""
Loop over a list of blog post src filenames and 
generate a blog index markdown file.
"""

import sys
import os.path
from datetime import datetime

from utils import parse_metadata


POST_TEMPLATE = """
---

## [{title}]({htmlname})
### {subtitle}

{description}

_{datestr}_ | [Read more...]({htmlname})

"""

def post_index(filenames):
    for file in sorted(filenames,reverse=True):
        path,name = os.path.split(file)


        htmlname = file[4:-3] + '.html'
        with open(file,'r') as f:
            md = parse_metadata(f.read())

        #DATESTR
        md['datestr'] = str(datetime.strptime(name[:10],'%Y-%m-%d').date())
        if 'subtitle' not in md:
            md['subtitle'] = ''
        print(POST_TEMPLATE.format(htmlname=htmlname,**md))

if __name__=='__main__':
    post_index(sys.argv[1:])
