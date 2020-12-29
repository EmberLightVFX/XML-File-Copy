# XML File Copy
Copy files from an XML file.

### Requirements:
* For Windows you need to insall Python 3.x
* For Mac you're fine with the pre-installed Python 2.7
* Linux is not yet tested
* 
All needed external libraries are located in the PythonLib folder.

## Usage
* Windows - double click XML File Copy.pyw or run `python "XML File Copy.pyw"` from cmd
* Mac - Execute XML File Copy.command

##### Copy from XML:
1. Select `File copy` in the top.
2. Select XML file.
3. Select location to copy files to.
4. If files aren\'t located where the xml says they are, select were we can find them under External path.
5. If you want to clone the tree structure, enable "Clone tree-structre".
	To not copy the whole folder structure to your tree structure, select what location that should be the root of the tree structure.
6. If your xml includes sequenced files, enabled "Transfer sequenced files".
	Enter what extensions your sequences uses, eg .R3D, .png, .exr

##### Start Resilio sync:
1. Select `Resilio Selective Sync` in the top.
2. Select XML file.
3. If files aren\'t located where the xml says they are, select were we can find them under External path.
4. If your xml includes sequenced files, enabled "Transfer sequenced files".
	Enter what extensions your sequences uses, eg .R3D, .png, .exr

![GUI](/extra/gui.jpg)