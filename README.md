# image-metadata-extractor
Dataloop FaaS example for a function that extracts image exif information and uploads it to item's metadata.

This function is ready to use. There are two ways to push and deploy it to Dataloop Platform:

###1. CLI

cd (this directory)

dlp projects checkout --project-name (name of the project)

dlp packages push --checkout

dlp packages deploy --checkout

###2. SDK

Run the script in create_function_script.py

##Requirements
You need to have dtlpy installed, if don't already, install it by running:
pip install dtlpy --upgrade