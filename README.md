# Drive Inspector  
   
Drive Inspector is a web app to [Google Drive](https://www.google.com/drive/) - the file storage and synchronization service  
developed by Google - that let you store and work collaboratively with team members.  
This extension will let users to have insight on every team drive contributions  
statistics with visualizations. It is created specifically for markers' (lecturers, teachers etc.) use.  
  
## Requirements  
- Python 3.x
- Windows XP and above  
  
## Developers' Dependencies Installation:  
To install, simply use `pip`:  

```bash
$ pip install bottle google-api-python-client oauth2client
```
 to get:  
- bottle: the Python webserver framework  
- the rest: required for Google Drive API
  
`bottle: the micro web framework`  
This will be the bridge/connector we use to link frontend UI to backend python, it will  
 operate at port 7878 so that it won't clash with other applications. The way it works  
 is it handles web request (the URL) and return the value according to our code. It can  
 make use of templates under the `web` directory (e.g. index.tpl).  
  
`oauth2client: the third party OAuth`  
This will be how our web app handles login of users. They will be prompted to login  
their Google Drive account to access the team drives in which they are the drive members.  
  
## Developers Usage  
`serverstart.bat` will run the `main.py` which spawn a server instance on `localhost:7878` and open that page.  
**To work on it**  
Page to be viewed directly at *.tpl* (See index.tpl for example)  
Static file should be put under `web/static/` and access through `/static/<filename>`
  
## Directory Guide

- Project_Docs: Assignment 1 deliverables (PMP, AoA, RR, Retrospectives, Burndown Chart)
- src: Source code
- web: Web UI  
- dist: distribution package in .zip, together with uncompressed folders
  
## Clients Usage  
Run `dist\bin\driveinspector.exe` and a new tab with our web app loaded will be opened in clients' default browser.