#!/bin/bash

#
# Regenerate the static application pages from their
# Markdown sources using Pandoc.
#


for BNAME in $(find htdocs -type f | grep '.md$' | sed -E 's/htdocs\///;s/\.md$//'); do
  if [ "${BNAME}" != "nav" ]; then
  mkpage "body=htdocs/${BNAME}.md" \
         "nav=htdocs/nav.md" \
	 page.tmpl \
         >"htdocs/${BNAME}.html"
  fi
done

# Update templates/nav.tpl
pandoc htdocs/nav.md > templates/nav.tpl

