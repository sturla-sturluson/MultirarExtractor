## Extracting multi rar files

A app that scans, extracts and cleans up those pesky multi rar files that all the torrent sites still use for some reason

Two implementations for this, the terminal-ui and a GUI-tkinter one

Both require at least python 3.10

### Using the GUI

- Run "tkinter_main.py"

- Select directories you want to scan by cliking "Open file dialog"

  - You can then Toggle those directories on and off by clicking on them

- Hit search to scan

- Extract All to extract all the files

- Delete All: Deletes all rar files in the directories

- Delete Extracted: Deletes only extracted rar files

- Extract and Delete: Extracts all files and deletes the rar files

### Using the terminal

- Run "terminal_main.py"

- Currently you just change the directories in the code

  - Variable name is "extract_path"
