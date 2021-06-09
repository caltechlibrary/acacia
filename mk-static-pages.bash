#!/bin/bash

#
# Regenerate the static application pages from their
# Markdown sources using Pandoc.
#
for BNAME in "about" "dashboard"; do
  mkpage "body=acacia/static/${BNAME}.md" \
         "nav=acacia/static/nav.md" \
	 page.tmpl \
         >"acacia/static/${BNAME}.html"
done

