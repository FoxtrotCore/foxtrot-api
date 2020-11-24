# Foxtrot API

An API for searching and delivering Code Lyoko transcripts and subtitles.

### [Apiary Documentation](https://foxtrotapi.docs.apiary.io)

## Install (from PyPi)

`$` `pip install foxtrot-api`

***

# Development and Contribution

## Build

`$` `python setup.py bdist_wheel sdist`

## Run the API Locally With Green Unicorn

`$` `gunicorn --workers 2 --bind :8080 --reload foxtrot_api:app`

## Deploy to PyPi

`$` `twine upload dist/*`

## Install Locally

`$` `pip install -e .`

## Install Development Version Locally

`$` `pip install -e . [dev]`

## Create or Update Manifest

`$` `rm -f MANIFEST.in && check-manifest --update`

## Create or Update Sphinx Documentation

`$` `sphinx-apidoc -f -o docs foxtrot_api && make -C docs html`
