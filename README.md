# CamTool 2

This app allows to animate camera in Assetto Corsa.

Refactoring is required.
The app is not optimized (10 fps drop), the code is quite messy, poorly commented and spreaded among the files.
I coded this app, when I didn't have proper knowledge about programming (and Python). 

Version from racedepartment contains all required files (dll, icons):
https://www.racedepartment.com/downloads/camtool-2.15062/

This app reads data directly from a memory.
Everytime Assetto Corsa is updated, I have to find pointers and generate DLL file used by stdlib64/CamToolTool.py.
