#!/bin/bash

#
# Regenerate the static application pages from their
# Markdown sources using Pandoc.
#
for BNAME in "about" "dashboard" "help/overview" "help/index" "help/add-a-doi" "help/review" "help/export-to-eprints"; do
  mkpage "body=htdocs/${BNAME}.md" \
         "nav=htdocs/nav.md" \
	 page.tmpl \
         >"htdocs/${BNAME}.html"
done

# Update templates/nav.tpl
pandoc htdocs/nav.md > templates/nav.tpl

