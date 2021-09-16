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

BASE_URL=""
if [ -f "settings.ini" ]; then
    BASE_URL=$(grep -E 'BASE_URL\s+=\s+' settings.ini | cut -d = -f 2 | sed -E 's/ //g')
fi

# Build navigation base on nav.tmpl and BASE_URL
mkpage "base_url=text:${BASE_URL}" nav.tmpl >htdocs/nav.md

for BNAME in $(find htdocs -type f | grep '.md$' | sed -E 's/htdocs\///;s/\.md$//'); do
  if [ "${BNAME}" != "nav" ]; then
    mkpage "body=htdocs/${BNAME}.md" \
         "nav=htdocs/nav.md" \
         "base_url=text:${BASE_URL}" \
	 page.tmpl \
         >"htdocs/${BNAME}.html" || exit 1
  fi
done

# Update templates/nav.tpl, templates/add-doi.tpl, templates/doi-submitted.tpl
pandoc htdocs/nav.md > templates/nav.tpl
pandoc forms/add-doi.md > templates/add-doi.tpl
pandoc forms/doi-submitted.md > templates/doi-submitted.tpl

