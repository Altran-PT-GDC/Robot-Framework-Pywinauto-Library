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
