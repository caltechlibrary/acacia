#!/bin/bash

#
# Regenerate the static application pages from their
# Markdown sources using Pandoc.
#
for BNAME in "about" "dashboard"; do
  mkpage "body=htdocs/${BNAME}.md" \
         "nav=htdocs/nav.md" \
	 page.tmpl \
         >"htdocs/${BNAME}.html"
done

