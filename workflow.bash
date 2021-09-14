#!/bin/bash

#
# Workflow processes requests that come in via the submit email account
# as well as those DOI added manually. 
#
# 1. Get emails messages
# 2. Convert email messages to doi
# 3. Retrieve metadata for each doi
#
export PATH="/bin:/usr/bin:/usr/local/bin"
cd /Sites/acacia
if [ "$1" = "full" ]; then
./get-messages
./messages-to-doi
fi
./retrieve-metadata
