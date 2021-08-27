#!/bin/bash

#
# Regenerate the static application pages from their
# Markdown sources using Pandoc.
#

# Check for Pandoc
PANDOC=$(which pandoc)
if [ "${PANDOC}" = "" ]; then
    echo "ERROR: Cannot find pandoc."
    echo ""
    echo "Pandoc is required to build static content."
    echo "See https://pandoc.org/ for details"
    exit 1
fi
MKPAGE=$(which mkpage)
if [ "${MKPAGE}" = "" ]; then
    echo "ERROR: Cannot find mkpage."
    echo ""
    echo "mkpage is required to build static content."
    echo "See https://github.com/caltechlibrary/mkpage for details"
    exit 1
fi


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
pandoc forms/add-doi.md > templates/add-doi.tpl
pandoc forms/doi-submitted.md > templates/doi-submitted.tpl

