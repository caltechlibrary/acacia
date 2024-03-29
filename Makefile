#
# Simple Makefile
#
PROJECT = Acacia

VERSION = $(shell grep '"version":' codemeta.json | cut -d\"  -f 4)

static: .FORCE
	codemeta2cff
	echo "__version__ = '$(VERSION)'" >acacia/version.py
	./mk-static-pages.bash

website:
	./mk-website.bash

setup: requirements.txt
	python3 -m pip install -r requirements.txt

status:
	git status

save:
	@if [ "$(msg)" != "" ]; then git commit -am "$(msg)"; else git commit -am "Quick Save"; fi
	git push origin $(BRANCH)

refresh:
	git fetch origin
	git pull origin $(BRANCH)

publish:
	bash gen-nav.bash
	bash mk-website.bash
	bash publish.bash

clean: 
	@if [ -f version.go ]; then rm version.go; fi
	@if [ -d bin ]; then rm -fR bin; fi
	@if [ -d dist ]; then rm -fR dist; fi
	@if [ -d man ]; then rm -fR man; fi

release: 
	make -f Release.Mak

.FORCE:
