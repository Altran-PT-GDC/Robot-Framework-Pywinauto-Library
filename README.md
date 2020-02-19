#Robot Framework Pywinauto Library

A Robot Framework library that uses Pywinauto to test Windows desktop apps using keyword-driven test scripts.
This library is based on a old winbot.py library located in https://groups.google.com/forum/m/#!topic/robotframework-devel/lTPC2H4XxW8 and developed by Dragonfyre13. 

Altran created the library to be working in Python 3.x and the new versions of Pywinauto (0.6.8) and included the remote interface. 
New functionalities will added in a near future.

### Usage:
1. install Robot Framework, Remote Library and PyWinAuto
    - pip install robotframework
    - pip install pywinauto
    
3. Execute a local robotframework script that imports the library
    robot pywinauto.robot
    
### Example Robot script:
    *** Settings ***
    Library  PywinautoLibrary

    *** Test Cases ***
    Test Notepad
        Log    Testing open notepad
        Start Application    notepad.exe
        sleep    1s
        Get Dialog    Untitled - NotepadNotepad
        Type Keys    Edit    Teste
        Menu Select    File -> Save As...
        Get Dialog    Save As
        Type Keys    edit1    teste.txt
        Click    Save
        Close Application
    

# Remote Server
### Usage:

1. install Robot Framework, Remote Library and PyWinAuto
    - pip install robotframework
    - pip install robotremoteserver
    - pip install pywinauto

2. Launch the remote server: in this example we're using the localhost ip (127.0.0.1), in a real scenario an accessible ip should be used
    python PywinautoLibrary.py 127.0.0.1 8270
    
    Or a real scenario example:
    python PywinautoLibrary.py 192.168.0.2 8270
    
3. Execute a local robotframework script that imports the remote library
    robot pywinauto_remote.robot
    
    
### Example Robot script:
    *** Settings ***
    Library  Remote  http://127.0.0.1:8270  WITH NAME  remote0
    
    *** Test Cases ***
    Launch and Close Notepad
        remote0.Start Application    notepad.exe
        sleep   2s
        remote0.Close Application
        
