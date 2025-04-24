# Adult participant administration system FRONTEND

Adult participant administration system, written in Django.

## Introduction

This Django project is part of a two-application system used to keep track of 
adult participants, experiments and appointments for the ILS Labs.

This project represents the frontend application, which is used by experiment 
leaders and participants.

## Requirements

* Python 3.9+ (3.8 might work, untested)
* Pip (for installing dependencies, see requirements.txt for details)
* A WSGI capable web server (not needed for development)
* A SQL database (tested with SQLite and MySQL)

## Installation

For production/acceptation deployment, please see our Puppet script. (Hosted on 
our private GitLab server).

Development instructions:
* Configure a working backend first!
* Clone this repository
* Install the dependencies using pip (it is recommended to use a virtual 
  environment!). ``pip install -r requirements.txt``
* Edit ``ppn_backend/settings.py`` to suit your needs. (Make sure you update the 
  backend location setting to your local setup!)
* Run all DB migrations ``python manage.py migrate``
* Compile the translation files using ``python manage.py compilemessages``
* You can now run a development server with ``python manage.py runserver``

The frontend does need a running backend to talk to! Otherwise it will be very 
unhelpful towards you.

## A note on dependencies
We use pip-tools to manage our dependencies (mostly to freeze the versions 
used). It's listed as a dependency, so it will be installed automatically.

``requirements.in`` lists the actual dependency and their version constraints. 
To update ``requirements.txt`` just run ``pip-compile -U``. Don't forget to test 
with the new versions!
