## Deployment  

We use the `PyInstaller` module to 'freeze' our Python program into stand-alone  
executable. Currently, we plan to only deliver executable for Windows platform.  
Other platforms will be considered in the future.  
  
## Maintenance  

Our Drive Inspector need not regular maintenance as it is running on clients' devices.  
The only maintenance needed is when Google Drive API is changed since it is our main  
depedency. If any bug is found or predicted, a short sprint will be carried out among  
the team to address the raised issue.  
  
## Dependencies  

- `Bottle web framework` 
- `Google Drive REST API`
- `oauth2client`
- `httplib2`  
  
If any of the dependencies listed above is changed, maintenance process will be carried out  

## Product Performance Feedback  

Mandatory communication (*a feedback form*) is required upon the first release to ensure  
our web app works as intended. The feedback obtained will act as a baseline in order to  
be checked against in the future in the case of updates. Clients can always contact the  
team through a preset button in app to submit any issue/bug found.  
  
## Updates and Patches  

Upon launching of app, the program will automatically check for updates at server. If  
there is any update available, the program will update itself automatically. Updates  
include bug fixes, upgrades etc. All of these are automated by script in program without 
the need of manual work.

