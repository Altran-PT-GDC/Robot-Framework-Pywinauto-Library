###
# pyWinAuto library for Robot Framework and Python 3
# Based on the winbot library developed by xxxx for python 2 and adapted by Altran for Python 3 and
# added a remote interface, please check the README for remote usage instructions
###

#TODO: Check all depracated items
#TODO: Develop library unit tests

import pywinauto
from robot.api.deco import keyword
from pywinauto import application as pwa


class PywinautoLibrary:
    def __init__(self):
        self.app = None
        self.dlg = None

    @keyword("Set Timeout")
    def setTimeout(self, timeout_type, new_timeout_time):
        """
        Set the timeout value to something other than the defaults. Below are the acceptable timeout types, and thier associated timeout defaults.

        Also acceptable are the timeout type of "default" and the timeout time of "fast", "slow" or "default". These are predefined timeout templates.

        * window_find_timeout (default 3)
        * window_find_retry (default .09)
        * app_start_timeout (default 10)
        * app_start_retry (default .90)
        * exists_timeout (default .5)
        * exists_retry (default .3)
        * after_click_wait (default .09)
        * after_clickinput_wait (default .01)
        * after_menu_wait (default .05)
        * after_sendkeys_key_wait (default .01)
        * after_button_click_wait (default 0)
        * before_closeclick_wait (default .1)
        * closeclick_retry (default .05)
        * closeclick_dialog_close_wait (default .05)
        * after_closeclick_wait (default .2)
        * after_windowclose_timeout (default 2)
        * after_windowclose_retry (default .5)
        * after_setfocus_wait (default .06)
        * after_setcursorpos_wait (default .01)
        * sendmessagetimeout_timeout (default .001)
        * after_tabselect_wait (default .01)
        * after_listviewselect_wait (default .01)
        * after_listviewcheck_wait default(.001)
        * after_treeviewselect_wait default(.001)
        * after_toobarpressbutton_wait default(.01)
        * after_updownchange_wait default(.001)
        * after_movewindow_wait default(0)
        * after_buttoncheck_wait default(0)
        * after_comboselect_wait default(0)
        * after_listboxselect_wait default(0)
        * after_listboxfocuschange_wait default(0)
        * after_editsetedittext_wait default(0)
        * after_editselect_wait default(0)
        """
        timeout_types = ["window_find_timeout", "window_find_retry", "app_start_timeout", "app_start_retry",
                         "exists_timeout",
                         "exists_retry", "after_click_wait", "after_clickinput_wait", "after_menu_wait",
                         "after_sendkeys_key_wait",
                         "after_button_click_wait", "before_closeclick_wait", "closeclick_retry",
                         "closeclick_dialog_close_wait", "after_closeclick_wait",
                         "after_windowclose_timeout", "after_windowclose_retry", "after_setfocus_wait",
                         "after_setcursorpos_wait",
                         "sendmessagetimeout_timeout", "after_tabselect_wait", "after_listviewselect_wait",
                         "after_listviewcheck_wait",
                         "after_treeviewselect_wait", "after_toobarpressbutton_wait", "after_updownchange_wait",
                         "after_movewindow_wait",
                         "after_buttoncheck_wait", "after_comboselect_wait", "after_listboxselect_wait",
                         "after_listboxfocuschange_wait",
                         "after_editsetedittext_wait", "after_editselect_wait", "default"]

        if timeout_type not in timeout_types:
            raise ValueError(str(timeout_type + " is not one of the valid timeout types."))

        if timeout_type == "default":
            if new_timeout_time == "default":
                pywinauto.timings.Timings.Defaults()
            elif new_timeout_time == "fast":
                pywinauto.timings.Timings.Fast()
            elif new_timeout_time == "slow":
                pywinauto.timings.Timings.Slow()
            else:
                raise ValueError(str(new_timeout_time + ' needs to be either "fast", "slow" or "default"'))
        else:
            # make sure we don't have anything other than a float or an int here.
            new_timeout_time = float(new_timeout_time)
            exec("pywinauto.timings.Timings." + timeout_type + " = " + str(new_timeout_time))

            print("changed " + timeout_type + " to " + str(new_timeout_time))
            return True

    @keyword
    def DisconnectFromApplication(self):
        """
        Remove the current reference to an application and dialog.
        """
        self.app = None
        self.dlg = None

    @keyword
    def GetExistingApplication(self, titleRegex):
        """
        Given a regex that indicates the window's title text, set the window as the current context.
        """
        # Reset the dialog and application contexts. We're selecting a new application, so niether of these are valid anymore.
        self.dlg = None
        self.app = None

        # TODO: need to put a sleep/wait loop here, right now it just fails if the window doesn't already exist.
        self.app = pwa.Application().connect(title_re=titleRegex)

    @keyword("Start Application")
    def startApplication(self, startCommand):
        """
        Given a command, execute it and return the identifier for the window it started.
        """
        # Reset the dialog and application contexts. We're selecting a new application, so niether of these are valid anymore.
        self.dlg = None
        self.app = None
        try:
            self.app = pwa.Application().start(startCommand)
        except pwa.AppStartError:
            print("could not start the application \"" + startCommand + '"')
            raise
        # Set the dialog back to nothing. We selected a new application, of course the dialog is nothing.

    @keyword("Close Application")
    def closeApplication(self):
        """
        Close the application in context
        """
        try:
            self.app.kill()
        except pwa.AppNotConnected:
            print("could not close the application \"" + self.app + '"')
            raise
        # Set the dialog back to nothing. We selected a new application, of course the dialog is nothing.

        # Reset the dialog and application contexts. We're selecting a new application, so niether of these are valid anymore.
        self.dlg = None
        self.app = None

    @keyword
    def GetDialogFromRegex(self, regex):
        """
        Given a regex, set the dialog who's title matches (in the current application) to the current context.
        """
        # TODO: make sure an app is selected first. Raise an error if not.
        if self.app:
            try:
                self.dlg = self.app.window_(title_re=regex)
                self.dlg.draw_outline()
            except:
                print('could not find the application matching "' + regex + '"')
        else:
            print('No application currently selected. Searching for an application matching "' + regex + '"')
            try:
                self.app = pwa.Application().connect(title_re=regex)
            except:
                print(
                    "Could not find application matching \"" + regex + '" while searching for a dialog. No '
                                                                       'application was previously selected.')
                raise
            print("Found an application matching \"" + regex + '". Set this application to the current context.')
            print('Searching for a matching dialog ("' + regex + '")')
            try:
                self.dlg = self.app[regex]
                self.dlg.draw_outline()
            except:
                print('dialog not found matching "' + regex + '"')
                raise

    @keyword
    def GetDialog(self, title):
        """
        Given an exact title, set the dialog matching it (in the current application) to the current context.
        If no application is selected currently, attempt to match both the application and dialog to this title.
        """
        # make sure there's an app selected. If there isn't, try to get an app matching the dialog name.
        if self.app:
            try:
                self.dlg = self.app[title]
                self.dlg.draw_outline()
            except:
                print('could not find a dialog with the title "' + title + '" associated with the current application')
                raise
        else:
            print('No application currently selected. Searching for an application with the title "' + title + '"')
            try:
                self.app = pwa.Application().connect(title_re=title)
            except:
                print(
                    'Could not find application with the title "' + title + '" while searching for a dialog with that '
                                                                            'title. No application was previously '
                                                                            'selected.')
                raise
            print('Found an application with the title "' + title + '". Set this application to the current context.')
            print('Searching for a dialog with the same title. ("' + title + '")')
            try:
                self.dlg = self.app[title]
                self.dlg.draw_outline()
            except:
                print('dialog not found with the title "' + title + '"')
                raise

    @keyword
    def OutlineDialog(self):
        """
        Draw an outline around the current dialog
        """
        # Verify that we have an app and dialog selected.
        if self.app is not None:
            raise UnboundLocalError("There is no application context currently set")
        if self.dlg is not None:
            raise UnboundLocalError("There is no dialog context currently set")

    @keyword
    def menu_select(self, menulocation):
        """
        Given a menu location, select that menu item. The menu location should be given in this form: "Edit ->
        Replace" or "File -> Save As" Spaces are not important in this form, so "File->SaveAs" is also acceptable.

        """
        if self.app is None:
            raise UnboundLocalError("There is no application context currently set")
        if self.dlg is None:
            raise UnboundLocalError("There is no dialog context currently set")
        # TODO: Should I catch an error here? What if I specify a menu item that doesn't exist?
        self.dlg.menu_select(menulocation)

    @keyword
    def GetWindowText(self):
        """
        Get the text of the currently selected dialog.
        Quite a few controls have other text that is visible, for example Edit controls usually have an empty string for WindowText
        but still have text displayed in the edit window.
        """
        if self.app is None:
            raise UnboundLocalError("There is no application context currently set")
        if self.dlg is None:
            raise UnboundLocalError("There is no dialog context currently set")

        return self.dlg.WindowText()

    @keyword
    def GetControlText(self, control):
        """
        Get the text contained within a control on the current dialog.
        """
        if self.app is None:
            raise UnboundLocalError("There is no application context currently set")
        if self.dlg is None:
            raise UnboundLocalError("There is no dialog context currently set")

        return self.dlg[control].WindowText()

    @keyword
    def GetNumberOfChildren(self, control):
        """
        Given a control on the current dialog, return the number of children of that control.
        IE, in a combo box, return the number of options. In a tab set, return the number of tabs.
        """
        if self.app is None:
            raise UnboundLocalError("There is no application context currently set")
        if self.dlg is None:
            raise UnboundLocalError("There is no dialog context currently set")

        return self.dlg[control].ControlCount()

    @keyword
    def ControlIsActive(self, control):
        """
        Given a control on the current dialog, assert that it is visible and enabled. If not, throw an error.
        """
        if self.app is None:
            raise UnboundLocalError("There is no application context currently set")
        if self.dlg is None:
            raise UnboundLocalError("There is no dialog context currently set")

        self.dlg[control].VerifyActionable()

    @keyword
    def ControlIsEnabled(self, control):
        """
        Given a control on the current dialog, assert that it is enabled. If not, throw an error.
        """
        if self.app is None:
            raise UnboundLocalError("There is no application context currently set")
        if self.dlg is None:
            raise UnboundLocalError("There is no dialog context currently set")

        self.dlg[control].VerifyEnabled()

    @keyword
    def ControlIsVisible(self, control):
        """
        Given a control on the current dialog, assert that it is visible. If not, throw an error.
        """
        if self.app is None:
            raise UnboundLocalError("There is no application context currently set")
        if self.dlg is None:
            raise UnboundLocalError("There is no dialog context currently set")

        self.dlg[control].VerifyVisible()

    @keyword
    def Click(self, control):
        """
        Send a click event to a control.

        This method sends WM_* messages to the control, to do a more 'realistic' mouse click use "win Real Click"
        which uses SendInput() API to perform the click. This method does not require that the control be visible on
        the screen (i.e. is can be hidden beneath another window and it will still work.)
        """
        if self.app is None:
            raise UnboundLocalError("There is no application context currently set")
        if self.dlg is None:
            raise UnboundLocalError("There is no dialog context currently set")

        self.dlg[control].click()

    @keyword
    def RealClick(self, control):
        """
        Move the mouse to the specified control, and click on it. DON'T MOVE THE MOUSE while using this action.

        This is different from Click in that it requires the control to be visible on the screen but performs a more realistic 'click' simulation.
        This method is also vulnerable if the mouse if moved by the user as that could easily move the mouse off the control before the Click has finished.
        """
        if self.app is None:
            raise UnboundLocalError("There is no application context currently set")
        if self.dlg is None:
            raise UnboundLocalError("There is no dialog context currently set")

        self.dlg[control].ClickInput()

    @keyword
    def DoubleClick(self, control):
        """
        Send a double click event to a control.

        This method sends WM_* messages to the control, to do a more 'realistic' mouse click use "win Real Double Click" which uses SendInput() API to perform the click.
        This method does not require that the control be visible on the screen (i.e. is can be hidden beneath another window and it will still work.)
        """
        if self.app is None:
            raise UnboundLocalError("There is no application context currently set")
        if self.dlg is None:
            raise UnboundLocalError("There is no dialog context currently set")

        self.dlg[control].Doubleclick()

    @keyword
    def RealDoubleClick(self, control):
        """
        Move the mouse to the specified control, and double click on it. DON'T MOVE THE MOUSE while using this action.

        This is different from Double Click in that it requires the control to be visible on the screen but performs a more realistic 'doubleclick' simulation.
        This method is also vulnerable if the mouse if moved by the user as that could easily move the mouse off the control before the doubleclick has finished.
        """
        if self.app is None:
            raise UnboundLocalError("There is no application context currently set")
        if self.dlg is None:
            raise UnboundLocalError("There is no dialog context currently set")

        self.dlg[control].DoubleClickInput()

    @keyword
    def RightClick(self, control):
        """
        Send a right click event to a control.

        This method sends WM_* messages to the control, to do a more 'realistic' mouse click use "win Real Right Click" which uses SendInput() API to perform the click.
        This method does not require that the control be visible on the screen (i.e. is can be hidden beneath another window and it will still work.)
        """
        if self.app is None:
            raise UnboundLocalError("There is no application context currently set")
        if self.dlg is None:
            raise UnboundLocalError("There is no dialog context currently set")

        self.dlg[control].Rightclick()

    @keyword
    def RealRightClick(self, control):
        """
        Move the mouse to the specified control, and right click on it. DON'T MOVE THE MOUSE while using this action.

        This is different from Right Click in that it requires the control to be visible on the screen but performs a more realistic 'right click' simulation.
        This method is also vulnerable if the mouse if moved by the user as that could easily move the mouse off the control before the right click has finished.
        """
        if self.app is None:
            raise UnboundLocalError("There is no application context currently set")
        if self.dlg is None:
            raise UnboundLocalError("There is no dialog context currently set")

        self.dlg[control].RightClickInput()

    @keyword
    def DragMouse(self, control, press_x, press_y, release_x, release_y, button='left'):
        """
        Press, move and release the mouse button specified by "button" (left by default).
        The coordinates to press the mouse button at are x and y for "press_x" and "press_y" respectively.
        The coordinates to release the mouse button at are x and y for "release_x" and "release_y" respectively.
        """
        if self.app is None:
            raise UnboundLocalError("There is no application context currently set")
        if self.dlg is None:
            raise UnboundLocalError("There is no dialog context currently set")

        self.dlg[control].DragMouse(button=button, press_coords=(press_x, press_y),
                                    release_coords=(release_x, release_y))

    @keyword
    def TypeKeys(self, control, keys):
        """
        Type keyboard keys into the control.

        For how to do special characters, and other functionality above and beyond, check the sendkeys module in python.
        http://www.rutherfurd.net/python/sendkeys/
        The parameters for sendkeys used are: (pause=0.05, with_spaces=True, with_tabs=True, with_newlines=True, turn_off_numlock=True)
        """
        if self.app is None:
            raise UnboundLocalError("There is no application context currently set")
        if self.dlg is None:
            raise UnboundLocalError("There is no dialog context currently set")

        self.dlg[control].type_keys(keys, pause=0.05, with_spaces=True, with_tabs=True, with_newlines=True,
                                    turn_off_numlock=True)

    @keyword
    def CloseWindow(self):
        """
        Close the selected dialog
        """
        if self.app is None:
            raise UnboundLocalError("There is no application context currently set")
        if self.dlg is None:
            raise UnboundLocalError("There is no dialog context currently set")

        self.dlg.Close()

    @keyword
    def MaximizeWindow(self):
        """
        Maximize the selected dialog
        """
        if self.app is None:
            raise UnboundLocalError("There is no application context currently set")
        if self.dlg is None:
            raise UnboundLocalError("There is no dialog context currently set")

        self.dlg.Maximize()

    @keyword
    def MinimizeWindow(self):
        """
        Maximize the selected dialog
        """
        if self.app is None:
            raise UnboundLocalError("There is no application context currently set")
        if self.dlg is None:
            raise UnboundLocalError("There is no dialog context currently set")

        self.dlg.Minimize()

    @keyword
    def RestoreWindow(self):
        """
        Maximize the selected dialog
        """
        if self.app is None:
            raise UnboundLocalError("There is no application context currently set")
        if self.dlg is None:
            raise UnboundLocalError("There is no dialog context currently set")

        self.dlg.Restore()

    @keyword
    def SetWindowFocus(self):
        """
        Sets the current focus to the currently selected window.
        This will bring the window to the foreground if neccesary.
        """
        if self.app is None:
            raise UnboundLocalError("There is no application context currently set")
        if self.dlg is None:
            raise UnboundLocalError("There is no dialog context currently set")

        self.dlg.SetFocus()

    @keyword
    def SetFocus(self, control):
        """
        Sets the current focus to the specified control.
        This will bring the window to the foreground if neccesary.
        """
        if self.app is None:
            raise UnboundLocalError("There is no application context currently set")
        if self.dlg is None:
            raise UnboundLocalError("There is no dialog context currently set")

        self.dlg[control].SetFocus()

    @keyword
    def Scroll(self, control, direction, amount, count=1):
        """
        direction can be any of "up", "down", "left", "right"
        amount can be one of "line", "page", "end"
        count (optional) the number of times to scroll
        """
        if self.app is None:
            raise UnboundLocalError("There is no application context currently set")
        if self.dlg is None:
            raise UnboundLocalError("There is no dialog context currently set")

        self.dlg[control].Scroll(direction, amount, count)

    @keyword
    def ControlHasFocus(self, control):
        """
        ### NOT COMPLETE - DO NOT USE ###
        Assert that the specified control has focus.
        """
        # TODO: Do this
        pass

    @keyword
    def ControlIsCheckBox(self, control):
        """
        Assert that the specified control is a check box
        """
        if self.app is None:
            raise UnboundLocalError("There is no application context currently set")
        if self.dlg is None:
            raise UnboundLocalError("There is no dialog context currently set")

        assert (self.dlg[control].FriendlyClassName == "CheckBox")

    @keyword
    def ControlIsButton(self, control):
        """
        Assert that the specified control is a button
        """
        if self.app is None:
            raise UnboundLocalError("There is no application context currently set")
        if self.dlg is None:
            raise UnboundLocalError("There is no dialog context currently set")

        assert (self.dlg[control].FriendlyClassName == "Button")

    @keyword
    def ControlIsRadioButton(self, control):
        """
        Assert that the specified control is a check box
        """
        if self.app is None:
            raise UnboundLocalError("There is no application context currently set")
        if self.dlg is None:
            raise UnboundLocalError("There is no dialog context currently set")

        assert (self.dlg[control].FriendlyClassName == "RadioButton")

    @keyword
    def ControlIsGroupBox(self, control):
        """
        Assert that the specified control is a check box
        """
        if self.app is None:
            raise UnboundLocalError("There is no application context currently set")
        if self.dlg is None:
            raise UnboundLocalError("There is no dialog context currently set")

        assert (self.dlg[control].FriendlyClassName == "GroupBox")

    @keyword
    def ControlIsChecked(self, control):
        """
        Assert that the specified control is checked (checkbox, radio, etc.)
        """
        if self.app is None:
            raise UnboundLocalError("There is no application context currently set")
        if self.dlg is None:
            raise UnboundLocalError("There is no dialog context currently set")

        assert (self.dlg[control].GetCheckState() == 1)

    @keyword
    def ControlIsChecked(self, control):
        """
        Assert that the specified control is checked (checkbox, radio, etc.)
        """
        if self.app is None:
            raise UnboundLocalError("There is no application context currently set")
        if self.dlg is None:
            raise UnboundLocalError("There is no dialog context currently set")

        assert (self.dlg[control].GetCheckState() == 1)

    @keyword
    def ControlIsUnChecked(self, control):
        """
        Assert that the specified control is unchecked (checkbox, radio, etc.)
        """
        if self.app is None:
            raise UnboundLocalError("There is no application context currently set")
        if self.dlg is None:
            raise UnboundLocalError("There is no dialog context currently set")

        assert (self.dlg[control].GetCheckState() == 0)

    @keyword
    def ControlIsIndeterminate(self, control):
        """
        Assert that the specified control is in an indeterminate state (checkbox is partially checked)
        """
        if self.app is None:
            raise UnboundLocalError("There is no application context currently set")
        if self.dlg is None:
            raise UnboundLocalError("There is no dialog context currently set")

        assert (self.dlg[control].GetCheckState() == 2)

    @keyword
    def SetCheckboxToChecked(self, control):
        """
        Set the specified checkbox's state to checked.
        """
        if self.app is None:
            raise UnboundLocalError("There is no application context currently set")
        if self.dlg is None:
            raise UnboundLocalError("There is no dialog context currently set")

        self.dlg[control].Check()

    @keyword
    def SetCheckboxToUnChecked(self, control):
        """
        Set the specified checkbox's state to unchecked.
        """
        if self.app is None:
            raise UnboundLocalError("There is no application context currently set")
        if self.dlg is None:
            raise UnboundLocalError("There is no dialog context currently set")

        self.dlg[control].UnCheck()

    @keyword
    def SetCheckboxToIndeterminate(self, control):
        """
        Set the specified checkbox's state to unchecked.
        """
        if self.app is None:
            raise UnboundLocalError("There is no application context currently set")
        if self.dlg is None:
            raise UnboundLocalError("There is no dialog context currently set")

        self.dlg[control].SetCheckIndeterminate()

    @keyword
    def GetComboBoxItems(self, control):
        """
        Given a control name in the current dialog, pull a pipe delimited string of all the valid items in that combo box.
        """
        if self.app is None:
            raise UnboundLocalError("There is no application context currently set")
        if self.dlg is None:
            raise UnboundLocalError("There is no dialog context currently set")

        return "|".join(self.dlg[control].ItemTexts())

    @keyword
    def GetComboBoxItemCount(self, control):
        """
        Get a count of the items in a combo box
        """
        if self.app is None:
            raise UnboundLocalError("There is no application context currently set")
        if self.dlg is None:
            raise UnboundLocalError("There is no dialog context currently set")

        return self.dlg[control].ItemCount() + 1  # This returns a number starting count at 0

    @keyword
    def GetComboBoxSelectedIndex(self, control):
        """
        Get the selected index of a combo box
        """
        if self.app is None:
            raise UnboundLocalError("There is no application context currently set")
        if self.dlg is None:
            raise UnboundLocalError("There is no dialog context currently set")

        return self.dlg[control].SelectedIndex()

    @keyword
    def GetComboBoxSelectedValue(self, control):
        """
        Get the selected value's text of a combo box
        """
        if self.app is None:
            raise UnboundLocalError("There is no application context currently set")
        if self.dlg is None:
            raise UnboundLocalError("There is no dialog context currently set")

        # Texts returns the items in a combo box, with the first one being the selected item.
        return self.dlg[control].Texts()[0]

    @keyword
    def ComboBoxSelectIndex(self, control, value):
        """
        Select an item in the combo box. Value is an integer to the index of the item in the combo box.
        """
        if self.app is None:
            raise UnboundLocalError("There is no application context currently set")
        if self.dlg is None:
            raise UnboundLocalError("There is no dialog context currently set")

        self.dlg[control].Select(int(value))

    @keyword
    def ComboBoxSelectValue(self, control, value):
        """
        Select an item in the combo box. Value is a string with the exact text of the item to select in the combo box.
        """
        if self.app is None:
            raise UnboundLocalError("There is no application context currently set")
        if self.dlg is None:
            raise UnboundLocalError("There is no dialog context currently set")

        self.dlg[control].Select(value)

    @keyword
    def GetEditBoxLineCount(self, control):
        """
        Given an edit box control on the current dialog, return the number of lines in the edit box.
        """
        if self.app is None:
            raise UnboundLocalError("There is no application context currently set")
        if self.dlg is None:
            raise UnboundLocalError("There is no dialog context currently set")

        return self.dlg[control].LineCount() + 1  # This returns a number starting count at 0

    @keyword
    def GetEditBoxLineText(self, control, line_index):
        """
        Given an edit box control on the current dialog, and an int for the index of a line in that edit box, return that line's text.
        If you give this a line that doesn't exist, it returns an empty string.
        """
        if self.app is None:
            raise UnboundLocalError("There is no application context currently set")
        if self.dlg is None:
            raise UnboundLocalError("There is no dialog context currently set")

        return self.dlg[control].GetLine(line_index)

    @keyword
    def GetEditBoxText(self, control):
        """
        Given an edit box control on the current dialog, return the text for that control.
        """
        if self.app is None:
            raise UnboundLocalError("There is no application context currently set")
        if self.dlg is None:
            raise UnboundLocalError("There is no dialog context currently set")

        return self.dlg[control].TextBlock()

    @keyword
    def SetEditBoxText(self, control, textblock):
        """
        Given an edit box control on the current dialog, and a block of text, set the block to the text for that control.
        As this is windows vs linux, \\n won't represent a newline. \\r\\n is needed to represent a newline. This differs from sendkeys
        because you are setting the control text directly vs typing it.
        """
        if self.app is None:
            raise UnboundLocalError("There is no application context currently set")
        if self.dlg is None:
            raise UnboundLocalError("There is no dialog context currently set")

        self.dlg[control].SetEditText(textblock)

    @keyword
    def GetListBoxItems(self, control):
        """
        Given a control name in the current dialog, pull a pipe delimited string of all the valid items in that list box.
        """
        if self.app is None:
            raise UnboundLocalError("There is no application context currently set")
        if self.dlg is None:
            raise UnboundLocalError("There is no dialog context currently set")

        return "|".join(self.dlg[control].ItemTexts())

    @keyword
    def GetListBoxItemCount(self, control):
        """
        Get a count of the items in a list box
        """
        if self.app is None:
            raise UnboundLocalError("There is no application context currently set")
        if self.dlg is None:
            raise UnboundLocalError("There is no dialog context currently set")

        return self.dlg[control].ItemCount() + 1  # This returns a number starting count at 0

    @keyword
    def GetListBoxSelectedIndex(self, control):
        """
        Get the selected indices of a list box. Returns a pipe delimited list of the index of each selected item.
        """
        if self.app is None:
            raise UnboundLocalError("There is no application context currently set")
        if self.dlg is None:
            raise UnboundLocalError("There is no dialog context currently set")

        selected = []
        for i in self.dlg[control].SelectedIndices():
            selected.append(str(i))
        return "|".join(selected)

    @keyword
    def GetListBoxSelectedValue(self, control):
        """
        Get the selected value's text from a list box. Returns a pipe delimited list of the text of each selected item.
        """
        if self.app is None:
            raise UnboundLocalError("There is no application context currently set")
        if self.dlg is None:
            raise UnboundLocalError("There is no dialog context currently set")

        # get the texts for the values.
        texts = self.dlg[control].Texts()

        selected = []
        for i in self.dlg[control].SelectedIndices():
            # Select from the texts, the values of each selected item.
            selected.append(texts[i])
        return "|".join(selected)

    @keyword
    def ListBoxSelectIndex(self, control, value):
        """
        Select an item in the list box. Value is an integer to the index of the item in the list box.
        """
        if self.app is None:
            raise UnboundLocalError("There is no application context currently set")
        if self.dlg is None:
            raise UnboundLocalError("There is no dialog context currently set")

        self.dlg[control].Select(int(value))

    @keyword
    def ListBoxSelectValue(self, control, value):
        """
        Select an item in the list box. Value is a string with the exact text of the item to select in the list box.
        """
        if self.app is None:
            raise UnboundLocalError("There is no application context currently set")
        if self.dlg is None:
            raise UnboundLocalError("There is no dialog context currently set")

        self.dlg[control].Select(value)

    @keyword
    def ListBoxDeselectAll(self, control):
        """
        Deselect all currently selected items in a list box.
        Not 100% sure this works. Please test and let me know either way.
        """
        if self.app is None:
            raise UnboundLocalError("There is no application context currently set")
        if self.dlg is None:
            raise UnboundLocalError("There is no dialog context currently set")

        for i in self.dlg[control].SelectedIndices():
            # Select from the texts, the values of each selected item.
            self.dlg[control].Select(i)

    @keyword
    def GetListViewColumnCount(self, control):
        """
        Get a count of the columns in a listview control
        """
        if self.app is None:
            raise UnboundLocalError("There is no application context currently set")
        if self.dlg is None:
            raise UnboundLocalError("There is no dialog context currently set")

        return self.dlg[control].ColumnCount() + 1  # This returns a number starting count at 0

    @keyword
    def GetListViewItemCount(self, control):
        """
        Get a count of the items in a listview control
        """
        if self.app is None:
            raise UnboundLocalError("There is no application context currently set")
        if self.dlg is None:
            raise UnboundLocalError("There is no dialog context currently set")

        return self.dlg[control].ItemCount() + 1  # This returns a number starting count at 0

    @keyword
    def ListViewHeaderText(self, control):
        """
        Given a listview control, return a pipe delimited list of the header text associated with the columns
        """
        if self.app is None:
            raise UnboundLocalError("There is no application context currently set")
        if self.dlg is None:
            raise UnboundLocalError("There is no dialog context currently set")

        texts = []
        for i in self.dlg[control].Columns():
            texts.append(i["text"])
        return "|".join(texts)

    @keyword
    def ListViewGetSelectedCount(self, control):
        """
        Get the number of selected items in the listview
        """
        if self.app is None:
            raise UnboundLocalError("There is no application context currently set")
        if self.dlg is None:
            raise UnboundLocalError("There is no dialog context currently set")

        return self.dlg[control].GetSelectedCount() + 1  # This returns a number starting count at 0

    @keyword
    def ListViewIndexIsSelected(self, control, index):
        """
        Assert that the item specified by the index is selected
        """
        if self.app is None:
            raise UnboundLocalError("There is no application context currently set")
        if self.dlg is None:
            raise UnboundLocalError("There is no dialog context currently set")

        assert (self.dlg[control].IsSelected(index))

    @keyword
    def ListViewIndexIsNotSelected(self, control, index):
        """
        Assert that the item specified by the index is not selected
        """
        if self.app is None:
            raise UnboundLocalError("There is no application context currently set")
        if self.dlg is None:
            raise UnboundLocalError("There is no dialog context currently set")

        assert (self.dlg[control].IsSelected(index) == False)

    @keyword
    def ListViewSelectIndex(self, control, index):
        """
        Select an item specified by the index.
        """
        if self.app is None:
            raise UnboundLocalError("There is no application context currently set")
        if self.dlg is None:
            raise UnboundLocalError("There is no dialog context currently set")

        self.dlg[control].Select(index)

    @keyword
    def ListViewDeselectIndex(self, control, index):
        """
        Deselect an item specified by the index.
        """
        if self.app is None:
            raise UnboundLocalError("There is no application context currently set")
        if self.dlg is None:
            raise UnboundLocalError("There is no dialog context currently set")

        self.dlg[control].Deselect(index)

    @keyword
    def ListViewIndexIsChecked(self, control, index):
        """
        Assert that the item specified by the index is checked
        """
        if self.app is None:
            raise UnboundLocalError("There is no application context currently set")
        if self.dlg is None:
            raise UnboundLocalError("There is no dialog context currently set")

        assert (self.dlg[control].IsChecked(index))

    @keyword
    def ListViewIndexIsNotChecked(self, control, index):
        """
        Assert that the item specified by the index is not checked
        """
        if self.app is None:
            raise UnboundLocalError("There is no application context currently set")
        if self.dlg is None:
            raise UnboundLocalError("There is no dialog context currently set")

        assert (self.dlg[control].IsChecked(index) == False)

    @keyword
    def ListViewCheckIndex(self, control, index):
        """
        Check an item specified by the index.
        """
        if self.app is None:
            raise UnboundLocalError("There is no application context currently set")
        if self.dlg is None:
            raise UnboundLocalError("There is no dialog context currently set")

        self.dlg[control].Check(index)

    @keyword
    def ListViewUncheckIndex(self, control, index):
        """
        Uncheck an item specified by the index.
        """
        if self.app is None:
            raise UnboundLocalError("There is no application context currently set")
        if self.dlg is None:
            raise UnboundLocalError("There is no dialog context currently set")

        self.dlg[control].UnCheck(index)

    @keyword
    def GetStatusBarPartCount(self, control):
        """
        Return the number of "parts" associated with a status bar on the current dialog
        """
        if self.app is None:
            raise UnboundLocalError("There is no application context currently set")
        if self.dlg is None:
            raise UnboundLocalError("There is no dialog context currently set")

        return self.dlg[control].PartCount() + 1  # This returns a number starting count at 0

    @keyword
    def GetStatusBarPartText(self, control, index):
        """
        Given a status bar control, and the index of the part in that status bar, return the text contained
        """
        if self.app is None:
            raise UnboundLocalError("There is no application context currently set")
        if self.dlg is None:
            raise UnboundLocalError("There is no dialog context currently set")

        return self.dlg[control].GetPartText(index)

    @keyword
    def GetStatusBarText(self, control):
        """
        Given a status bar control, return the text contained in it's parts, in a pipe delimited string.
        """
        if self.app is None:
            raise UnboundLocalError("There is no application context currently set")
        if self.dlg is None:
            raise UnboundLocalError("There is no dialog context currently set")

        return "|".join(self.dlg[control].Texts())

    @keyword
    def GetTabCount(self, control):
        """
        Given a tab control, return the number of tabs in that control.
        """
        if self.app is None:
            raise UnboundLocalError("There is no application context currently set")
        if self.dlg is None:
            raise UnboundLocalError("There is no dialog context currently set")

        return self.dlg[control].TabCount() + 1  # This returns a number starting count at 0

    @keyword
    def GetSelectedTabIndex(self, control):
        """
        Given a tab control, return the index of the selected tab.
        """
        if self.app is None:
            raise UnboundLocalError("There is no application context currently set")
        if self.dlg is None:
            raise UnboundLocalError("There is no dialog context currently set")

        return self.dlg[control].GetSelectedTab()

    @keyword
    def GetTabText(self, control, index):
        """
        Given a tab control, and an index, return the text associated with the tab specified by the index
        """
        if self.app is None:
            raise UnboundLocalError("There is no application context currently set")
        if self.dlg is None:
            raise UnboundLocalError("There is no dialog context currently set")

        return self.dlg[control].GetTabText(index)

    @keyword
    def GetAllTabTexts(self, control, index):
        """
        Given a tab control, return the text associated with all tabs in that control, in a pipe delimited string
        """
        if self.app is None:
            raise UnboundLocalError("There is no application context currently set")
        if self.dlg is None:
            raise UnboundLocalError("There is no dialog context currently set")

        return "|".join(self.dlg[control].Texts())

    @keyword
    def SelectTabByText(self, control, text):
        """
        Given a tab control, and the text of a tab in it, select that tab.
        """
        if self.app is None:
            raise UnboundLocalError("There is no application context currently set")
        if self.dlg is None:
            raise UnboundLocalError("There is no dialog context currently set")

        self.dlg[control].Select(str(text))

    @keyword
    def SelectTabByIndex(self, control, index):
        """
        Given a tab control, and the text of a tab in it, select that tab.
        """
        if self.app is None:
            raise UnboundLocalError("There is no application context currently set")
        if self.dlg is None:
            raise UnboundLocalError("There is no dialog context currently set")

        self.dlg[control].Select(int(index))

    @keyword
    def GetToolbarButtonCount(self, control):
        """
        Given a toolbar control, return the number of buttons on the toolbar
        """
        if self.app is None:
            raise UnboundLocalError("There is no application context currently set")
        if self.dlg is None:
            raise UnboundLocalError("There is no dialog context currently set")

        return self.dlg[control].ButtonCount() + 1  # This returns a number starting count at 0

    @keyword
    def GetToolbarButtonText(self, control, index):
        """
        Given an index of a button on the specified toolbar control, return the button's text
        """
        if self.app is None:
            raise UnboundLocalError("There is no application context currently set")
        if self.dlg is None:
            raise UnboundLocalError("There is no dialog context currently set")

        return self.dlg[control].GetButton(index).text.value

    @keyword
    def ClickToolbarButton(self, control, text):
        """
        Given the text of a button on the specified toolbar control, press that button
        Not 100% sure this works. It's an undocumented feature in the pywinauto library...
        """
        if self.app is None:
            raise UnboundLocalError("There is no application context currently set")
        if self.dlg is None:
            raise UnboundLocalError("There is no dialog context currently set")

        self.dlg[control].PressButton(text)

    @keyword
    def GetTreeText(self, control):
        """
        Return all text for a tree in a pipe delimited string
        """
        if self.app is None:
            raise UnboundLocalError("There is no application context currently set")
        if self.dlg is None:
            raise UnboundLocalError("There is no dialog context currently set")

        "|".join(self.dlg[control].Texts())

    @keyword
    def ClickTreeElement(self, control, path):
        """
        Click a treeview control element by the path within the tree.
        The path should take the same form as a menu, where -> delimits the nodes.
        For example "Tree->Node2->Subnode1" would specify Subnode1 on the tree below

        + Tree
        ----+ Node1
        ----+ Node2
        --------+ Subnode1
        ----+ Node3
        --------+ Subnode2
        """
        if self.app is None:
            raise UnboundLocalError("There is no application context currently set")
        if self.dlg is None:
            raise UnboundLocalError("There is no dialog context currently set")

        path = '\\' + path.replace('->', '\\')

        self.dlg[control].GetItem(path).click()

    @keyword
    def RightClickTreeElement(self, control, path):
        """
        Right Click a treeview control element by the path within the tree.
        The path should take the same form as a menu, where -> delimits the nodes.
        For example "Tree->Node2->Subnode1" would specify Subnode1 on the tree below

        + Tree
        ----+ Node1
        ----+ Node2
        --------+ Subnode1
        ----+ Node3
        --------+ Subnode2
        """
        if self.app is None:
            raise UnboundLocalError("There is no application context currently set")
        if self.dlg is None:
            raise UnboundLocalError("There is no dialog context currently set")

        path = '\\' + path.replace('->', '\\')

        self.dlg[control].GetItem(path).Click(button='right')

    @keyword
    def DoubleClickTreeElement(self, control, path):
        """
        Double Click a treeview control element by the path within the tree.
        The path should take the same form as a menu, where -> delimits the nodes.
        For example "Tree->Node2->Subnode1" would specify Subnode1 on the tree below

        + Tree
        ----+ Node1
        ----+ Node2
        --------+ Subnode1
        ----+ Node3
        --------+ Subnode2
        """
        if self.app is None:
            raise UnboundLocalError("There is no application context currently set")
        if self.dlg is None:
            raise UnboundLocalError("There is no dialog context currently set")

        path = '\\' + path.replace('->', '\\')

        self.dlg[control].GetItem(path).Click(double=True)

    @keyword
    def ExpandTreeElement(self, control, path):
        """
        Expand a treeview control element by the path within the tree.
        The path should take the same form as a menu, where -> delimits the nodes.
        For example "Tree->Node2->Subnode1" would specify Subnode1 on the tree below

        + Tree
        ----+ Node1
        ----+ Node2
        --------+ Subnode1
        ----+ Node3
        --------+ Subnode2
        """
        if self.app is None:
            raise UnboundLocalError("There is no application context currently set")
        if self.dlg is None:
            raise UnboundLocalError("There is no dialog context currently set")

        path = '\\' + path.replace('->', '\\')

        self.dlg[control].GetItem(path).Expand()

    @keyword
    def Popupmenu_select(self, menulocation):
        """
        Given a popup menu option, select that menu item. The menu location should be given in this form: "Edit -> Replace" or "File -> Save As"
        Spaces are not important in this form, so "File->SaveAs" is also acceptable.
        """
        if self.app is None:
            raise UnboundLocalError("There is no application context currently set")
        if self.dlg is None:
            raise UnboundLocalError("There is no dialog context currently set")
        # TODO: Should I catch an error here? What if I specify a menu item that doesn't exist?
        self.app.PopupMenu.menu_select(menulocation)


if __name__ == '__main__':
    import sys
    from robotremoteserver import RobotRemoteServer

    RobotRemoteServer(PywinautoLibrary(), *sys.argv[1:])
