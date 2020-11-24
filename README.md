# Foxtrot API

[![apiary](https://img.shields.io/badge/ftf-apiary-9cf)](https://foxtrotapi.docs.apiary.io/)
[![website-status](https://img.shields.io/website?down_color=red&down_message=offline&up_message=online&url=https%3A%2F%2Fapi.foxtrotfanatics.com)](https://api.foxtrotfanatics.com)
[![pypi](https://img.shields.io/pypi/v/foxtrot-api)](https://pypi.org/project/foxtrot-api/)
[![issues](https://img.shields.io/github/issues/FoxtrotCore/foxtrot-api)](https://github.com/FoxtrotCore/foxtrot-api/issues)
[![docs](https://img.shields.io/readthedocs/foxtrot-api)](https://foxtrot-api.readthedocs.io/)
[![build-status](https://img.shields.io/github/workflow/status/FoxtrotCore/foxtrot-api/Deploy%20to%20PyPi)](https://github.com/FoxtrotCore/foxtrot-api/actions?query=workflow%3A%22Unit+Tests%22)
[![unit-tests-status](https://img.shields.io/github/workflow/status/FoxtrotCore/foxtrot-api/Unit%20Tests)](https://github.com/FoxtrotCore/foxtrot-api/actions?query=workflow%3A%22Deploy+to+PyPi%22)

An API for searching and delivering Code Lyoko transcripts and subtitles.

***

# Usage

Check out our

### [Apiary Documentation](https://foxtrotapi.docs.apiary.io)

## Install (from PyPi)

`$` `pip install foxtrot-api`

***

# Development and Contribution

## Install Live Development Version

`$` `pip install -e .[dev]`

## Run the API Locally *(via Green Unicorn with live-reload)*

`$` `gunicorn --workers 2 --bind :8080 --reload foxtrot_api.__main__:app`

## Create and Update Manifest

`$` `rm -f MANIFEST.in && check-manifest --update`

## Create and Update Sphinx Documentation

`$` `sphinx-apidoc -f -o docs foxtrot_api && make -C docs html`

***

# Deployment

As you would expect, everything in this section requires valid API tokens and misc authentication procedures. This is more of a note for the devs, really.

## Build and Deploy to PyPi

`$` `python setup.py bdist_wheel sdist && twine upload dist/*`

## Deploy to Google App Engine

`$` `gcloud app deploy`
