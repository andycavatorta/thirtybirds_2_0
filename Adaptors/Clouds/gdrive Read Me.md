# **gdrive** Read Me
The file **gdrive** here is an executable Google Drive CLI interface from Petter Rasmussen. This is version 2.1.0, downloaded from GitHub…
https://github.com/prasmussen/gdrive

## Upload Usage
The full documentation is on that GitHub with details of the upload function here…
https://github.com/prasmussen/gdrive#user-content-upload-file-or-directory
The short version on upload usage is…
`gdrive upload FILENAME`
A local folder example would be…
`gdrive upload B7_1.png`
Full paths are also supported…
`gdrive upload /home/pi/supercooler/Captures/B7_1.png`
> NOTE: Wildcards are note allowed in the filename.

## Deployment
The script I used to deploy **gdrive** from thirtybirds onto the local units was as follows…
	"sudo cp /home/pi/thirtybirds_2_0/Adaptors/Clouds/gdrive /home/pi/gdrive",
	"sudo chmod +x /home/pi/gdrive",
	"sudo install /home/pi/gdrive /usr/local/bin/gdrive",
	"mkdir /home/pi/.gdrive",
	"wget -P /home/pi/.gdrive/ http://theproblemislastyear.com/u23mkhJsVUPNJHnOYQJnM7arOAcEjkC2qdngPOOqnAafc2rqOSwPtFNf3FS2j4gh/token_v2.json”,
Short comments on each line…
1. copying to the home directory
2. making the program executable
3. “installing” via Linux so it is cleanly runnable from any location
4. making the folder for the JSON authorization file
5. copying the authorization file (*token\_v2.json*) from a public server to the local unit
After running this on all units, I removed the authorization file from the public server and removed line 5 from the *upgradeScripts.py* file to avoid any unnecessary web traffic and failures (should it run again).