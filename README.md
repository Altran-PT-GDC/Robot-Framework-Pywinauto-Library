### Remote Server Usage:

1. install Robot Framework, Remote Library and PyWinAuto
    - pip install robotframework
    - pip install robotremoteserver
    - pip install pywinauto

2. Launch the remote server: in this example we're using the localhost ip (127.0.0.1), in a real scenario an accessible ip should be used
    python PywinautoLibrary.py 127.0.0.1 8270
    
    Or a real scenario example:
    python PywinautoLibrary.py 192.168.0.2 8270
    
3. Execute a local robotframework script that imports the the remote library
    robot pywinauto_remote.robot
    
    
### Example Robot script:

    *** Settings ***
    Library  Remote  http://127.0.0.1:8270  WITH NAME  remote0
    
    *** Test Cases ***
    Launch and Close Notepad
        remote0.Start Application    notepad.exe
        sleep   2s
        remote0.Close Application
        