#
# Makefile to setup and test Acacia
#
build: settings.ini acacia.db

settings.ini:
	cp settings.ini-example settings.ini
	$(EDITOR) settings.ini

acacia.db: requirements.txt
	python3 -m pip install -r requirements.txt
	./configure-database

test: .FORCE
	./test-eprints-ssh

run: .FORCE
	./configure-database
	./get-messages
	./messages-to-doi
	./retrieve-metadata

clean: .FORCE
	@for FNAME in $(shell ls -1 *.bak); do rm $$FNAME; done
	@for FNAME in $(shell ls -1 acacia/*.bak); do rm $$FNAME; done

.FORCE:
