#
#   Module:     DotNet
#   Platform:   Python 3, Windows.NET
#
#   Some general helper classes for use with .NET Windows.Forms:
#
#       CustomMainMenu: 
#           A MainMenu created from a list of menu item parameters
#
#       CustomToolBar:
#           A ToolBar created from a list of toolbar item parameters.
#
#       SimpleContextMenu:
#           A ContextMenu created from a list of handlers and item text.
#
#   Copyright Craig Farrow, 2010 - 2024
#

import clr
clr.AddReference("System.Windows.Forms")

import os

from System.Windows.Forms import (
    MainMenu, MenuItem, Shortcut,
    ToolBar, ToolBarButton, ToolBarButtonStyle, ToolBarAppearance,
    ToolStrip, ToolStripContainer, ToolStripSeparator,
    ContextMenu,
    ImageList, 
    ColorDepth,
    DockStyle
    )

from System.Drawing import (Bitmap, Image)
 
# ------------------------------------------------------------------
class CustomMainMenu(MainMenu):
    """
    Creates a .NET MainMenu from an initialised structure:
        List of tuples: (Menu Title, Submenu List)
        Submenu List is a list of tuples:
            (Handler, Text, Shortcut, Tooltip)
            If the Handler is None, then the menu is disabled.
            Shortcut can be None instead of Shortcut.None (which
            has to be 'getattr(Shortcut, "None")' in Python 3.)
            If the tuple is None, then a separator is inserted.
        Handlers are standard .NET Event Handlers, which take two 
        parameters: the sender object, and System.EventArgs.
    """
    def __init__(self, menuList):
        MainMenu.__init__(self)
        for menu in menuList:
            newMenu = MenuItem()
            newMenu.Text, submenuList = menu
            for submenu in submenuList:
                newSubmenu = MenuItem()
                if submenu:
                    handler, newSubmenu.Text, shortcut, newSubmenu.Tooltip = submenu
                    if handler:
                        newSubmenu.Click += handler
                    else:
                        newSubmenu.Enabled = False
                    if shortcut:
                        newSubmenu.Shortcut = shortcut
                else:
                    newSubmenu.Text = "-"       # Separator
                newMenu.MenuItems.Add(newSubmenu)
            self.MenuItems.Add(newMenu)

# ------------------------------------------------------------------
class CustomToolBar(ToolBar):
    """
    Creates a .NET ToolBar from an initialised structure:
        buttonList = List of tuples: 
            (Handler, Text, ImageName, Tooltip)
            If the Handler is None, then the button is disabled.
            An item of None produces a toolbar separator.
        imagePathTuple = (prefix, suffix) pair to generate a full
            file path from the ImageName.
    """

    def __init__(self, buttonList, imagePathTuple):
        ToolBar.__init__(self)
        self.Appearance = ToolBarAppearance.Flat
        self.Dock = DockStyle.Top

        self.HandlerList = []
        self.ImageList = ImageList()
        self.ImageList.ColorDepth = ColorDepth.Depth32Bit

        for bParams in buttonList:
            button = ToolBarButton()
            if bParams:
                handler, button.Text, imageName, button.ToolTipText = bParams
                path, suffix = imagePathTuple
                imagePathName = os.path.join(path, imageName+suffix)
                self.ImageList.Images.Add(Bitmap.FromFile(imagePathName))
                button.ImageIndex = self.ImageList.Images.Count-1
                self.HandlerList.append(handler)
                if not handler:
                    button.Enabled = False
            else:
                button.Style = ToolBarButtonStyle.Separator
                self.HandlerList.append(None)   # Place-holder in handler list
            self.Buttons.Add(button)

        self.ButtonClick += self.__OnButtonClick

    def __OnButtonClick(self, sender, event):
        i = self.Buttons.IndexOf(event.Button)
        if self.HandlerList[i]:
            self.HandlerList[i]()               # Call the event handler
                
    def UpdateButtonText(self, buttonIndex, newText):
        self.Buttons[buttonIndex].Text = newText

# ------------------------------------------------------------------
class SimpleContextMenu(ContextMenu):
    """
    Creates a .NET ContextMenu from a list of tuples: 
        (Handler, Text)
    """

    def __init__(self, contextMenuItems):
        ContextMenu.__init__(self)

        for handler, itemText in contextMenuItems:
            item = MenuItem()
            item.Text = itemText
            item.Click += handler
            self.MenuItems.Add(item)
