
# 
# The broad classes of files we'll be interested in
#
SRC_POSTS = $(wildcard src/posts/*.md)
POSTS := $(patsubst src/posts/%.md,site/posts/%.html,$(SRC_POSTS))
PAGES := $(patsubst src/pages/%.md,site/%.html,$(wildcard src/pages/*.md))
ASSETS := $(patsubst src/assets/%,site/assets/%,$(shell find src/assets -type f))
RSS_ITEMS := $(patsubst src/posts/%.md,tmp/%.rss,$(SRC_POSTS))


#
# If you're publishing a static site on S3 you can define your bucket
# here and the `sync` target will sync your site.
#
S3URI=s3://your-bucket-name.com

#
# Targets
#
all: posts pages assets misc

posts: $(POSTS)
pages: $(PAGES)
assets: $(ASSETS)
misc: site/index.html site/feed.xml site/favicon.ico site/robots.txt

############
# Rules

#
# The blog index.
# index.html is generated from index.md...
#
site/index.html:  tmp/index.md src/site-metadata.yaml src/templates/page.html | site
	pandoc \
		--standalone\
		--css="/assets/main.css"\
		--template=src/templates/page.html \
		-o site/index.html \
		src/site-metadata.yaml $<

#
# ...index.md is generated by a python script
# that reads the $(SRC_POSTS)
#
tmp/index.md:  $(SRC_POSTS) | tmp
	cat src/posts-header.md > $@
	bin/blog-index.py $(SRC_POSTS) >> $@

#
# The RSS feed
#
site/feed.xml: $(SRC_POSTS) | site
	bin/rss.py $^ > $@

#
# Generate a post from a markdown file.
#
site/posts/%.html:  src/posts/%.md  src/templates/page.html src/site-metadata.yaml | site/posts
	pandoc	\
		--standalone \
		--css="/assets/main.css" \
		--metadata=date:`echo $< | cut -d/ -f 3 | cut -c1-10` \
		--template=src/templates/page.html \
		--output $@ \
		src/site-metadata.yaml $<


#
# Generate a page (not a dated blog post) from a markdown file
# in src/pages
site/%.html:  src/pages/%.md src/site-metadata.yaml src/templates/page.html | site
	mkdir -p `dirname $@`
	pandoc\
		--standalone\
		--css="/assets/main.css"\
		--template=src/templates/page.html\
	 --output $@ \
	 src/site-metadata.yaml $<


# copy all the assets into the assets directory
# (if we do each file as its own rule, make -j can parallelize this)
site/assets/%: src/assets/% | site/assets
	mkdir -p `dirname $@`
	cp $< $@

# copy the favicon
site/favicon.ico: src/favicon.ico
	cp $< $@

# copy the robots.txt
site/robots.txt: src/robots.txt
	cp $< $@


####
# Utilities

# start a local webserver to view the site
serve: all
	python -m http.server --directory site 8000 

# sync the site to an AWS S3 bucket
sync: all
	aws s3 sync --delete site $(S3URI) 

# make directories if needed
site:
	mkdir site
tmp:
	mkdir tmp
site/assets:
	mkdir -p site/assets
site/posts:
	mkdir -p site/posts

# clean up
clean:
	rm -rf site tmp