# **gdrive** Read Me

The file **gdrive** here is an executable Google Drive CLI interface from Petter Rasmussen. This is version 2.1.0, downloaded from GitHub [https://github.com/prasmussen/gdrive].

## Usage
### upload
Documentation for the *upload* function is on [https://github.com/prasmussen/gdrive#user-content-upload-file-or-directory]. The short version on *upload* usage is…

`gdrive upload FILENAME`

A local folder example would be…

`gdrive upload B7_1.png`

Full paths are also supported…

`gdrive upload /home/pi/supercooler/Captures/B7_1.png`

> NOTE: Wildcards are note allowed in the filename.

You can also create directories on your Google Drive account with *mkdir*…

`gdrive mkdir 20170630T195920Z`

An additional example is in the following *mkdir* section.

### mkdir
Documentation for the *mkdir* function is on [https://github.com/prasmussen/gdrive#create-directory]. The short version on *mkdir* usage is…

`gdrive mkdir 20170630T195920Z`

The standard output will return the Google ID for this folder…

`Directory 0BzpNPyJoi6uoWUI5N1JWT2dpOFU created`

This ID can then be used with the `-p` flag (parent) of an *upload* command to specify the destination folder…

`gdrive upload -p 0BzpNPyJoi6uoWUI5N1JWT2dpOFU B7_1.png`

### list
Documentation for the *list* function is on [https://github.com/prasmussen/gdrive#user-content-list-files]. The short version on *list* usage is…

`gdrive list`

This simple command returns the listing and IDs of the Drive root contents…

	Id                              Name              Type   Size       Created
	0BzpNPyJoi6uoM1BxTkJ6aXBNTkk    B6_1.png          bin    1.4 MB     2017-06-30 19:51:48
	0BzpNPyJoi6uoWUI5N1JWT2dpOFU    TestTimeStamp1    dir               2017-06-30 19:50:02
	0BzpNPyJoi6uoUkdyQmotTmN3WVU    B6_0.png          bin    1.5 MB     2017-06-30 15:36:23
	0BzpNPyJoi6uoVERwT3hMZjRVTGs    A1_0.png          bin    1.1 MB     2017-06-29 21:00:45
	0BzpNPyJoi6uobm9uTjhVNDBYNDQ    A0_0.png          bin    883.4 KB   2017-06-29 18:53:13
	0BzpNPyJoi6uoa0J2bUE5WUpwczA    captureD8.png     bin    1.6 MB     2017-06-29 18:01:46
	0BzpNPyJoi6uoODM1TWFTVW9HTXc    captureD4.png     bin    1.5 MB     2017-06-29 18:01:10
	0BzpNPyJoi6uoc3RhcnRlcl9maWxl   Getting started   bin    1.6 MB     2017-06-29 17:54:25

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