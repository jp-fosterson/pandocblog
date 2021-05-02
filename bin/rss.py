#!/usr/bin/env python

import sys
import os.path
import re
from datetime import datetime
from rfeed import Feed,Item,Guid

from utils import parse_metadata

def strip_markdown(s):
    """
    Strip some common markdown out of
    the description, for the cases where the
    description is taken from the first paragraph
    of the text.
    """
    s = re.sub("[\\[\\]]", "", s)
    s = re.sub("\(.*\)", "", s)
    return s

def rss(filenames):
    """
    Read the site metadata and 
    metadata from all the given markdown files
    and compose the rss xml feed.
    """
    itemlist = []
    with open('src/site-metadata.yaml') as f:
        site = parse_metadata(f.read())

    for file in sorted(filenames,reverse=True):

    # Convert the markdown file src path into
        # the html site path.
        path,name = os.path.split(file)
        htmlname = file[4:-3] + '.html'

        # Read the site metadata.
        with open(file,'r') as f:
            md = parse_metadata(f.read())

        link = site['site-link']  + htmlname
        itemlist.append(
            Item(
                title = md['title'],
                description = strip_markdown(md.get('description')),
                author = md.get('author'),
                pubDate = datetime.strptime(name[:10],'%Y-%m-%d'),
                link = link,
                guid = Guid(link),
                )
            )

    feed = Feed(
        title = site['site-title'],
        link = site['site-link'],
        description = site['site-description'],
        language = "en-US",
        lastBuildDate = datetime.now(),
        items = itemlist,

    )
    
    return feed.rss()

if __name__=='__main__':
    print(rss(sys.argv[1:]))
