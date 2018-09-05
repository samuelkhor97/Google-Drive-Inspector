#Don't read me 

## If you're asked to read this, then read this part:

### SPECIAL DELIVERY: THE NEW THINGS 29/08/18

`venv: python virtual environment`
I bundled venv together in the repo so that we can develop using the same environment, putting here is the easiest delivery method as well. (It sucks, there are 3k+ files)
Anyway, the current and foreseen external libraries use urged me to do this, so you guys don't have to configure your working environment anymore.
Currently installed packages: `bottle google-api-python-client oauth2client` (bottle: the webserver framework, the rest: required for gdrive API)
**Usage**
`pyshell.bat` Start a pyshell instance (with all the variables loaded)
You will see a `(venv)` prefix in the command prompt, that indicates you are in correct working state and good to go.  You might have used the command `py` in the past, but now, `python` is the new `py` (if you have globally configured `python` instance, then use `vpython` instead).  *Please tell me if you encounter any directory issue*

`bottle: the micro web framework`
This will be the bridge/connector we use to link frontend UI to backend python, it will operate at port 7878 so that it won't clash with other applications.  The way it works is it handles web request (the URL) and return the value according to our code.  It can make use of templates under the `web` directory (e.g. index.tpl).  
**Usage**
`startserver.bat` Run the `realmain.py` which spawn a server instance on `localhost:7878` and open that page.
**To work on it**
Page to be viewed directly should be crafted and rename to *.tpl. (See index.tpl for example), static file should be put under `web/static/` and access throught `/static/<filename>`

## Insist, if you still, important information, here you might find.

### Directory Guide

- Project_Docs: Assignment 1 deliverables (PMP, AoA, RR)
- src: Source code
- web: Web UI
- venv: Virtual Environment (for development use)

