*** Settings ***
Library  Remote    http://127.0.0.1:8270    WITH NAME    remote0

*** Test Cases ***
Test Notepad
    Log    Testing open notepad
    remote0.Start Application    notepad.exe
    sleep    1s
    remote0.Get Dialog    Untitled - NotepadNotepad
    remote0.Type Keys    Edit    Teste
    remote0.Menu Select    File -> Save As...
    remote0.Get Dialog    Save As
    remote0.Type Keys    edit1    teste.txt
    remote0.Click    Save
    remote0.Close Application
