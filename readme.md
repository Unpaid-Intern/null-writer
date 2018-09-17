# null-writer is a lightweight OS for making your own
# single-purpose writing device 

## Is your old Alphasmart finally giving out on you, but you are having a hard time affording the $500 to get a freewrite?
# That's the situation I found myself in so I've been trying to find a way to put together a platform agnostic writer's OS that can be installed on C.H.I.P., Raspberry Pi, or any similar computing platform with minimal hassle.  Then using some combination of a usb keyboard, a touch screen/e-reader display and a hand made or 3d printed case, I should be able to make a null-writer for around $80 bucks? We'll see!

# This version is an experimental proof of concept written using asciimatics (a curses like package) and python.  
# WARNING: Use at your own risk! I will be adding text output and automatic backup features, but in v1.0 it is just a few text fields attached to a sqlite Db, so please do not use it for professional writing! Journaling might be fine if you are okay with not being able to directly export your text files, and the possiblity of losing it all.  


############################################### Notes for User
## Installation
# to install null-writer, simply put the null-writer project folder (the directory this readme is in now) somewhere on the device of your choosing.
# Next, install the only dependency besides python:
# $ apt-get install asciimatics==1.9.0  
# $ pip install asciimatics==1.9.0

# To manually test your install, navigate to /your_install_path/null-writer/src/ and run 'python app.py'
# If that all goes well, then you can create a script that will run the command: "python app.py" whenever your device boots up.



################################################ Notes for Development
#Installation is the same, except you can drop the bit about creating a script to run the app on boot. The project is in python and not compiled so the entire thing pretty much just lives in the app.py file.

## Project file name style guide
# database name convention:
# no underscores, dashes, or capitalization: tableconventionexample.columnexamplename

# file structure convention:
# files are all lower case with dashes: file-name-example.file

# folder structure convention:
# folders are all lower case with underscores: folder_name_example

