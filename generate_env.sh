#!/bin/bash

# Load the config.json file
config=$(jq -r '. | to_entries[] | .key + "=" + (.value | tostring)' config.json)

# Create the .env file
echo "$config" > .env